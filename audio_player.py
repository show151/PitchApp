import simpleaudio as sa
import os

# オーディオファイルのパス
AUDIO_DIR = "./audio/"

def play_wav(filename):
    """指定されたWAVファイルを再生する"""
    filepath = os.path.join(AUDIO_DIR, filename)
    if not os.path.exists(filepath):
        print(f"ファイルが見つかりません: {filepath}")
        return
    wave_obj = sa.WaveObject.from_wave_file(filepath)
    play_obj = wave_obj.play()
    play_obj.wait_done()
