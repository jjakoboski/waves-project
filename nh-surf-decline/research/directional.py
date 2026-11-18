import gzip,csv,calendar,json
from collections import defaultdict
from statistics import mean
from pathlib import Path
P=Path(__file__).parent
sectors={'NE_SE':(45,135),'N_SE':(0,135),'NE_SSE':(45,157.5),'E_SE':(90,135)}
monthly=[]
for year in range(2011,2026):
 hours=defaultdict(list)
 with gzip.open(P/'data'/f'44098h{year}.txt.gz','rt') as f:
  names=next(f).lstrip('#').split()
  for l in f:
   if l.startswith('#'):continue
   r=dict(zip(names,l.split()));h,p,d=[float(r[k]) for k in ['WVHT','DPD','MWD']]
   if not (0<=h<30 and 0<p<40 and 0<=d<=360):continue
   v={}
   for s,(lo,hi) in sectors.items():
    incoming=lo<=d<=hi
    v[s+'_share']=int(incoming)
    v[s+'_h_weight']=h*incoming
    for t in [8,10]:
     v[s+f'_h1_p{t}']=int(incoming and h>=1 and p>=t)
    v[s+'_h1_5_p8']=int(incoming and h>=1.5 and p>=8)
    v[s+'_gt3_p8']=int(incoming and h>3 and p>=8)
   hours[tuple(int(r[k]) for k in ['MM','DD','hh'])].append(v)
 months=defaultdict(list)
 for (m,day,hour),rs in hours.items():months[m].append({k:mean(r[k] for r in rs) for k in rs[0]})
 for m,rs in months.items():monthly.append(dict(year=year,month=m,coverage=len(rs)/(calendar.monthrange(year,m)[1]*24),**{k:mean(r[k] for r in rs) for k in rs[0]}))
with open(P/'directional_monthly.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(monthly[0]));w.writeheader();w.writerows(monthly)
for cutoff in [.7,.8,.9]:
 print('CUTOFF',cutoff)
 for a,b in [(2011,2015),(2016,2020),(2021,2025),(2011,2020)]:
  rows=[r for r in monthly if a<=r['year']<=b and r['coverage']>=cutoff]
  result={k:mean(mean(r[k] for r in rows if r['month']==m) for m in range(1,13)) for k in list(monthly[0])[3:]}
  for s in sectors:result[s+'_conditional_height']=result[s+'_h_weight']/result[s+'_share']
  print(a,b,len(rows),json.dumps({k:round(v,5) for k,v in result.items()}))
  if cutoff==.8:
   for season,months in [('cold',[10,11,12,1,2,3,4]),('warm',[5,6,7,8,9])]:
    print(season,{k:round(mean(mean(r[k] for r in rows if r['month']==m) for m in months),5) for k in ['NE_SE_h1_p8','NE_SE_h1_5_p8','NE_SE_share']})
