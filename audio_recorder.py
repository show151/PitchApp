import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(filename, duration=4.0, fs=44100):
    print("録音を開始します...")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("録音が終了しました。")
    write(filename, fs, audio_data)
    print(f"音声が保存されました: {filename}")
