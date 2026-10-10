import subprocess, sys, numpy as np
from scipy import ndimage
raw, matte, out, n = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv)>4 else 0
W,H=1080,1920
fr=lambda args: subprocess.Popen(['ffmpeg','-v','error']+args+['-f','rawvideo','-'],stdout=subprocess.PIPE,bufsize=10**8)
pr=fr(['-i',raw,'-pix_fmt','rgb24'])
pm=fr(['-i',matte,'-vf','format=yuva444p,alphaextract','-pix_fmt','gray'])
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgba','-s',f'{W}x{H}','-r','30','-i','-']+
   (['-frames:v',str(n),'-c:v','png','-f','image2',out] if out.endswith('.png') else
    ['-vf','unsharp=5:5:0.35:5:5:0','-c:v','libvpx-vp9','-pix_fmt','yuva420p','-b:v','0','-crf','18','-row-mt','1','-deadline','good','-cpu-used','4','-auto-alt-ref','0',out]),stdin=subprocess.PIPE)
PL=np.load(sys.argv[5]) if len(sys.argv)>5 else None
if PL is not None:
    GD=PL[...,1]-np.maximum(PL[...,0],PL[...,2]); USE=GD>35
i=0
while True:
    b=pr.stdout.read(W*H*3); m=pm.stdout.read(W*H)
    if len(b)<W*H*3 or len(m)<W*H: break
    rgb=np.frombuffer(b,np.uint8).reshape(H,W,3).astype(np.float32)
    ai=np.frombuffer(m,np.uint8).reshape(H,W).astype(np.float32)/255
    r,g,bl=rgb[...,0],rgb[...,1],rgb[...,2]
    green=g-np.maximum(r,bl)
    key=np.clip(1-(green-12)/38,0,1)
    if PL is not None:
        ak=np.clip(1-(green-4)/np.maximum(GD-4,1)*1.1,0,1)
        key=np.where(USE,np.minimum(key,ak),key)
        aa=np.maximum(ak,0.2)[...,None]
        F=(rgb-(1-aa)*PL)/aa
        um=(USE&(ak<0.98)&(ak>0.02))[...,None]
        rgb=np.where(um,np.clip(F,0,255),rgb)
        r,g,bl=rgb[...,0],rgb[...,1],rgb[...,2]
    mx=np.maximum(np.maximum(r,g),bl); mn=np.minimum(np.minimum(r,g),bl)
    lum=0.3*r+0.59*g+0.11*bl
    wall=np.clip((lum-95)/45,0,1)*np.clip((42-(mx-mn))/22,0,1)
    yy=np.arange(H,dtype=np.float32)[:,None]
    wall=wall*np.clip((470-yy)/60,0,1)
    a=np.minimum(ai,key)*(1-wall)
    a=ndimage.grey_erosion(a,size=(3,3))
    a=ndimage.gaussian_filter(a,0.9)
    # despill
    lim=np.maximum(r,bl)*0.98+4
    g2=np.where(g>lim,lim,g)
    rgb[...,1]=g2
    inner=(a>0.985).astype(np.float32)
    inner=ndimage.grey_erosion(inner,size=(5,5))
    den=ndimage.gaussian_filter(inner,5)+1e-4
    est=np.dstack([ndimage.gaussian_filter(rgb[...,c]*inner,5)/den for c in range(3)])
    w=np.clip((0.985-a)/0.4+ (1-inner)*0.6,0,1)[...,None]
    w=np.where(den[...,None]>0.02,w,0)
    rgb=rgb*(1-w)+est*w
    x=np.clip(rgb/255,0,1)*1.05
    x=np.clip(x,0,1)
    x=x+0.35*x*(1-x)*(x-0.42)          # gentle S-curve, keeps shadows open
    x[...,0]*=1.025; x[...,2]*=0.965      # slight warmth, removes green-screen cast
    l=(0.3*x[...,0]+0.59*x[...,1]+0.11*x[...,2])[...,None]
    x=l+(x-l)*1.06
    rgb=np.clip(x,0,1)*255
    o=np.dstack([np.clip(rgb,0,255),a[...,None]*255]).astype(np.uint8)
    enc.stdin.write(o.tobytes()); i+=1
    if n and i>=n: break
enc.stdin.close(); enc.wait(); print("frames",i)
