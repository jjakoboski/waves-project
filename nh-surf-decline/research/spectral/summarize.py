import csv,json,numpy as np
from pathlib import Path
P=Path(__file__).parent
s=json.load(open(P/'summary.json'))
sites=['Hampton','Jenness','Wallis'];metrics=['m0_8','m0_10','m0_12','gt3_8','gt3_10','gt3_12','gt2_12']
res={}
for suffix in ['100km_buf0','100km_buf-1','100km_buf500','50km_buf0','150km_buf0']:
 res[suffix]={}
 for k in metrics:
  a=np.array([s['0.8']['2016-2020']['metrics'][site+'_offshore_'+suffix+':'+k] for site in sites]);b=np.array([s['0.8']['2021-2025']['metrics'][site+'_offshore_'+suffix+':'+k] for site in sites])
  res[suffix][k]=dict(old=float(a.mean()),new=float(b.mean()),change_pct=float(100*(b.mean()/a.mean()-1)),site_changes=[float(100*(bv/av-1)) if av>0 else None for av,bv in zip(a,b)])
 print(suffix,json.dumps(res[suffix]))
rs=[{k:float(v) for k,v in r.items()} for r in csv.DictReader(open(P/'annual_metrics.csv'))]
annual=[]
for r in rs:
 row={k:r[k] for k in ['year','coverage']}
 for suffix in ['100km_buf0','100km_buf-1']:
  for k in metrics:
   row[suffix+':'+k]=float(np.mean([r[site+'_offshore_'+suffix+':'+k] for site in sites]))
 annual.append(row)
for suffix in ['100km_buf0','100km_buf-1']:
 baseline=np.mean([r[suffix+':m0_8'] for r in annual if 2016<=r['year']<=2020])
 for r in annual:r[suffix+':index']=100*r[suffix+':m0_8']/baseline
print('ANNUAL',json.dumps(annual,indent=2))
monthly=[{k:float(v) for k,v in r.items()} for r in csv.DictReader(open(P/'monthly_metrics.csv'))]
for suffix in ['100km_buf0','100km_buf-1']:
 def avg(lo,hi,months):return np.mean([np.mean([np.mean([r[site+'_offshore_'+suffix+':m0_8'] for site in sites]) for r in monthly if lo<=r['year']<=hi and r['month']==m and r['coverage']>=.8]) for m in months])
 print('2025 Jan-Jul change',suffix,100*(avg(2025,2025,range(1,8))/avg(2016,2020,range(1,8))-1))
# Year-block bootstrap retains within-year seasonality and storm clustering. Descriptive uncertainty.
rng=np.random.default_rng(891)
boot={}
for k in ['m0_8','gt3_8','gt3_10','gt3_12','gt2_12']:
 mats=[]
 for years in [range(2016,2021),range(2021,2026)]:
  arr=np.full((5,12),np.nan)
  for i,y in enumerate(years):
   for r in monthly:
    if r['year']==y and r['coverage']>=.8:arr[i,int(r['month'])-1]=np.mean([r[site+'_offshore_100km_buf0:'+k] for site in sites])
  mats.append(arr)
 samples=[]
 for b in range(4000):
  vals=[]
  for mat in mats:
   draw=mat[rng.integers(0,5,5)]
   if np.any(np.all(np.isnan(draw),axis=0)):break
   vals.append(np.mean(np.nanmean(draw,axis=0)))
  if len(vals)==2 and vals[0]>0:samples.append(100*(vals[1]/vals[0]-1))
 boot[k]=dict(percentile_95=np.percentile(samples,[2.5,97.5]).tolist(),replicates=len(samples))
print('BOOTSTRAP',json.dumps(boot))
(P/'report_results.json').write_text(json.dumps(dict(comparisons=res,annual=annual,bootstrap=boot),indent=2))
with open(P/'coast_summary_annual.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(annual[0]));w.writeheader();w.writerows(annual)
