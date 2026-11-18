import csv,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).parent;O=P.parent.parent/'output/wind';O.mkdir(exist_ok=True)
r=[{k:float(v) for k,v in r.items()} for r in csv.DictReader(open(P/'fetch_annual.csv'))];wave=json.load(open(P.parent/'spectral/report_results.json'))['annual']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.edgecolor':'#CCD8DF','axes.labelcolor':'#455D6D','xtick.color':'#455D6D','ytick.color':'#455D6D','text.color':'#153449'})
fig,axs=plt.subplots(2,1,figsize=(10,6.5),sharex=True,gridspec_kw={'hspace':.38});years=[v['year'] for v in r]
for ax in axs:
 ax.axvspan(2020.5,2025.4,color='#EFF4F5');ax.grid(axis='y',alpha=.18);ax.set_xlim(2010.6,2025.4)
axs[0].plot(years,[100*v['u10_d12_f200_a45'] for v in r],'o-',color='#7CABB0',label='Within 45° of the direction toward NH',lw=1.8,ms=4)
axs[0].plot(years,[100*v['u10_d12_f200_a30'] for v in r],'o-',color='#167F86',label='Within 30° (primary diagnostic)',lw=2,ms=4)
axs[0].set_ylim(0,4.5);axs[0].set_ylabel('Qualifying six-hour samples (%)');axs[0].set_title('Targeted, persistent wind setups became less common after 2020',loc='left',weight='bold',fontsize=12,pad=12);axs[0].legend(frameon=False,fontsize=9,loc='upper left');axs[0].text(2021,4.15,'2021–2025',fontsize=9,color='#566875')
axs[1].plot(years,[v['100km_buf0:index'] for v in wave],'o-',color='#C45B36',lw=2,ms=4);axs[1].axhline(100,color='#83949D',ls='--',lw=1);axs[1].set_ylim(0,155);axs[1].set_ylabel('Exposed ≥8 s swell energy index');axs[1].set_xticks(years[::2]);axs[1].set_title('But wind and swell do not move in lockstep: 2025 is the weakest swell year',loc='left',weight='bold',fontsize=11,pad=12)
fig.suptitle('Wind strength × alignment × fetch length × persistence',x=.09,y=.98,ha='left',fontsize=17,weight='bold')
fig.text(.09,.925,'Wind diagnostic: ≥10 m/s over a contiguous ≥200 km ocean segment, at every 6-hour sample spanning 12 hours.',fontsize=9)
fig.text(.09,.025,'Sources: NOAA PSL NCEP–NCAR Reanalysis 1; CDIP 160. Wind field is coarse (~150–210 km).\nSwell index baseline: 2016–2020 = 100. Diagnostic frequency is not a count of independent storms.',fontsize=8,color='#566875')
fig.subplots_adjust(left=.09,right=.97,top=.84,bottom=.12)
fig.savefig(O/'wind_fetch_and_swell.png',dpi=200);fig.savefig(O/'wind_fetch_and_swell.svg');print(O/'wind_fetch_and_swell.png')
