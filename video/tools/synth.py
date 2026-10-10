import numpy as np, soundfile as sf, sys
from scipy import signal
SR=48000; out=sys.argv[1]; rng=np.random.default_rng(7)
def env(n,a,d):  # attack/decay seconds, exp decay
    t=np.arange(n)/SR; e=np.minimum(t/max(a,1e-4),1)*np.exp(-np.maximum(t-a,0)/d); return e
def norm(x,peak=0.8): return x/np.max(np.abs(x))*peak
def st(x,w=0.0): return np.stack([x*(1-w),x*(1+w)],1)
def save(n,x): sf.write(f"{out}/{n}.wav",x.astype(np.float32),SR)
# whoosh: noise through sweeping bandpass, swelled envelope
def whoosh(dur=0.7,f0=300,f1=2600,peak=0.5):
    n=int(dur*SR); x=rng.standard_normal(n); y=np.zeros(n); blk=256
    zi=None
    for i in range(0,n,blk):
        p=i/n; f=f0*(f1/f0)**(np.sin(p*np.pi/2))
        b,a=signal.butter(2,[f*0.6/(SR/2),min(f*1.6/(SR/2),0.99)],'band')
        seg,_=signal.lfilter(b,a,x[i:i+blk],zi=np.zeros(4) if zi is None else zi); zi=_; y[i:i+blk]=seg
    t=np.linspace(0,1,n); e=np.sin(np.pi*t**0.8)**2
    y=norm(y*e,peak); L=y; R=np.roll(y,int(0.004*SR))
    pan=np.linspace(-0.6,0.6,n); return np.stack([L*(1-pan)/1.6,R*(1+pan)/1.6],1)
save("whoosh",whoosh()); save("whoosh_soft",whoosh(0.55,500,3200,0.32))
# soft UI click
n=int(0.08*SR); t=np.arange(n)/SR
c=(np.sin(2*np.pi*2400*t)*0.6+np.sin(2*np.pi*4100*t)*0.3)*env(n,0.0008,0.012)
save("click",st(norm(c,0.35)))
# notification ping (two partials, soft)
n=int(0.9*SR); t=np.arange(n)/SR
p=(np.sin(2*np.pi*1318.5*t)*env(n,0.004,0.28)+0.5*np.sin(2*np.pi*1975.5*t)*env(n,0.004,0.18)+0.25*np.sin(2*np.pi*2637*t)*env(n,0.002,0.08))
save("ping",st(norm(p,0.3),0.1))
# cinematic low impact: pitch-dropping sine + filtered noise thump
n=int(2.2*SR); t=np.arange(n)/SR
f=38+60*np.exp(-t*9); ph=2*np.pi*np.cumsum(f)/SR
sub=np.sin(ph)*env(n,0.005,0.55)
b,a=signal.butter(2,900/(SR/2)); thump=signal.lfilter(b,a,rng.standard_normal(n))*env(n,0.002,0.09)
imp=norm(sub+0.35*norm(thump),0.85); save("impact",st(imp))
# earthquake rumble: lowpassed noise with slow tremor modulation
n=int(3.2*SR); t=np.arange(n)/SR
b,a=signal.butter(3,110/(SR/2)); r=signal.lfilter(b,a,rng.standard_normal(n))
r*= (0.6+0.4*np.sin(2*np.pi*7*t))*(0.7+0.3*np.sin(2*np.pi*2.3*t))
e=np.minimum(t/0.25,1)*np.exp(-np.maximum(t-0.6,0)/0.9)
save("rumble",st(norm(r*e,0.7)))
# riser (short, for hook)
n=int(1.2*SR); t=np.arange(n)/SR
b,a=signal.butter(2,[1500/(SR/2),9000/(SR/2)],'band'); rs=signal.lfilter(b,a,rng.standard_normal(n))*(t/1.2)**2.2
save("riser",st(norm(rs,0.22)))
# ambient music bed: soft detuned pads, Dm - Bb - F - C, 4s each, plus gentle sub pulse
dur=46.5; n=int(dur*SR); t=np.arange(n)/SR
chords=[[50,57,62,65,69],[46,53,58,62,65],[41,48,57,60,65],[48,55,60,64,67]]
mtof=lambda m:440*2**((m-69)/12)
pad=np.zeros(n); seg=4.0
for k in range(int(np.ceil(dur/seg))+1):
    s=int(k*seg*SR); e2=min(n,int((k+1)*seg*SR+1.5*SR))
    if s>=n: break
    tt=np.arange(e2-s)/SR; L=len(tt)
    ce=np.minimum(tt/1.2,1)*np.minimum(np.maximum((L/SR-tt)/1.5,0),1)
    for m in chords[k%4]:
        for d in (-0.07,0.0,0.06):
            fr=mtof(m)*2**(d/12)
            pad[s:e2]+=np.sin(2*np.pi*fr*tt+rng.uniform(0,6))*ce*(0.6 if m<50 else 0.35)
b,a=signal.butter(2,1800/(SR/2)); pad=signal.lfilter(b,a,pad)
# soft pulse (eighth-note shimmer) at 96bpm
beat=60/96/2; pulse=np.zeros(n)
for k in range(int(dur/beat)):
    s=int(k*beat*SR); L=int(0.25*SR); tt=np.arange(L)/SR
    if s+L>n: break
    m=[74,77,81,79][(k//8)%4]
    pulse[s:s+L]+=np.sin(2*np.pi*mtof(m)*tt)*np.exp(-tt/0.07)*(1.0 if k%2==0 else 0.55)
sub=np.zeros(n)
for k in range(int(dur/(beat*2))):
    s=int(k*beat*2*SR); L=int(0.4*SR); tt=np.arange(L)/SR
    if s+L>n: break
    sub[s:s+L]+=np.sin(2*np.pi*mtof([38,34,41,36][int(k*beat*2/seg)%4])*tt)*np.exp(-tt/0.18)
mix=norm(pad,1)*0.55+norm(pulse,1)*0.16+norm(sub,1)*0.3
fade=np.minimum(t/2.0,1)*np.minimum(np.maximum((dur-t)/3.0,0),1)
mix=norm(mix*fade,0.7)
L=mix; R=np.roll(mix,int(0.011*SR))*0.96+0.04*L
save("music_bed",np.stack([L,R],1))
print("ok")
