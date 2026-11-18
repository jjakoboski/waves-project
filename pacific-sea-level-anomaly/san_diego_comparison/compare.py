import os
os.environ['MPLCONFIGDIR']='/tmp/sla-mpl'
from pathlib import Path
import json
import numpy as np
import pandas as pd
import netCDF4 as nc
from pyproj import Geod
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as md
P=Path(__file__).resolve().parent
raw=json.loads((P/'hourly.json').read_text()); meta=raw['metadata']
def read_obs(name,prelim=False):
 d=pd.DataFrame(json.loads((P/name).read_text())['data']);d.index=pd.to_datetime(d.t)
 d['value']=pd.to_numeric(d.v,errors='coerce')
 flag=d.f.str.split(',').apply(lambda a:any(int(x)!=0 for x in (a[1:] if prelim else a)))
 d.loc[flag,'value']=np.nan
 return d.loc[d.index.minute==0,'value']
obs=pd.concat([read_obs('hourly.json'),read_obs('october_preliminary.json',True),read_obs('november_preliminary.json',True)]).sort_index()
assert not obs.index.duplicated().any()
pred=pd.DataFrame(json.loads((P/'predictions.json').read_text())['predictions']);pred.index=pd.to_datetime(pred.t);pred=pd.to_numeric(pred.v)
hourly=pd.DataFrame({'observed_m_MSL':obs,'predicted_m_MSL':pred});hourly['residual_cm']=(hourly.observed_m_MSL-hourly.predicted_m_MSL)*100
count=hourly.residual_cm.resample('D').count();daily=hourly.residual_cm.resample('D').mean().where(count>=20)
datasets=[nc.Dataset(f) for f in sorted((P.parent/'pacific_sla').glob('chunk*.nc'))]
lat=datasets[0]['latitude'][:];lon=datasets[0]['longitude'][:];x,y=np.meshgrid(lon,lat)
g=Geod(ellps='WGS84');_,_,dist=g.inv(np.full(x.shape,float(meta['lon'])),np.full(y.shape,float(meta['lat'])),x,y)
# Search nearest consistently valid point on precisely the animation's sampled grid.
a=np.ma.concatenate([d['sla'][:] for d in datasets]); valid=(~np.ma.getmaskarray(a)).all(axis=0)
ij=np.unravel_index(np.where(valid,dist,np.inf).argmin(),dist.shape)
t=np.concatenate([d['time'][:] for d in datasets]);dates=pd.to_datetime([v.isoformat() for v in nc.num2date(t,datasets[0]['time'].units)])
sat=pd.Series(a[:,ij[0],ij[1]].filled(np.nan)*100,index=dates)
pairs=pd.DataFrame({'satellite_cm_DTU15':sat,'gauge_daily_residual_cm':daily.reindex(dates)}).dropna()
smean=pairs.satellite_cm_DTU15.mean();gmean=pairs.gauge_daily_residual_cm.mean()
pairs['satellite_centered_cm']=pairs.satellite_cm_DTU15-smean;pairs['gauge_centered_cm']=pairs.gauge_daily_residual_cm-gmean
pairs['difference_cm']=pairs.satellite_centered_cm-pairs.gauge_centered_cm
stats={'n_pairs':len(pairs),'correlation':pairs.satellite_centered_cm.corr(pairs.gauge_centered_cm),'centered_rms_difference_cm':np.sqrt(np.mean(pairs.difference_cm**2)),'mean_absolute_centered_difference_cm':pairs.difference_cm.abs().mean(),'satellite_lat':float(lat[ij[0]]),'satellite_lon':float(lon[ij[1]]),'gauge_metadata':meta,'distance_km':float(dist[ij]/1000),'satellite_removed_mean_cm':smean,'gauge_removed_mean_cm':gmean,'valid_gauge_days':int(daily.notna().sum()),'total_days':len(daily),'min_hours':20}
for label,z in [('verified_only',pairs.loc[:'2026-09-30']),('recent_preliminary',pairs.loc['2026-10-01':])]:
 stats[label]={'n':len(z),'correlation':z.satellite_centered_cm.corr(z.gauge_centered_cm),'centered_rms_difference_cm':float(np.std(z.satellite_cm_DTU15-z.gauge_daily_residual_cm))}
print(json.dumps(stats,indent=2));(P/'statistics.json').write_text(json.dumps(stats,indent=2));pairs.to_csv(P/'paired_comparison.csv',index_label='date_UTC');pd.DataFrame({'residual_cm':daily,'valid_hours':count}).to_csv(P/'gauge_daily.csv',index_label='date_UTC')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#24384b','text.color':'#24384b'})
fig,(ax,bx)=plt.subplots(2,1,figsize=(12,8),sharex=True,gridspec_kw={'height_ratios':[3,1]},facecolor='#f7f9fb')
fig.subplots_adjust(left=.085,right=.97,top=.82,bottom=.19,hspace=.12)
fig.text(.085,.94,'SAN DIEGO  /  SATELLITE vs TIDE GAUGE',fontsize=21,weight='bold')
fig.text(.085,.895,'17 Nov 2025–16 Nov 2026  •  NOAA station 9410170  •  Offshore grid point ~21 km away',fontsize=11)
fig.text(.085,.854,f"53 matched dates   |   Correlation r = {stats['correlation']:.2f}   |   RMS difference = {stats['centered_rms_difference_cm']:.1f} cm",fontsize=12,weight='bold')
for axis in [ax,bx]:
 axis.set_facecolor('white');axis.axvspan(pd.Timestamp('2026-10-01'),pd.Timestamp('2026-11-17'),color='#f7e6c5',alpha=.6);axis.axhline(0,color='#8394a3',lw=.8);axis.grid(axis='y',alpha=.2)
ax.plot(daily.index,daily-gmean,color='#3e94a3',lw=.8,alpha=.35,label='Gauge: daily observed minus predicted tide')
ax.plot(daily.index,daily.rolling(7,center=True,min_periods=4).mean()-gmean,color='#007f89',lw=2,label='Gauge: 7-day mean (visual guide)')
ax.plot(pairs.index,pairs.satellite_centered_cm,'o-',color='#c65432',ms=3.5,lw=1.6,label='Satellite: weekly snapshots')
ax.set_ylabel('Centered sea level anomaly (cm)');ax.legend(loc='upper left',fontsize=9,frameon=False)
ax.text(.98,.97,'Shading: preliminary gauge data',transform=ax.transAxes,ha='right',va='top',fontsize=9)
bx.plot(pairs.index,pairs.difference_cm,'o-',ms=3,color='#59677d',lw=1);bx.set_ylabel('Satellite −\ngauge (cm)');bx.xaxis.set_major_locator(md.MonthLocator(interval=2));bx.xaxis.set_major_formatter(md.DateFormatter('%b %Y'));bx.set_xlim(pd.Timestamp('2025-11-17'),pd.Timestamp('2026-11-17'))
fig.text(.085,.10,'Each record has its own mean removed over the same 53 dates; absolute datums are not equated.\nStatistics and differences use daily gauge residuals on satellite dates (not the smoothed line).',fontsize=10,linespacing=1.5)
fig.text(.085,.035,'Sources: NOAA CO-OPS; NOAA CoastWatch. Altimetry data are provided by the NOAA Laboratory for Satellite Altimetry.\nOffshore gridded sea level and a harbor gauge need not match: local weather, coastal dynamics, and corrections differ.',fontsize=9,color='#586b7d',linespacing=1.5)
fig.savefig(P/'san_diego_comparison.png',dpi=160);fig.savefig(P/'san_diego_comparison.pdf')
