import sys, sherpa_onnx, soundfile as sf
d='asr/sherpa-onnx-whisper-turbo'
r = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{d}/turbo-encoder.int8.onnx", decoder=f"{d}/turbo-decoder.int8.onnx", tokens=f"{d}/turbo-tokens.txt", language="ur", task="transcribe", num_threads=8)
a, sr = sf.read('asr/audio16k.wav', dtype='float32')
for w in sys.argv[1:]:
    s,e=map(float,w.split(':'))
    st=r.create_stream(); st.accept_waveform(sr,a[int(s*sr):int(e*sr)]); r.decode_stream(st); print(f"{s}-{e}: {st.result.text}", flush=True)
