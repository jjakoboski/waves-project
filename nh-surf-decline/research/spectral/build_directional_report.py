from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shapely.geometry import shape
from shapely.ops import transform
from pyproj import Transformer,Geod
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
P=Path(__file__).parent;O=P.parent.parent/'output/pdf';F=P/'figures';F.mkdir(exist_ok=True)
r=json.load(open(P/'report_results.json'));annual=r['annual'];case=r['comparisons']['100km_buf0'];alt=r['comparisons']['100km_buf-1']
navy='#153449';teal='#167F86';orange='#C45B36';gray='#566875'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.edgecolor':'#D8E2E6','xtick.color':gray,'ytick.color':gray,'text.color':navy,'axes.labelcolor':gray,'savefig.facecolor':'white'})
fig,ax=plt.subplots(figsize=(8.0,2.8));yrs=[a['year'] for a in annual];v=[a['100km_buf0:index'] for a in annual]
ax.axvspan(2020.5,2025.4,color='#F1F5F5');ax.axhline(100,color=gray,lw=1,ls='--');ax.plot(yrs,v,'o-',color=teal,lw=2,ms=4);ax.scatter([2025],[v[-1]],color=orange,zorder=5,s=28)
ax.set(xlim=(2010.7,2025.4),ylim=(0,155),xticks=yrs[::2],yticks=[0,50,100,150]);ax.grid(axis='y',alpha=.2);ax.set_ylabel('Swell energy index');ax.text(2021,144,'2021-2025',color=gray,fontsize=9);ax.annotate('135',(2018,v[7]),xytext=(0,10),textcoords='offset points',ha='center',color=teal,weight='bold');ax.annotate('54',(2025,v[-1]),xytext=(0,-18),textcoords='offset points',ha='center',color=orange,weight='bold')
fig.tight_layout();fig.savefig(F/'annual_swell_energy.png',dpi=220);fig.savefig(F/'annual_swell_energy.svg');plt.close(fig)
# Geographically accurate regional exposure illustration in WGS84 UTM 19N.
tr=Transformer.from_crs(4326,32619,always_xy=True);g=Geod(ellps='WGS84');land=transform(tr.transform,shape(json.load(open(P/'land_region.geojson'))));meta=json.load(open(P/'exposure_summary.json'));m=np.load(P/'exposure_masks.npz');dirs=m['directions']
fig,ax=plt.subplots(figsize=(5.4,4.4));ax.set_facecolor('#EDF5F7')
lon,lat=meta['sites']['Jenness_offshore']
for direction in range(0,360,15):
 dist=np.linspace(0,65000,66);lo,la,_=g.fwd(np.full(66,lon),np.full(66,lat),np.full(66,direction+.5),dist);x,y=tr.transform(lo,la)
 visible=m['Jenness_offshore_100km_buf0'][direction]>0
 ax.plot(x,y,color=teal if visible else orange,alpha=.34,lw=.8,ls='-' if visible else '--',zorder=1)
for poly in land.geoms:
 if poly.geom_type!='Polygon':continue
 x,y=poly.exterior.xy;ax.fill(x,y,color='#DFE4DE',ec='#89988C',lw=.45,zorder=2)
for name,(lon,lat) in meta['sites'].items():
 x,y=tr.transform(lon,lat);ax.scatter(x,y,s=22,color=teal,zorder=4);ax.annotate(name.split('_')[0],(x,y),xytext=(-9,6),textcoords='offset points',ha='right',fontsize=9,zorder=5)
x,y=tr.transform(-70.169,42.8);ax.scatter(x,y,marker='*',s=90,color=navy,zorder=5);ax.annotate('Jeffreys Ledge\n44098 / CDIP 160',(x,y),xytext=(7,-6),textcoords='offset points',fontsize=8,zorder=5)
for label,lon,lat in [('Cape Ann',-70.66,42.65),('Isles of Shoals',-70.62,42.97)]:
 x,y=tr.transform(lon,lat);ax.text(x,y,label,fontsize=8,zorder=5,color=navy)
x0,y0=tr.transform(-70.98,42.55);x1,y1=tr.transform(-69.95,43.22);ax.set_xlim(x0,x1);ax.set_ylim(y0,y1);ax.set_aspect('equal');ax.set_xticks([]);ax.set_yticks([])
sx,sy=x0+5500,y0+5000;ax.plot([sx,sx+20000],[sy,sy],color=navy,lw=2);ax.text(sx+10000,sy+1400,'20 km',ha='center',fontsize=8)
nx,ny=x0+5500,y1-13000;lo,la=Transformer.from_crs(32619,4326,always_xy=True).transform(nx,ny);elo,ela,_=g.fwd(lo,la,0,7000);ex,ey=tr.transform(elo,ela);ax.annotate('',xy=(ex,ey),xytext=(nx,ny),arrowprops=dict(arrowstyle='-|>',color=navy));ax.text(ex,ey+1000,'N',ha='center',fontsize=9)
fig.tight_layout(pad=.3);fig.savefig(F/'coastal_exposure.png',dpi=220);fig.savefig(F/'coastal_exposure.svg');plt.close(fig)

c=canvas.Canvas(str(O/'nh_surf_directional_report.pdf'),pagesize=(612,792));c.setTitle('New Hampshire swell: directional spectra and coastal exposure');c.setAuthor('Analysis of CDIP wave spectra and GSHHG coastline')
def text(x,y,s,size=10,color=navy,bold=False):
 c.setFillColor(HexColor(color));c.setFont('Helvetica-Bold' if bold else 'Helvetica',size);c.drawString(x,y,s)
def para(x,y,s,w=524,size=10,leading=14):
 p=Paragraph(s,ParagraphStyle('p',fontName='Helvetica',fontSize=size,leading=leading,textColor=HexColor(navy)));_,h=p.wrap(w,700);p.drawOn(c,x,y-h);return y-h
def footer(n):
 c.setStrokeColor(HexColor('#DFE8EB'));c.line(44,42,568,42);text(44,28,'NH SWELL / REVISED DIRECTIONAL ANALYSIS',7,gray);text(480,28,f'17 NOV 2026 / {n}',7,gray)
text(44,751,'SPECTRA + COASTAL EXPOSURE',9,teal,True)
text(44,722,'A clearer view of incoming swell',25,navy,True)
para(44,703,'Separating energy by both period and direction confirms a recent swell deficit, but moderates the earlier claims. These are offshore exposure estimates, not modeled beach surf heights.',size=11,leading=15)
for x,num,label in [(44,'-13%','energy in >=8-second swell'),(308,'-33%','time with H10 >3 m')]:
 text(x,632,num,29,orange,True);text(x,613,label,10,gray)
text(44,592,'2021-2025 vs. 2016-2020; equal average of three representative NH exposures.',8,gray)
text(44,568,'01  2025 remains weak; 2023-2024 were near baseline',13,navy,True)
c.drawImage(str(F/'annual_swell_energy.png'),44,365,width=524,height=183.4)
para(44,355,'Index: mean exposed >=8-second spectral energy, with 2016-2020 annual average = 100. The island-transparent sensitivity gives almost identical annual indices. Annual values use observed hours.',size=8.5,leading=11)
text(44,307,'02  Height and period together',13,navy,True)
para(44,293,'H8, H10 and H12 are equivalent significant heights calculated only from exposed energy at periods >=8, >=10 or >=12 seconds. They exclude short-period and blocked-direction energy.',size=9,leading=12)
xs=[44,236,335,430];headers=['Swell-band condition','2016-2020','2021-2025','Change']
for x,h in zip(xs,headers):text(x,250,h,9,gray,True)
for i,(label,key) in enumerate([('H8 >3 m','gt3_8'),('H10 >3 m','gt3_10'),('H12 >3 m','gt3_12'),('H12 >2 m','gt2_12')]):
 y=228-i*24;z=case[key];text(44,y,label,11);text(236,y,f"{z['old']*100:.3f}%",10);text(335,y,f"{z['new']*100:.3f}%",10);text(430,y,f"{z['change_pct']:.0f}%",11,orange,True)
para(44,140,'<b>Important revision:</b> the earlier 64% decline for >3 m / >=12 s is not a robust coastwide result. The revised H12 >3 m decline is 28% with islands blocking, versus 38% when small islands are transparent; one site increases from a tiny baseline.',size=9,leading=12)
para(44,87,'<b>Not a proven permanent trend:</b> a year-block bootstrap gives an approximate 95% interval of -35% to +10% for the five-year energy change. Exceedance uncertainty is wider. Model ranges are not confidence intervals.',size=8.5,leading=11)
footer(1);c.showPage()
text(44,751,'WHAT CHANGED / WHAT REMAINS UNCERTAIN',9,teal,True)
text(44,722,'Which directions have an open approach?',22,navy,True)
c.drawImage(str(F/'coastal_exposure.png'),44,432,width=330,height=269)
text(391,683,'Three offshore receptors',10,navy,True)
para(391,669,'Hampton, Jenness and Wallis are represented by offshore points, not exact breaks. Results average their site-specific energy or exceedance fractions.',w=177,size=9,leading=12)
text(391,590,'A land-based direction filter',10,navy,True)
para(391,576,'Solid teal rays illustrate open directions at Jenness. Dashed orange rays intersect land within 100 km. Cape Ann and the Isles of Shoals change the exposure window.',w=177,size=9,leading=12)
text(391,497,'Geographic basis',10,navy,True)
para(391,483,'GSHHG high-resolution coastline; WGS84 geodesic rays; UTM zone 19N map. Regional screening, not survey-grade shoreline geometry.',w=177,size=8,leading=11)
text(44,414,'The stronger method',12,navy,True)
para(44,397,'<b>1. Separate the sea state.</b> Reconstruct a frequency-direction spectrum from CDIP energy and four directional coefficients using maximum entropy. This retains incoming components even when outgoing waves dominate, and removes blocked-direction components from mixed seas. Directional reconstruction remains an estimate from limited angular moments. [1, 2]',size=9,leading=12)
para(44,337,'<b>2. Apply exposure and integrate.</b> Sum only good spectral bins in each period band and open direction. Convert integrated variance m0 to equivalent band height H = 4 sqrt(m0). The old total-height-plus-peak-period thresholds and the new band-height thresholds are different metrics.',size=9,leading=12)
para(44,287,'<b>3. Check sensitivity and coverage.</b> About 127,000 valid hourly records cover 2011-2025, including late 2025 from the replacement buoy. Five-year means balance calendar months and retain >=80%-complete months. Across 50-150 km rays, a 500 m land buffer, and a small-island-transparent case, regional >=8 s energy falls about 12-13%. The 2025 deficit is already present before the August buoy replacement.',size=9,leading=12)
text(44,213,'What this does not establish',12,navy,True)
para(44,196,'The buoy spectrum is assumed representative across nearby waters. Straight-line shadows do not simulate refraction, shoaling, diffraction around islands, tides, currents or breaking. These results identify potentially incoming offshore swell, not the energy or surf height actually delivered to each beach. A validated nearshore hindcast is still needed for that. No storm-track cause or permanent climate shift has been demonstrated.',size=9,leading=12)
text(44,119,'Sources and reproducibility',10,navy,True)
links=[('1. CDIP 160 spectral archive and data access','https://www.cdip.ucsd.edu/m/documents/data_access.html'),('2. Lygre & Krogstad (1986), directional maximum entropy','https://journals.ametsoc.org/view/journals/phoc/16/12/1520-0485_1986_016_2052_meeotd_2_0_co_2.xml'),('3. GSHHG 2.3.7 shoreline database','https://www.soest.hawaii.edu/pwessel/gshhs/index.html')]
for i,(label,url) in enumerate(links):
 y=103-12*i;text(44,y,label,8,teal);c.linkURL(url,(44,y-2,400,y+9),relative=0)
text(44,60,'Scripts, data coverage, validation and full caveats: research/spectral/README.md',8,gray)
footer(2);c.save();print(O/'nh_surf_directional_report.pdf')
