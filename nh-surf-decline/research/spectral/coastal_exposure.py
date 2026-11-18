import sys,json
from pathlib import Path
import numpy as np
import shapefile
from shapely.geometry import shape,box,Point,LineString,mapping
from shapely.ops import transform,unary_union
from shapely import make_valid
from pyproj import Transformer,Geod
P=Path(__file__).parent
reader=shapefile.Reader(str(P/'coast/GSHHS_shp/h/GSHHS_h_L1.shp'))
print('bounds',reader.bbox)
# GSHHG geographic longitudes range -180..180 in this distribution.
region=box(-72,40,-66,46);pieces=[]
for s in reader.iterShapes():
 bb=box(*s.bbox)
 if not bb.intersects(region):continue
 g=make_valid(shape(s.__geo_interface__)).intersection(region)
 if not g.is_empty:pieces.append(g)
land=unary_union(pieces)
(P/'land_region.geojson').write_text(json.dumps(mapping(land)))
tr=Transformer.from_crs('EPSG:4326','EPSG:32619',always_xy=True)
back=Transformer.from_crs('EPSG:32619','EPSG:4326',always_xy=True)
land_m=transform(tr.transform,land)
geod=Geod(ellps='WGS84')
# Representative offshore receptors, not precise break coordinates.
sites={'Hampton_offshore':(-70.780,42.910),'Jenness_offshore':(-70.745,42.990),'Wallis_offshore':(-70.695,43.040)}
dirs=np.arange(.5,360,1.)
results={};summary={}
for name,(lon,lat) in sites.items():
 pt=Point(*tr.transform(lon,lat));assert not land_m.contains(pt),(name,'on land')
 assert np.max(np.abs(np.array(back.transform(pt.x,pt.y))-[lon,lat]))<1e-8
 for length in [50000,100000,150000]:
  for buffer in ([0,500,-1] if length==100000 else [0]):
   terrain=unary_union([g for g in land_m.geoms if g.area>=5e6]) if buffer==-1 else land_m.buffer(buffer)
   visible=[]
   for direction in dirs:
    dist=np.linspace(0,length,int(length/1000)+1)
    lo,la,_=geod.fwd(np.full(len(dist),lon),np.full(len(dist),lat),np.full(len(dist),direction),dist)
    x,y=tr.transform(lo,la)
    visible.append(not terrain.intersects(LineString(zip(x,y))))
   key=f'{name}_{length//1000}km_buf{buffer}'
   results[key]=np.array(visible,dtype=float)
   inds=np.flatnonzero(visible);groups=np.split(inds,np.where(np.diff(inds)>1)[0]+1)
   summary[key]=[[float(dirs[g[0]]-.5),float(dirs[g[-1]]+.5)] for g in groups if len(g)]
   print(key,summary[key])
np.savez(P/'exposure_masks.npz',directions=dirs,**results)
(P/'exposure_summary.json').write_text(json.dumps(dict(crs_source='EPSG:4326 WGS84 lon/lat degrees',crs_analysis='EPSG:32619 WGS84 UTM19N meters',rays='WGS84 ellipsoidal geodesics, sampled every 1 km',coast='GSHHG 2.3.7 high-resolution level-1 polygons',sites=sites,windows=summary),indent=2))
