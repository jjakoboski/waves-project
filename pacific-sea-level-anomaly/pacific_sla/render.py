import os, sys, json
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/sla-mpl'

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import netCDF4 as nc
from datetime import datetime, timezone
P=Path(__file__).resolve().parent
datasets=[nc.Dataset(f) for f in sorted(P.glob('chunk*.nc'))]
lat=datasets[0]['latitude'][:]; rawlon=datasets[0]['longitude'][:]
ix=np.r_[np.where(rawlon>=120)[0],np.where(rawlon<=-70)[0]]
lon=rawlon[ix].copy();lon[lon<0]+=360
a=np.ma.concatenate([d['sla'][:,:,ix] for d in datasets],axis=0)*100
times=np.concatenate([d['time'][:] for d in datasets])
t=nc.num2date(times,datasets[0]['time'].units)
assert np.all(np.diff(lon)>0) and np.allclose(np.diff(lon),.5)
assert np.all(np.diff(times)>0)
assert a.shape==(len(t),len(lat),len(lon))
print('Data:',a.shape, str(t[0]),str(t[-1]),'cm percentiles:',np.percentile(a.compressed(),[1,50,99]),flush=True)
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':'#23364a','axes.labelcolor':'#23364a'})
fig=plt.figure(figsize=(12,9),facecolor='#f6f8fa')
ax=fig.add_axes([.055,.16,.89,.70],projection=ccrs.PlateCarree(central_longitude=180))
ax.set_extent([-60,110,-60,65],crs=ccrs.PlateCarree(central_longitude=180))
ax.set_facecolor('#dce4eb')
m=ax.pcolormesh(lon,lat,a[0],transform=ccrs.PlateCarree(),cmap='RdBu_r',vmin=-60,vmax=60,shading='auto',rasterized=True)
ax.add_feature(cfeature.LAND.with_scale('110m'),facecolor='#deded8',edgecolor='#68747d',linewidth=.45,zorder=3)
g=ax.gridlines(draw_labels=True,xlocs=[120,150,180,-150,-120,-90],ylocs=[-60,-30,0,30,60],linewidth=.45,color='#526679',alpha=.35)
g.top_labels=False;g.right_labels=False;g.xlabel_style={'size':9};g.ylabel_style={'size':9}
fig.text(.055,.947,'PACIFIC  /  SEA LEVEL ANOMALY',size=22,weight='bold')
fig.text(.055,.912,'Weekly snapshots of satellite-derived sea surface height',size=12,color='#526679')
date=fig.text(.945,.914,t[0].strftime('%d %b %Y'),ha='right',size=14,weight='bold')
cax=fig.add_axes([.26,.108,.48,.021]); cb=fig.colorbar(m,cax=cax,orientation='horizontal',extend='both',ticks=[-60,-30,0,30,60])
cb.set_label('Sea level anomaly (cm)  •  relative to DTU15 mean sea surface',fontsize=10)
fig.text(.055,.024,'NOAA CoastWatch / RADS • Daily fields sampled every ~7 days • 0.5° display sampling\nPacific-centered equirectangular projection • Gray ocean: missing data • Fixed color scale',fontsize=9,color='#526679',linespacing=1.6)
progress=fig.add_axes([.055,.875,.89,.004]);progress.set_xlim(0,len(t)-1);progress.set_ylim(0,1);progress.axis('off');progress.axhspan(0,1,color='#dce4eb');bar=progress.axhspan(0,1,xmax=.001,color='#287a9a')
def update(i):
 m.set_array(a[i].ravel());date.set_text(t[i].strftime('%d %b %Y'));bar.set_width(i/(len(t)-1))
 return m,date,bar
# Save representative stills and animation.
for i,name in [(0,'first'),(len(t)//2,'middle'),(len(t)-1,'preview')]:
 update(i);fig.savefig(P/f'{name}.png',dpi=120,facecolor=fig.get_facecolor())
anim=FuncAnimation(fig,update,frames=len(t),interval=200,blit=False)
anim.save(P/'pacific_sea_level_anomaly.gif',writer=PillowWriter(fps=5),dpi=90)
matplotlib.rcParams['animation.ffmpeg_path']='/Users/jkat/miniconda3/bin/ffmpeg'
anim.save(P/'pacific_sea_level_anomaly.mp4',writer=FFMpegWriter(fps=5,bitrate=2500),dpi=120)
manifest={'source':'https://coastwatch.noaa.gov/erddap/griddap/noaacwBLENDEDsshDaily.html','variable':'sla','source_units':'m','display_units':'cm','baseline':'DTU15 mean sea surface','dates':[x.isoformat() for x in t],'native_grid_degrees':.25,'sampled_grid_degrees':.5,'projection':'Plate Carree centered at 180 degrees','bounds':[120,290,-60,65],'frames':len(t),'range_cm':[-60,60],'retrieved_utc':datetime.now(timezone.utc).isoformat(),'note':'Every seventh available daily field; June 1 2026 is absent from source. No temporal interpolation or weekly averaging. Longitude east block shifted by +360 for continuous antimeridian plotting.'}
(P/'manifest.json').write_text(json.dumps(manifest,indent=2))
print('Done',flush=True)
