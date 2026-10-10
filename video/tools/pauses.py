import sys, soundfile as sf, numpy as np
a, sr = sf.read(sys.argv[1], dtype='float32')
hop = sr//100  # 10ms
rms = np.array([np.sqrt(np.mean(a[i:i+hop*2]**2)) for i in range(0, len(a)-hop*2, hop)])
db = 20*np.log10(rms+1e-9)
thr = np.percentile(db, 18)
print("thr", round(thr,1), "p50", round(np.percentile(db,50),1))
low = db < thr
runs=[]; i=0
while i < len(low):
    if low[i]:
        j=i
        while j<len(low) and low[j]: j+=1
        if j-i >= 9: runs.append((i/100, j/100))
        i=j
    else: i+=1
for s,e in runs: print(f"{s:.2f}-{e:.2f} ({e-s:.2f})")
