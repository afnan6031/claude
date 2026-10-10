import sys, json, sherpa_onnx, soundfile as sf, numpy as np
d='asr/sherpa-onnx-whisper-turbo'
r = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{d}/turbo-encoder.int8.onnx", decoder=f"{d}/turbo-decoder.int8.onnx", tokens=f"{d}/turbo-tokens.txt", language="ur", task="transcribe", num_threads=8, tail_paddings=8000)
a, sr = sf.read('asr/audio16k.wav', dtype='float32')
pauses=[(2.24,2.38),(5.54,5.69),(7.23,7.41),(8.33,8.56),(10.70,10.92),(12.42,12.63),(14.46,14.83),(16.98,17.07),(18.57,18.88),(20.81,21.04),(24.40,24.57),(27.09,27.22),(28.79,28.88),(32.46,32.62),(34.94,35.15),(38.30,38.43),(40.45,40.65),(42.97,43.27)]
cuts=[0.0]+[(s+e)/2 for s,e in pauses]+[len(a)/sr]
out=[]
for s,e in zip(cuts,cuts[1:]):
    st=r.create_stream(); st.accept_waveform(sr,np.concatenate([a[int(s*sr):int(e*sr)],np.zeros(2*sr,dtype="float32")])); r.decode_stream(st)
    t=st.result.text.strip(); out.append({"start":round(s,2),"end":round(e,2),"text":t}); print(f"{s:5.2f}-{e:5.2f} {t}", flush=True)
json.dump(out,open('asr/segments.json','w'),ensure_ascii=False,indent=1)
