from pathlib import Path
import subprocess, time
p=Path(__file__).resolve().parent
for i,u in enumerate((p/'urls.txt').read_text().splitlines()):
 f=p/f'chunk{i:02}.nc'
 if f.exists() and f.stat().st_size>1000:continue
 print(i,u,flush=True)
 subprocess.run(['curl','-g','-sSL','--fail','--retry','2','--retry-delay','3','--max-time','90',u,'-o',str(f)],check=True)
 print(f.name,f.stat().st_size,flush=True)
