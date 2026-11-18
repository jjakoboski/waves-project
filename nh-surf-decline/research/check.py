import csv
from statistics import mean
from pathlib import Path
P=Path(__file__).parent
rs=list(csv.DictReader(open(P/'monthly_metrics.csv')))
for r in rs:
 for k,v in r.items():
  if k!='station':r[k]=float(v) if v else None
for s in ['44098','44007']:
 for cutoff in [.7,.8,.9]:
  print(s,'coverage cutoff',cutoff)
  for a,b in [(2016,2020),(2021,2025)]:
   rows=[r for r in rs if r['station']==s and a<=r['year']<=b and r['coverage']>=cutoff]
   for season,months in [('all',range(1,13)),('cold',[10,11,12,1,2,3,4]),('warm',[5,6,7,8,9])]:
    vals={k:round(mean(mean(r[k] for r in rows if r['month']==m and r.get(k)!=None) for m in months),4) for k in ['height_m','h1_p8','ge1_5m']}
    print(a,season,vals)
nao=[]
for l in open(P/'data/nao.txt'):
 try:y,m,v=l.split();nao.append((int(y),int(m),float(v)))
 except ValueError:pass
for a,b in [(2011,2015),(2016,2020),(2021,2025)]:
 print('NAO',a,b,[(name,round(mean(v for y,m,v in nao if a<=y<=b and m in months),3)) for name,months in [('all',range(1,13)),('cold',[10,11,12,1,2,3,4])]])
