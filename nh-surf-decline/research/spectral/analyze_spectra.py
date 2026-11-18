import json,csv,calendar
from pathlib import Path
import numpy as np
from dap_read import arrays
P=Path(__file__).parent
coords=arrays(P/'coords.dods',['>i4','>f4','>f4'])
rtcoords=arrays(P/'rt_coords.dods',['>i4','>f4','>f4'])
q=arrays(P/'quality.dods',['u1','>f4','>f4','u1'])
hist=[]
for name in ['energy','waveA1Value','waveB1Value','waveA2Value','waveB2Value']:
 a,t,f=arrays(P/f'swell_{name}.dods',['>f4','>i4','>f4']);hist.append(a.reshape(-1,len(f)).astype(float))
rt=arrays(P/'late2025_fullswell.dods',['u1','u1']+['>f4','>i4','>f4']*5)
rta=[rt[2+i*3].reshape(-1,21).astype(float) for i in range(5)]
check,ct,cf=arrays(P/'check_direction.dods',['>f4','>i4','>f4'])
ang=np.rad2deg(np.angle(hist[1][:100]+1j*hist[2][:100]))%360
err=(ang-check.reshape(100,18)+180)%360-180
print('direction angle max error degrees',np.max(np.abs(err[:,2:])),flush=True)
assert np.max(np.abs(err[:,2:]))<.01
m=np.load(P/'exposure_masks.npz');theta=m['directions'];names=[k for k in m.files if k!='directions']
mask=np.stack([m[k] for k in names],axis=1)
names+=['NE_SE','all_directions']
mask=np.column_stack((mask,((theta>=45)&(theta<=135)).astype(float),np.ones(len(theta))))
exp1=np.exp(-1j*np.deg2rad(theta));exp2=exp1**2
periods=[8,10,12]
colnames=[]
for name in names:
 for period in periods:colnames += [f'{name}:m0_{period}',f'{name}:mn1_{period}',f'{name}:gt3_{period}',f'{name}:gt2_{period}']
outs=[];times=[];validation=[]
for tag,data,tt,ff,bw,flags,freqflags in [('historic',hist,t,f,coords[2][:18],q[0],q[-1][:18]),('late2025',rta,rt[3],rt[4],rtcoords[2][:21],rt[0],rt[1][:21])]:
 goodfreq=freqflags==1
 # Exclude flagged bands and integrate partial frequency cells exactly at period limits.
 weights={per:np.clip(np.minimum(ff+bw/2,1/per)-(ff-bw/2),0,bw)*goodfreq for per in periods}
 valid=(flags==1)&np.all(np.isfinite(data[0])&(data[0]>=0),axis=1)
 for z in data[1:]:valid &= np.all(np.isfinite(z)&(np.abs(z)<=1),axis=1)
 for start in range(0,len(tt),512):
  end=min(start+512,len(tt));en,a1,b1,a2,b2=[v[start:end] for v in data]
  c1=a1+1j*b1;c2=a2+1j*b2
  phi1=(c1-c2*np.conj(c1))/np.maximum(1-abs(c1)**2,1e-10);phi2=c2-c1*phi1
  numerator=np.real(1-phi1*np.conj(c1)-phi2*np.conj(c2))
  ok=np.all(numerator[:,goodfreq]>0,axis=1)
  D=np.maximum(numerator,1e-12)[...,None]/np.maximum(abs(1-phi1[...,None]*exp1-phi2[...,None]*exp2)**2,1e-14)
  D/=D.sum(axis=-1,keepdims=True)
  # Verify moment recovery; adapt quadrature for unusually narrow spectra.
  rec1=np.sum(D*np.conj(exp1),axis=-1);rec2=np.sum(D*np.conj(exp2),axis=-1)
  errors=np.maximum(abs(rec1-c1),abs(rec2-c2))
  frac=D@mask
  bad=np.argwhere((errors>.001)&goodfreq[None,:])
  for ii,jj in bad:
   for subdivision in [10,50]:
    th=(np.arange(360*subdivision)+.5)/subdivision
    ee=np.exp(-1j*np.deg2rad(th))
    dd=max(numerator[ii,jj],1e-12)/np.maximum(abs(1-phi1[ii,jj]*ee-phi2[ii,jj]*ee**2)**2,1e-20)
    dd/=dd.sum()
    e1=abs(np.sum(dd*np.conj(ee))-c1[ii,jj]);e2=abs(np.sum(dd*np.conj(ee)**2)-c2[ii,jj])
    frac[ii,jj]=dd@np.repeat(mask,subdivision,axis=0)
    errors[ii,jj]=max(e1,e2)
    if errors[ii,jj]<.001:break
  validation.append([float(np.max(errors[:,goodfreq])),float(len(bad))])
  assert np.min(frac)>-1e-10 and np.max(frac)<1+1e-8
  vals=[]
  for k in range(len(names)):
   se=en*frac[:,:,k]
   for per in periods:
    energy=se@weights[per]
    mn1=se@(weights[per]/ff)
    vals.extend([energy,mn1,(energy>9/16).astype(float),(energy>4/16).astype(float)])
  out=np.stack(vals,axis=1)
  keep=valid[start:end]&ok
  outs.append(out[keep]);times.append(tt[start:end][keep])
  if start%16384==0:print(tag,start,'/',len(tt),flush=True)
print('moment max errors',np.max(validation,axis=0),flush=True)
X=np.concatenate(outs);times=np.concatenate(times).astype('int64');order=np.argsort(times);X=X[order];times=times[order]
# Equalize temporal weighting by averaging any repeated UTC-hour records.
hours=times//3600;unique,ix,count=np.unique(hours,return_index=True,return_counts=True)
X=np.add.reduceat(X,ix,axis=0)/count[:,None]
np.savez_compressed(P/'hourly_metrics.npz',hours=unique,values=X,columns=np.array(colnames))
monthly=[];annual=[]
dates=(unique*3600).astype('datetime64[s]');months=dates.astype('datetime64[M]')
for mon in np.unique(months):
 y,mo=map(int,str(mon).split('-'));ii=months==mon;row=dict(year=y,month=mo,hours=int(ii.sum()),coverage=float(ii.sum()/(calendar.monthrange(y,mo)[1]*24)))
 row.update(zip(colnames,np.mean(X[ii],axis=0)));monthly.append(row)
for y in range(2011,2026):
 ii=dates.astype('datetime64[Y]')==np.datetime64(str(y));row=dict(year=y,hours=int(ii.sum()),coverage=float(ii.sum()/(8784 if calendar.isleap(y) else 8760)))
 row.update(zip(colnames,np.mean(X[ii],axis=0)));annual.append(row)
for name,rows in [('monthly',monthly),('annual',annual)]:
 with open(P/f'{name}_metrics.csv','w') as f1:
  w=csv.DictWriter(f1,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summaries={}
for cutoff in [.7,.8,.9]:
 summaries[str(cutoff)]={}
 for lo,hi in [(2011,2020),(2016,2020),(2021,2025)]:
  rows=[r for r in monthly if lo<=r['year']<=hi and r['coverage']>=cutoff]
  vals={k:float(np.mean([np.mean([r[k] for r in rows if r['month']==mo]) for mo in range(1,13)])) for k in colnames}
  summaries[str(cutoff)][f'{lo}-{hi}']=dict(months=len(rows),metrics=vals)
(P/'summary.json').write_text(json.dumps(summaries,indent=2))
(P/'validation.json').write_text(json.dumps(dict(direction_max_error_degrees=float(np.max(abs(err[:,2:]))),moment_max_error=float(np.max(np.array(validation)[:,0])),refined_bands=int(np.sum(np.array(validation)[:,1])),valid_hours=len(unique),sample_stride=2,direction_step_degrees=1),indent=2))
print('COMPLETE',len(unique),'hours',flush=True)
