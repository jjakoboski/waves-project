import gzip, csv, calendar, json
from pathlib import Path
from collections import defaultdict
from statistics import mean
ROOT=Path(__file__).parent
monthly=[]
for station in ['44098','44007']:
 for year in range(2011,2026):
  hourly=defaultdict(list)
  with gzip.open(ROOT/'data'/f'{station}h{year}.txt.gz','rt') as f:
   names=next(f).lstrip('#').split()
   for line in f:
    if line.startswith('#'): continue
    r=dict(zip(names,line.split()))
    h=float(r['WVHT']); p=float(r['DPD']); d=float(r['MWD'])
    if not 0<=h<30: continue
    v={'height_m':h,'ge1m':float(h>=1),'ge1_5m':float(h>=1.5),'ge2m':float(h>=2)}
    if 0<p<40:
     v['period_s']=p
     v['h1_p8']=float(h>=1 and p>=8)
     v['h1_p10']=float(h>=1 and p>=10)
     if 0<=d<=360:
      v['h1_p8_east']=float(h>=1 and p>=8 and 45<=d<=135)
    hourly[tuple(int(r[k]) for k in ['MM','DD','hh'])].append(v)
  months=defaultdict(list)
  for (m,day,hour),rs in hourly.items():
   keys=set().union(*(r.keys() for r in rs))
   months[m].append({k:mean([r[k] for r in rs if k in r]) for k in keys})
  for m,rs in months.items():
   out={'station':station,'year':year,'month':m,'coverage':len(rs)/(calendar.monthrange(year,m)[1]*24)}
   for k in set().union(*(r.keys() for r in rs)):
    vals=[r[k] for r in rs if k in r]
    out[k]=mean(vals) if len(vals)/len(rs)>=.8 else None
   monthly.append(out)
keys=list(monthly[0])
with open(ROOT/'monthly_metrics.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(monthly)
for station in ['44098','44007']:
 print('\nSTATION',station)
 for year in range(2011,2026):
  rows=[r for r in monthly if r['station']==station and r['year']==year]
  good=[r for r in rows if r['coverage']>=.8]
  print(year,'coverage',round(mean(r['coverage'] for r in rows),3),'months',len(good),'Hs',round(mean(r['height_m'] for r in good),3))
 for lo,hi in [(2011,2015),(2016,2020),(2021,2025),(2011,2020)]:
  rows=[r for r in monthly if r['station']==station and lo<=r['year']<=hi and r['coverage']>=.8]
  # Equal calendar-month weighting, then equal available years within month.
  result={k:round(mean(mean(r[k] for r in rows if r['month']==m and r.get(k) is not None) for m in range(1,13)),4) for k in keys[4:] if all(any(r['month']==m and r.get(k) is not None for r in rows) for m in range(1,13))}
  print(lo,hi,len(rows),json.dumps(result))
