from pathlib import Path
import csv,json
from statistics import mean
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,Color
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
P=Path(__file__).parent; OUT=P.parent/'output/pdf/nh_surf_wave_report.pdf'
annual=[{k:float(v) for k,v in r.items()} for r in csv.DictReader(open(P/'ndbc_energy_annual.csv'))]
a={};active=False
for l in open(P/'height_period_results.txt'):
 if l.startswith('CUTOFF'):active=l.strip()=='CUTOFF 0.8'
 elif active and l[:4].isdigit():
  start,end,j=l.split(' ',2);a[start+'-'+end]=json.loads(j)
old,new=a['2016-2020'],a['2021-2025']
navy='#153449';teal='#167F86';orange='#C45B36';gray='#566875';light='#DFE8EB';bg='#F4F7F7'
c=canvas.Canvas(str(OUT),pagesize=(612,792));c.setTitle('New Hampshire surf: fewer large, long-period conditions');c.setAuthor('Research analysis of NOAA NDBC buoy records')
def text(x,y,s,size=10,color=navy,bold=False):
 c.setFillColor(HexColor(color));c.setFont('Helvetica-Bold' if bold else 'Helvetica',size);c.drawString(x,y,s)
def para(x,y,s,w=512,size=10,leading=14,color=navy):
 p=Paragraph(s,ParagraphStyle('p',fontName='Helvetica',fontSize=size,leading=leading,textColor=HexColor(color)));_,h=p.wrap(w,700);p.drawOn(c,x,y-h);return y-h

def line(x1,y1,x2,y2,color=light,width=1):
 c.setStrokeColor(HexColor(color));c.setLineWidth(width);c.line(x1,y1,x2,y2)
def dot(x,y,color,r=3):
 c.setFillColor(HexColor(color));c.circle(x,y,r,stroke=0,fill=1)
def footer(n):
 line(44,43,568,43);text(44,28,'NH COAST  /  PRELIMINARY OBSERVATIONAL STUDY',7,gray);text(481,28,f'16 NOV 2026  /  {n}',7,gray)
def annual_plot(y,h,values,low,high,ticks,label,fmt):
 x=75;w=466
 c.setFillColor(HexColor(bg));c.rect(x+9.5*w/14,y,4.5*w/14,h,fill=1,stroke=0)
 for v in ticks:
  yy=y+(v-low)/(high-low)*h;line(x,yy,x+w,yy);text(44,yy-3,fmt(v),8,gray)
 for i,r in enumerate(annual):
  xx=x+i*w/14
  if i%2==0:text(xx-10,y-17,str(int(r['year'])),8,gray)
  yy=y+(values[i]-low)/(high-low)*h
  if i:line(prev[0],prev[1],xx,yy,teal,2)
  dot(xx,yy,orange if i==14 else teal,3.5);prev=(xx,yy)
 text(x,y+h+10,label,8,gray)
 text(x+9.5*w/14+8,y+h-13,'2021-2025',8,gray)
 return x,w

text(44,752,'NEW HAMPSHIRE / WAVE CLIMATE',9,teal,True)
text(44,720,'Fewer large, long-period conditions',24,navy,True)
para(44,702,'An offshore buoy check supports a shortage of stronger incoming conditions. Average peak period barely changed; the biggest losses occurred when large height and long period coincided.',size=11,leading=15)
for x,num,desc in [(44,'-19%','screened energy content'),(220,'-37%','time >3 m and >=10 s'),(396,'-64%','time >3 m and >=12 s')]:
 text(x,628,num,27,orange,True);text(x,610,desc,9,gray)
text(44,590,'2021-2025 versus 2016-2020; calendar-month-balanced estimates.',8,gray)
text(44,562,'01  Energy varied; 2025 was exceptionally weak',13,navy,True)
vals=[r['energy_index'] for r in annual]
x,w=annual_plot(376,156,vals,0,150,[0,50,100,150],'Direction-screened energy index (2016-2020 annual mean = 100)',lambda v:str(v))
ybase=376+100/150*156
c.setDash(4,3);line(x,ybase,x+w,ybase,gray,1);c.setDash()
text(x+7*w/14-8,376+vals[7]/150*156+12,'128',10,teal,True)
text(x+w-8,376+vals[-1]/150*156-20,'59',11,orange,True)
para(44,345,'2018 was unusually energetic. Overall energy returned near baseline in 2023-2024, while 2025 fell to 59. This is not a uniform five-year collapse.',size=9,leading=12)
text(44,301,'02  Height and period together reveal the largest losses',13,navy,True)
text(245,280,'2016-2020',9,teal,True);text(354,280,'2021-2025',9,orange,True)
xx=246;ww=225;y0=127;hh=128
for v in range(5):
 xp=xx+v/4*ww;line(xp,y0,xp,y0+hh);text(xp-5,y0-14,f'{v}%',8,gray)
for i,(label,k) in enumerate([('>3 m + >=8 seconds','h3_t8'),('>3 m + >=10 seconds','h3_t10'),('>3 m + >=12 seconds','h3_t12'),('>2 m + >=12 seconds','h2_t12')]):
 yy=246-i*35;ov=old[k]*100;nv=new[k]*100
 text(44,yy-3,label,10)
 xo=xx+ov/4*ww;xn=xx+nv/4*ww;line(xn,yy,xo,yy,gray,2);dot(xo,yy,teal,4);dot(xn,yy,orange,4)
 text(xn-10,yy-14,f'{nv:.2f}',7,orange);text(xo-8,yy+9,f'{ov:.2f}',7,teal)
 text(498,yy-4,f'{100*(nv/ov-1):.0f}%',12,orange,True)
text(246,95,'Share of observed time meeting both thresholds',8,gray)
para(44,80,'All figures: Jeffreys Ledge buoy 44098, dominant waves FROM NE-SE (45-135 degrees). Offshore significant height is not beach surf height. Sources and limitations on page 2.',size=8,leading=10)
footer(1);c.showPage()
text(44,752,'INTERPRETATION / METHODS',9,teal,True)
text(44,720,'Period alone does not explain the decline',22,navy,True)
text(44,682,'03  Incoming peak periods remained broadly similar',13,navy,True)
annual_plot(508,139,[r['mean_incoming_peak_period_s'] for r in annual],8.4,9.6,[8.4,8.8,9.2,9.6],'Annual mean peak period when dominant direction is NE-SE (seconds)',lambda v:f'{v:.1f}')
para(44,473,'<b>Five-year averages: 9.11 seconds -> 9.08 seconds.</b> Incoming periods >=10 seconds occurred slightly more often overall (17.46% -> 17.80% of time), yet >3 m waves with those periods became 37% less common. The deficit is in the combination of height and period.',size=10,leading=14)
text(44,406,'What the record supports',12,navy,True)
para(44,389,'Large, long-period conditions became scarcer after the active 2018 season. The broader energy record rebounded in 2023-2024; 2025 is the clearest weak year. A single permanent change date is not established. Storm strength, track and fetch are plausible mechanisms, but this analysis does not attribute a cause.',size=10,leading=14)
text(44,319,'How the figures were calculated',12,navy,True)
para(44,302,'<b>Data:</b> NOAA NDBC annual standard meteorological archives, 44098, 2011-2025. Complete calendar years only; 2026 is excluded. Valid observations are averaged within each UTC hour. Annual figures use available hours; annual coverage ranges from 81% to nearly 100%.',size=9,leading=12)
para(44,250,'<b>Energy:</b> NDBC defines significant height Hs = 4 sqrt(m0). Integrated spectral variance is therefore inferred per observation as m0 = Hs squared / 16. Figure 1 averages this quantity with a NE-SE direction screen, assigning zero outside that sector. It is not the previous height-squared-times-period power proxy. The index is our normalization, not an official NDBC product. [1, 2]',size=9,leading=12)
para(44,187,'<b>Comparisons and limits:</b> Five-year estimates retain months with >=80% valid hourly coverage and weight calendar months equally. Annual plots are not gap-filled and use a different weighting. Peak direction screens total wave height; mixed incoming/outgoing seas are not partitioned. No nearshore refraction, sheltering or beach transformation is modeled. Rare thresholds are sensitive to individual storms; no trend significance or causal attribution is claimed.',size=9,leading=12)
text(44,113,'Sources and reproducibility',10,navy,True)
links=[('1. NDBC wave calculations','https://www.ndbc.noaa.gov/faq/wavecalc.shtml'),('2. NDBC measurement definitions','https://www.ndbc.noaa.gov/faq/measdes.shtml'),('3. NDBC historical data archive','https://www.ndbc.noaa.gov/data/historical/stdmet/')]
for i,(label,url) in enumerate(links):
 yy=98-i*12;text(44,yy,label,8,teal);c.linkURL(url,(44,yy-2,300,yy+9),relative=0)
text(316,98,'Reproducible scripts and data:',8,gray);text(316,86,'research/README.md in this chat folder',8,gray)
footer(2);c.save()
print(OUT)
