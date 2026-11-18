import json,csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).parent
s=json.load(open(P/'offshore_summary.json'));rs=list(csv.DictReader(open(P/'offshore_annual.csv')))
fig,axs=plt.subplots(1,2,figsize=(12,4.8));colors=['#277b96','#d37836']
for period,col in zip(['2016-2020','2021-2025'],colors):
 ds=[6,12,24,36,48,72];axs[0].plot(ds,[s[period][f'west_a45_u10_d{d}_L200']*100 for d in ds],'-o',label=period,color=col)
axs[0].set(title='Long offshore spells did not become more common',xlabel='Minimum sustained duration (hours)',ylabel='Qualifying six-hourly observations (%)');axs[0].legend(frameon=False)
years=[int(r['year']) for r in rs]
axs[1].plot(years,[float(r['west_a45_u10_d24_L200'])*100 for r in rs],'-o',color=colors[0]);axs[1].axvspan(2020.5,2025.5,color=colors[1],alpha=.12)
axs[1].set(title='2025 was strong; 2022–2023 were weak',xlabel='Year',ylabel='Observations after ≥24 hours (%)',xticks=[2011,2014,2017,2020,2023,2025])
for ax in axs:ax.grid(axis='y',alpha=.2);ax.spines[['top','right']].set_visible(False);ax.set_ylim(bottom=0)
fig.suptitle('Persistence of winds blowing offshore from New Hampshire',fontsize=16,fontweight='bold',y=.98)
fig.text(.06,.025,'Winds from 225–315° at ≥10 m/s (22 mph), over ≥200 km of open water; within 45° of an outward corridor.\nNOAA PSL NCEP–NCAR reanalysis, 2011–2025. Left: calendar-month balanced. Right: annual fractions. These are not storm counts.',fontsize=9,color='#444444')
fig.tight_layout(rect=[0,.13,1,.9]);out=Path(__file__).resolve().parents[2]/'output/wind';out.mkdir(parents=True,exist_ok=True);fig.savefig(out/'offshore_persistence.png',dpi=180);fig.savefig(out/'offshore_persistence.svg')
