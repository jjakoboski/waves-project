import csv,calendar,json
from statistics import mean
from pathlib import Path
P=Path(__file__).parent
rows=[{k:float(v) for k,v in r.items()} for r in csv.DictReader(open(P/'directional_monthly.csv'))]
key='NE_SE_gt3_p8'
clim={m:mean(r[key] for r in rows if r['month']==m and r['coverage']>=.8) for m in range(1,13)}
annual=[]
for y in range(2011,2026):
 rs=[r for r in rows if r['year']==y];good=[r for r in rs if r['coverage']>=.8]
 hours=lambda r:r['coverage']*calendar.monthrange(y,int(r['month']))[1]*24
 obs=sum(hours(r) for r in rs)
 raw=sum(r[key]*hours(r) for r in rs)/obs
 adjusted=mean(clim.values())+mean(r[key]-clim[r['month']] for r in good)
 annual.append(dict(year=y,coverage_pct=100*obs/(8784 if calendar.isleap(y) else 8760),observed_pct=raw*100,seasonally_adjusted_pct=adjusted*100,good_months=len(good)))
print(json.dumps(annual,indent=2))
with open(P/'yearly_results.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(annual[0]));w.writeheader();w.writerows(annual)
# Exploratory single-step model: monthly fixed effects plus indicator for years >= breakpoint.
# Residualize both outcome and step indicator by calendar month; least squares closed form.
for key in ['NE_SE_gt3_p8','NE_SSE_gt3_p8']:
 for end in [2024,2025]:
  for cutoff in [.7,.8,.9]:
   rs=[r for r in rows if r['year']<=end and r['coverage']>=cutoff]
   ym={m:mean(r[key] for r in rs if r['month']==m) for m in range(1,13)}
   fits=[]
   for start in range(2014,end-1):
    xm={m:mean(int(r['year']>=start) for r in rs if r['month']==m) for m in range(1,13)}
    xy=sum((r[key]-ym[r['month']])*(int(r['year']>=start)-xm[r['month']]) for r in rs)
    xx=sum((int(r['year']>=start)-xm[r['month']])**2 for r in rs)
    fits.append((round(xy*xy/xx,6),start,round(100*xy/xx,3)))
   print(key,end,cutoff,'best breaks improvement/year/pp',sorted(fits,reverse=True)[:4])
