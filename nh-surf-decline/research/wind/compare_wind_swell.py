import json,csv
from pathlib import Path
import numpy as np
P=Path(__file__).parent
s=json.load(open(P/'fetch_summary.json'));out={}
for k in ['ocean_mean_speed','u10_d0_f200_a30','u10_d12_f200_a30','u10_d24_f200_a30','u12_d12_f200_a30','u15_d12_f200_a30','u10_d12_f400_a30','u10_d12_f200_a45','u10_d24_f200_a45','u12_d12_f200_a45','u15_d12_f200_a45']:
 a=s['2016-2020'][k];b=s['2021-2025'][k];c=s['2011-2020'][k];out[k]=dict(old=a,new=b,change=100*(b/a-1),change_decade=100*(b/c-1));print(k,out[k])
w=np.load(P/'fetch_timeseries.npz');wave=np.load(P.parent/'spectral/hourly_metrics.npz');cols=list(wave['columns']);sites=['Hampton','Jenness','Wallis'];data=np.mean(wave['values'][:,[cols.index(site+'_offshore_100km_buf0:m0_8') for site in sites]],axis=1)
hours=wave['hours'];grid=np.arange(int(w['time'][0]),int(w['time'][-1])+1);arr=np.full(len(grid)+49,np.nan);arr[hours-hours[0]]=data
# Match forecasts to subsequent observed swell energy, retaining >=75% of 12-48h window.
pos=w['time']-hours[0];futures=np.array([np.nanmean(arr[p+12:p+49]) if np.isfinite(arr[p+12:p+49]).sum()>=28 else np.nan for p in pos])
months=w['time'].astype('datetime64[h]').astype('datetime64[M]').astype(int)%12+1
mask=w['u10_d12_f200_a30']>0
ratios=[];weights=[]
for m in range(1,13):
 valid=(months==m)&np.isfinite(futures);ev=valid&mask;control=valid&~mask
 if ev.any() and control.any():ratios.append(np.mean(futures[ev])/np.mean(futures[control]));weights.append(ev.sum())
print('following12-48h energy ratio month-weighted event sample',np.average(ratios,weights=weights),'event snapshots',sum(weights))
# Equal-month period summaries for cold/warm seasons.
rs=[{k:float(v) for k,v in r.items()} for r in csv.DictReader(open(P/'fetch_monthly.csv'))]
for season,ms in [('cold',[10,11,12,1,2,3,4]),('warm',[5,6,7,8,9])]:
 for k in ['u10_d12_f200_a30','u10_d24_f200_a30']:
  vals=[np.mean([np.mean([r[k] for r in rs if lo<=r['year']<=hi and r['month']==m]) for m in ms]) for lo,hi in [(2016,2020),(2021,2025)]]
  print(season,k,vals,100*(vals[1]/vals[0]-1))
# Exploratory year-block bootstrap of the principal regional index.
rng=np.random.default_rng(139);mats=[]
for ys in [range(2016,2021),range(2021,2026)]:mats.append(np.array([[next(r['u10_d12_f200_a30'] for r in rs if r['year']==y and r['month']==m) for m in range(1,13)] for y in ys]))
changes=[]
for _ in range(5000):
 a,b=[mat[rng.integers(0,5,5)].mean() for mat in mats];changes.append(100*(b/a-1))
print('bootstrap principal 95',np.percentile(changes,[2.5,97.5]))
(P/'comparison.json').write_text(json.dumps(dict(metrics=out,following_swell_ratio=float(np.average(ratios,weights=weights)),bootstrap95=np.percentile(changes,[2.5,97.5]).tolist()),indent=2))
