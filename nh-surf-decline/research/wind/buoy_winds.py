import gzip,csv,json,calendar
from collections import defaultdict
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
P=Path(__file__).parent
start=int(datetime(2011,1,1,tzinfo=timezone.utc).timestamp()/3600);stop=int(datetime(2026,1,1,tzinfo=timezone.utc).timestamp()/3600)
months=np.arange(start,stop).astype('datetime64[h]').astype('datetime64[M]');results=[]
def sustained(a,n):
 edges=np.diff(np.r_[False,a,False].astype(int));s=np.where(edges==1)[0];e=np.where(edges==-1)[0];out=np.zeros(len(a),bool)
 for x,y in zip(s,e):
  if y-x>=n:out[x:y]=True
 return out
for station in ['44005','44007','44013']:
 obs=defaultdict(list)
 for y in range(2011,2026):
  path=(P.parent/'data' if station=='44007' else P/'data')/f'{station}h{y}.txt.gz'
  if not path.exists():continue
  with gzip.open(path,'rt') as f:
   cols=next(f).lstrip('#').split()
   for l in f:
    if l.startswith('#'):continue
    r=dict(zip(cols,l.split()));s=float(r['WSPD']);d=float(r['WDIR'])
    if not(0<=s<60 and 0<=d<=360):continue
    t=int(datetime(int(r['YY']),int(r['MM']),int(r['DD']),int(r['hh']),tzinfo=timezone.utc).timestamp()/3600)
    if start<=t<stop:obs[t].append((s,d))
 speed=np.full(stop-start,np.nan);direction=speed.copy()
 for t,rs in obs.items():
  a=np.array(rs);speed[t-start]=a[:,0].mean();direction[t-start]=np.rad2deg(np.arctan2(np.mean(a[:,0]*np.sin(np.deg2rad(a[:,1]))),np.mean(a[:,0]*np.cos(np.deg2rad(a[:,1])))))%360
 valid=np.isfinite(speed);vals={'speed':speed}
 for sector,(lo,hi) in {'east':(45,135),'west':(225,315),'wide_east':(30,160)}.items():
  for v in [8,10,12,15]:
   cond=(speed>=v)&(direction>=lo)&(direction<=hi)
   for n in [1,6,12,24]:vals[f'{sector}_{v}ms_{n}h']=sustained(cond,n).astype(float)
 for mon in np.unique(months):
  ii=(months==mon)&valid;y,m=map(int,str(mon).split('-'));coverage=ii.sum()/(24*calendar.monthrange(y,m)[1])
  row=dict(station=station,year=y,month=m,coverage=coverage,hours=int(ii.sum()))
  row.update({k:float(np.mean(v[ii])) if ii.any() else None for k,v in vals.items()});results.append(row)
 np.savez_compressed(P/f'{station}_hourly.npz',hour=np.arange(start,stop),speed=speed,direction=direction)
with open(P/'buoy_monthly.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
for station in ['44005','44007','44013']:
 print(station)
 for y in range(2011,2026):print(y,round(np.mean([r['coverage'] for r in results if r['station']==station and r['year']==y]),2))
 for lo,hi in [(2016,2020),(2021,2025)]:
  rows=[r for r in results if r['station']==station and lo<=r['year']<=hi and r['coverage']>=.8]
  if any(not any(r['month']==m for r in rows) for m in range(1,13)):continue
  print(lo,hi,len(rows),{k:round(float(np.mean([np.mean([r[k] for r in rows if r['month']==m]) for m in range(1,13)])),5) for k in ['speed','east_10ms_6h','east_10ms_12h','east_12ms_12h','west_10ms_12h']})
