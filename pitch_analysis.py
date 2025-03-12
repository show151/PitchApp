import librosa
import numpy as np
from scipy.signal import find_peaks
from collections import Counter

# 音名と周波数の対応表
note_frequencies = {
    "ド": 261.63,
    "レ": 293.66,
    "ミ": 329.63,
    "ファ": 349.23,
    "ソ": 392.00,
    "ラ": 440.00,
    "シ": 493.88
}

def analyze_segments(audio_file, segment_duration=1.0, skip_initial_seconds=1.0):
    # 音声ファイルを読み込む
    y, sr = librosa.load(audio_file)
    total_duration = len(y) / sr  # 全体の時間（秒）

    # 最初の1秒分をスキップ
    skip_samples = int(skip_initial_seconds * sr)
    if skip_samples < len(y):  # 録音データがスキップ時間以上の場合のみスキップ
        y = y[skip_samples:]
    else:
        print("エラー: 録音時間が短すぎて解析できません。")
        return []

    # 各区間を分割
    segment_samples = int(segment_duration * sr)  # 各区間のサンプル数
    segments = [y[i:i + segment_samples] for i in range(0, len(y), segment_samples)]
    
    segment_results = []

    for segment_index, segment in enumerate(segments):
        if len(segment) < segment_samples:  # 最後の区間が短い場合スキップ
            break

        # 振幅のピークを検出
        amplitude_envelope = np.abs(segment)
        peaks, _ = find_peaks(amplitude_envelope, height=0.05)
        print(f"区間 {segment_index + 1}: 検出されたピーク数: {len(peaks)}")

        # ピーク部分のピッチ解析
        pitches, magnitudes = librosa.piptrack(y=segment, sr=sr)
        detected_pitches = []
        for peak in peaks:
            frame_index = peak // (len(segment) // pitches.shape[1])
            if frame_index < pitches.shape[1]:
                index = magnitudes[:, frame_index].argmax()
                pitch = pitches[index, frame_index]
                if pitch > 0:  # ノイズを除外
                    detected_pitches.append(pitch)

        # ピッチを音名に変換
        def pitch_to_note(pitch):
            for note, freq in note_frequencies.items():
                if abs(pitch - freq) < 10:  # 許容範囲10Hz
                    return note
            return None

        detected_notes = [pitch_to_note(p) for p in detected_pitches if pitch_to_note(p)]
        print(f"区間 {segment_index + 1}: 検出された音: {detected_notes}")

        # 最頻出音を集計
        if detected_notes:
            note_counts = Counter(detected_notes)
            most_common_note = note_counts.most_common(1)[0][0]  # 最頻出の音
        else:
            most_common_note = None

        segment_results.append(most_common_note)

    print(f"各区間の最頻出音: {segment_results}")
    return segment_results


def calculate_match_rate(detected, target):
    match_count = sum([1 for d, t in zip(detected, target) if d == t])
    match_rate = (match_count / len(target)) * 100 if len(target) > 0 else 0
    differences = [(i, d, t) for i, (d, t) in enumerate(zip(detected, target)) if d != t]

    # 小数第2位までにフォーマット
    match_rate = round(match_rate, 2)
    return match_rate, differences

