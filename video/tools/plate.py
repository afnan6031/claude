import subprocess, numpy as np, sys
from scipy import ndimage
W,H=1080,1920; raw,matte,out=sys.argv[1:4]
def frames(args,ch):
    p=subprocess.Popen(['ffmpeg','-v','error']+args+['-f','rawvideo','-'],stdout=subprocess.PIPE)
    while True:
        b=p.stdout.read(W*H*ch)
        if len(b)<W*H*ch: break
        yield np.frombuffer(b,np.uint8).reshape(H,W,ch) if ch>1 else np.frombuffer(b,np.uint8).reshape(H,W)
R=frames(['-i',raw,'-vf','select=not(mod(n\\,22))','-vsync','0','-pix_fmt','rgb24'],3)
M=frames(['-i',matte,'-vf','select=not(mod(n\\,22)),format=yuva444p,alphaextract','-vsync','0','-pix_fmt','gray'],1)
stack=[]
for r,m in zip(R,M):
    mm=ndimage.grey_dilation(m,size=(25,25))  # stay clear of the subject
    f=r.astype(np.float32); f[mm>8]=np.nan; stack.append(f)
st=np.stack(stack); print("frames",len(stack))
plate=np.nanmedian(st,axis=0)
known=~np.isnan(plate[...,0]); print("known",known.mean())
p=np.nan_to_num(plate); k=known.astype(np.float32)
for s in (6,20,60,160):
    den=ndimage.gaussian_filter(k,s)
    fill=np.dstack([ndimage.gaussian_filter(p[...,c]*k,s) for c in range(3)])/(den[...,None]+1e-6)
    mask=(~known)&(den>1e-3)
    p[mask]=fill[mask]; k[mask]=1; known=k>0
np.save(out,p.astype(np.float32))
import imageio.v3 as iio
