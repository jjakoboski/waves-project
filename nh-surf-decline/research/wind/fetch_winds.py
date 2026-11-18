import sys,json,csv,calendar
from pathlib import Path
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from shapely.geometry import shape,box,LineString
from shapely import make_valid
from shapely.ops import unary_union
from pyproj import Geod
import shapefile
P=Path(__file__).parent;sys.path.insert(0,str(P.parent/'spectral'));from dap_read import arrays
# WGS84, longitude-first. Rays use ellipsoidal distances; land intersections in lon/lat
# are topology-only, not planar angular distance measurements.
region=box(-73,32,-53,48);pieces=[]
for s in shapefile.Reader(str(P.parent/'spectral/coast/GSHHS_shp/h/GSHHS_h_L1.shp')).iterShapes():
 if box(*s.bbox).intersects(region):pieces.append(make_valid(shape(s.__geo_interface__)).intersection(region))
land=unary_union(pieces);geod=Geod(ellps='WGS84')
land=unary_union([g for g in land.geoms if abs(geod.geometry_area_perimeter(g)[0])>=5e6])
# Ignore small near-coast island shadows for a regional wind-source diagnostic.
# Start rays 50 km offshore; keep only rays whose first 50 km avoids mainland.
origin=(-70.745,42.99);angles=np.arange(45,151,15);distances=np.arange(50,851,50)*1000
points=[];water=[];bearings=[]
for az in angles:
 lo,la,back=geod.fwd(np.full(len(distances),origin[0]),np.full(len(distances),origin[1]),np.full(len(distances),az),distances)
 # Require uninterrupted open-water path from 50km to every further sample.
 openmask=[]
 for j in range(len(distances)):
  openmask.append(not land.intersects(LineString(zip(lo[:j+1],la[:j+1]))) if j else not land.contains(__import__('shapely').geometry.Point(lo[0],la[0])))
 points.append(np.column_stack([la,lo+360]));water.append(openmask)
 # Direction from source, opposite the local back-bearing toward NH.
 bearings.append((back+180)%360)
points=np.array(points);water=np.array(water);bearings=np.array(bearings)
# Mainland visibility near shore: require ray source direction within broad NE-SE
# regional ocean window. 150deg is blocked near NH by Cape Ann: explicitly test path
# from a 5km-offset point to 50km, allowing tiny offshore islands only.
for i,az in enumerate(angles):
 ds=np.linspace(5000,50000,46);lo,la,_=geod.fwd(np.full(46,origin[0]),np.full(46,origin[1]),np.full(46,az),ds)
 # If any coastal land intersects, exclude this corridor (conservative).
 if land.intersects(LineString(zip(lo,la))):water[i,:]=False
print('open ray max km',[(int(a),int(distances[np.flatnonzero(w)[-1]]/1000) if w.any() else 0) for a,w in zip(angles,water)],flush=True)
U=[];V=[];times=[]
for y in range(2011,2026):
 vals=[]
 for var in ['uwnd','vwnd']:
  a,t,lat,lon=arrays(P/'data'/f'{var}_{y}.dods',['>f4','>f8','>f4','>f4']);a=a.reshape(len(t),len(lat),len(lon));assert np.all(np.abs(a)<150)
  # Interpolate each 6-hour spatial field to the candidate fetch rays.
  values=np.moveaxis(a[:,::-1,:],0,-1)
  interp=RegularGridInterpolator((lat[::-1],lon),values,bounds_error=False,fill_value=np.nan)
  vals.append(np.moveaxis(interp(points.reshape(-1,2)).reshape(len(angles),len(distances),len(t)),-1,0))
 U.append(vals[0]);V.append(vals[1]);times.append((np.datetime64('1800-01-01T00')+t.astype('timedelta64[h]')).astype('datetime64[h]'))
U=np.concatenate(U);V=np.concatenate(V);times=np.concatenate(times)
assert np.all(np.diff(times).astype(int)==6)
speed=np.hypot(U,V);direction=(np.rad2deg(np.arctan2(-U,-V)))%360
error=(direction-bearings[None,:,:]+180)%360-180
metrics={}
# At each endpoint, require every sample in the preceding D hours to meet the
# speed and alignment condition at every point of at least one contiguous fetch.
for tolerance in [30,45]:
 for threshold in [8,10,12,15]:
  cond=(speed>=threshold)&(abs(error)<=tolerance)&water[None,:,:]
  for duration in [0,12,24,36]:
   n=duration//6+1
   persistent=np.zeros(cond.shape,bool)
   persistent[n-1:]=np.all(np.lib.stride_tricks.sliding_window_view(cond,n,axis=0),axis=-1)
   for fetch in [200,400]:
    width=fetch//50+1
    exists=np.any(np.all(np.lib.stride_tricks.sliding_window_view(persistent,width,axis=2),axis=-1),axis=(1,2))
    metrics[f'u{threshold}_d{duration}_f{fetch}_a{tolerance}']=exists.astype(float)
# Control diagnostics: strength/persistence without direction, and winds aimed away.
for sector in ['any_direction','away']:
 cond=(speed>=10)&water[None,:,:]
 if sector=='away':cond &= abs(error)>=150
 for duration in [12,24]:
  n=duration//6+1;persistent=np.zeros(cond.shape,bool)
  persistent[n-1:]=np.all(np.lib.stride_tricks.sliding_window_view(cond,n,axis=0),axis=-1)
  metrics[f'{sector}_u10_d{duration}_f200']=np.any(np.all(np.lib.stride_tricks.sliding_window_view(persistent,5,axis=2),axis=-1),axis=(1,2)).astype(float)
# Supporting regional offshore winds, for comparison independent of alignment.
validpoints=water
metrics['ocean_mean_speed']=speed[:,validpoints].mean(axis=1)
rows=[]
for mon in np.unique(times.astype('datetime64[M]')):
 ii=times.astype('datetime64[M]')==mon;y,m=map(int,str(mon).split('-'));r=dict(year=y,month=m,samples=int(ii.sum()))
 r.update({k:float(v[ii].mean()) for k,v in metrics.items()});rows.append(r)
with open(P/'fetch_monthly.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
annual=[]
for y in range(2011,2026):
 ii=times.astype('datetime64[Y]')==np.datetime64(str(y));r=dict(year=y);r.update({k:float(v[ii].mean()) for k,v in metrics.items()});annual.append(r)
with open(P/'fetch_annual.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(annual[0]));w.writeheader();w.writerows(annual)
summary={}
for lo,hi in [(2011,2020),(2016,2020),(2021,2025)]:
 rs=[r for r in rows if lo<=r['year']<=hi];summary[f'{lo}-{hi}']={k:float(np.mean([np.mean([r[k] for r in rs if r['month']==m]) for m in range(1,13)])) for k in metrics}
(P/'fetch_summary.json').write_text(json.dumps(summary,indent=2));np.savez_compressed(P/'fetch_timeseries.npz',time=times.astype('int64'),**metrics)
(P/'fetch_geometry.json').write_text(json.dumps(dict(origin=origin,angles=angles.tolist(),distances_m=distances.tolist(),points_lat_lon360=points.tolist(),open_water=water.tolist(),local_from_bearings=bearings.tolist()),indent=2))
for k in ['ocean_mean_speed','u10_d12_f200_a30','u10_d24_f200_a30','u12_d12_f200_a30','u15_d12_f200_a30','u10_d12_f400_a30','u12_d24_f400_a30']:
 a=summary['2016-2020'][k];b=summary['2021-2025'][k];print(k,a,b,100*(b/a-1) if a else None)
print('COMPLETE',len(times),flush=True)
