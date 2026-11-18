import sys,json,csv,calendar
from pathlib import Path
import numpy as np
from scipy.interpolate import RegularGridInterpolator
P=Path(__file__).parent;sys.path.insert(0,str(P.parent/'spectral'));from dap_read import arrays
geo=json.load(open(P/'fetch_geometry.json'));points=np.array(geo['points_lat_lon360']);water=np.array(geo['open_water']);bearing=np.array(geo['local_from_bearings'])
U=[];V=[];times=[]
for year in range(2011,2026):
 vals=[]
 for var in ['uwnd','vwnd']:
  a,t,lat,lon=arrays(P/'data'/f'{var}_{year}.dods',['>f4','>f8','>f4','>f4']);a=a.reshape(len(t),len(lat),len(lon))
  interp=RegularGridInterpolator((lat[::-1],lon),np.moveaxis(a[:,::-1,:],0,-1),bounds_error=False,fill_value=np.nan)
  vals.append(np.moveaxis(interp(points.reshape(-1,2)).reshape(*points.shape[:2],len(t)),-1,0))
 U.append(vals[0]);V.append(vals[1]);times.append(np.datetime64('1800-01-01T00')+t.astype('timedelta64[h]'))
U=np.concatenate(U);V=np.concatenate(V);times=np.concatenate(times);speed=np.hypot(U,V);direction=np.rad2deg(np.arctan2(-U,-V))%360
error=(direction-bearing[None,:,:]+180)%360-180
DURATIONS=[0,6,12,24,36,48,72];metrics={}
def past_all(cond,n):
 out=np.zeros(cond.shape,bool);out[n-1:]=np.all(np.lib.stride_tricks.sliding_window_view(cond,n,axis=0),axis=-1);return out
for sector,(lo,hi) in {'west':(225,315),'west_narrow':(240,300)}.items():
 for align in [30,45,90]:
  for threshold in [0.5,5,8,10,12,15]:
   cond=(speed>=threshold)&(direction>=lo)&(direction<=hi)&water[None,:,:]
   if align!=90:cond &= abs(error)>=(180-align)
   for duration in DURATIONS:
    persistent=past_all(cond,duration//6+1)
    for length in [200,400]:
     n=length//50+1
     x=np.any(np.all(np.lib.stride_tricks.sliding_window_view(persistent,n,axis=2),axis=-1),axis=(1,2))
     metrics[f'{sector}_a{align}_u{threshold}_d{duration}_L{length}']=x.astype(float)
# Reduce to calendar-month/annual metrics.
rows=[];annual=[]
for mo in np.unique(times.astype('datetime64[M]')):
 ii=times.astype('datetime64[M]')==mo;y,m=map(int,str(mo).split('-'));r=dict(year=y,month=m);r.update({k:float(v[ii].mean()) for k,v in metrics.items()});rows.append(r)
for y in range(2011,2026):
 ii=times.astype('datetime64[Y]')==np.datetime64(str(y));r=dict(year=y);r.update({k:float(v[ii].mean()) for k,v in metrics.items()});annual.append(r)
for label,rs in [('monthly',rows),('annual',annual)]:
 with open(P/f'offshore_{label}.csv','w') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
summary={}
for lo,hi in [(2011,2020),(2016,2020),(2021,2025)]:
 rs=[r for r in rows if lo<=r['year']<=hi];summary[f'{lo}-{hi}']={k:float(np.mean([np.mean([r[k] for r in rs if r['month']==m]) for m in range(1,13)])) for k in metrics}
(P/'offshore_summary.json').write_text(json.dumps(summary,indent=2))
for threshold in [0.5,5,8,10,12,15]:
 for duration in DURATIONS:
  k=f'west_a45_u{threshold}_d{duration}_L200';a=summary['2016-2020'][k];b=summary['2021-2025'][k]
  print(k,round(100*a,3),round(100*b,3),round(100*(b/a-1),1) if a else None)
# Local buoy persistence uses the same endpoint convention: at least D hours
# between first and last hourly observations, requiring D+1 contiguous samples.
buoyrows=[]
for station in ['44007','44013']:
 z=np.load(P/f'{station}_hourly.npz');tt=z['hour'].astype('datetime64[h]');sp=z['speed'];dd=z['direction'];valid=np.isfinite(sp)&np.isfinite(dd)
 bm={};eligible={}
 for u in [0.5,5,8,10,12]:
  cond=valid&(sp>=u)&(dd>=225)&(dd<=315)
  for duration in [0,6,12,24,36,48]:
   k=f'u{u}_d{duration}';bm[k]=past_all(cond,duration+1);eligible[k]=past_all(valid,duration+1)
 for mon in np.unique(tt.astype('datetime64[M]')):
  ii=tt.astype('datetime64[M]')==mon;y,m=map(int,str(mon).split('-'));r=dict(station=station,year=y,month=m,coverage=float(valid[ii].mean()))
  for k,v in bm.items():
   jj=ii&eligible[k];r[k]=float(v[jj].mean()) if jj.any() else None
  buoyrows.append(r)
with open(P/'offshore_buoy_monthly.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(buoyrows[0]));w.writeheader();w.writerows(buoyrows)
print('LOCAL BUOYS')
for station in ['44007','44013']:
 for k in ['u5_d12','u5_d24','u10_d12','u10_d24']:
  vals=[]
  for lo,hi in [(2016,2020),(2021,2025)]:
   rs=[r for r in buoyrows if r['station']==station and lo<=r['year']<=hi and r['coverage']>=.8]
   vals.append(np.mean([np.mean([r[k] for r in rs if r['month']==m and r[k]!=None]) for m in range(1,13)]))
  print(station,k,vals,100*(vals[1]/vals[0]-1) if vals[0] else None)
# numerical consistency
for u in [0.5,5,8,10,12,15]:
 for a,b in zip(DURATIONS[:-1],DURATIONS[1:]):assert np.all(metrics[f'west_a45_u{u}_d{b}_L200']<=metrics[f'west_a45_u{u}_d{a}_L200'])
print('COMPLETE')
