import gzip,csv,calendar,json,math
from pathlib import Path
from statistics import mean
from collections import defaultdict
P=Path(__file__).parent
monthly=[]
for y in range(2011,2026):
 hours=defaultdict(list)
 with gzip.open(P/'data'/f'44098h{y}.txt.gz','rt') as f:
  names=next(f).lstrip('#').split()
  for l in f:
   if l.startswith('#'):continue
   r=dict(zip(names,l.split()));h,t,d=[float(r[k]) for k in ['WVHT','DPD','MWD']]
   if not(0<=h<30 and 0<t<40 and 0<=d<=360):continue
   incoming=45<=d<=135
   v={'incoming':int(incoming),'t_weight':t*incoming,'h_weight':h*incoming,'h2_weight':h*h*incoming,'power_proxy':h*h*t*incoming}
   for per in [8,10,12,14]:
    v[f't{per}']=int(incoming and t>=per)
    for height in [1,1.5,2,3]:v[f'h{height}_t{per}']=int(incoming and h>height and t>=per)
   hours[tuple(int(r[k]) for k in ['MM','DD','hh'])].append(v)
 months=defaultdict(list)
 for (m,day,hour),rs in hours.items():months[m].append({k:mean(r[k] for r in rs) for k in rs[0]})
 for m,rs in months.items():monthly.append(dict(year=y,month=m,coverage=len(rs)/(calendar.monthrange(y,m)[1]*24),**{k:mean(r[k] for r in rs) for k in rs[0]}))
with open(P/'height_period_monthly.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(monthly[0]));w.writeheader();w.writerows(monthly)
keys=list(monthly[0])[3:]
def summary(rows,months=range(1,13)):
 v={k:mean(mean(r[k] for r in rows if r['month']==m) for m in months) for k in keys}
 v['incoming_mean_period']=v['t_weight']/v['incoming'];v['incoming_mean_height']=v['h_weight']/v['incoming'];v['energy_weighted_period']=v['power_proxy']/v['h2_weight']
 return v
for cutoff in [.7,.8,.9]:
 print('CUTOFF',cutoff)
 for a,b in [(2011,2015),(2016,2020),(2021,2025),(2011,2020)]:
  rows=[r for r in monthly if a<=r['year']<=b and r['coverage']>=cutoff]
  print(a,b,json.dumps(summary(rows)))
# Annual observed-hour weighted metrics; no missing-hour imputation.
annual=[]
for y in range(2011,2026):
 rs=[r for r in monthly if r['year']==y]
 weights=[r['coverage']*calendar.monthrange(y,int(r['month']))[1]*24 for r in rs]
 vals={k:sum(r[k]*w for r,w in zip(rs,weights))/sum(weights) for k in keys}
 annual.append(dict(year=y,coverage=sum(weights)/(8784 if calendar.isleap(y) else 8760),incoming_mean_period=vals['t_weight']/vals['incoming'],incoming_mean_height=vals['h_weight']/vals['incoming'],**vals))
with open(P/'height_period_annual.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(annual[0]));w.writeheader();w.writerows(annual)
print('ANNUAL')
for r in annual:print(r['year'],*[round(r[k],4) for k in ['incoming_mean_period','incoming_mean_height','power_proxy','t10','t12','h3_t8','h3_t10','h3_t12']])
