from pathlib import Path
import numpy as np,struct

def arrays(path,types):
 b=Path(path).read_bytes().split(b'\nData:\n',1)[1];pos=0;out=[]
 for typ in types:
  n=struct.unpack_from('>I',b,pos)[0];pos+=4
  n2=struct.unpack_from('>I',b,pos)[0];pos+=4
  assert n==n2,(n,n2)
  arr=np.frombuffer(b,dtype=typ,count=n,offset=pos).copy();pos+=arr.nbytes
  if typ=='u1':pos+=(4-n%4)%4
  out.append(arr)
 assert pos==len(b),(pos,len(b))
 return out
if __name__=='__main__':
 t,f,w=arrays(Path(__file__).parent/'coords.dods',['>i4','>f4','>f4'])
 print(t.astype('datetime64[s]')[[0,-1]]);print(f);print(w)
 print('2011 start',np.searchsorted(t,np.datetime64('2011-01-01').astype('datetime64[s]').astype(int)))
