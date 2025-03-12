from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QComboBox, QWidget
from PySide6.QtCore import Qt
from audio_player import play_wav
from audio_recorder import record_audio
from pitch_analysis import analyze_segments, calculate_match_rate

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("音声一致率解析アプリ")
        self.setGeometry(100, 100, 400, 300)

        # メインレイアウト
        layout = QVBoxLayout()

        # プルダウンメニュー（正解音リストとファイル名の対応）
        self.sequence_selector = QComboBox()
        self.sequences = {
            "ドレド": {"notes": ["ド", "レ", "ド"], "file": "doredo.wav"},
            "レミレ": {"notes": ["レ", "ミ", "レ"], "file": "remire.wav"},
            "ミファミ": {"notes": ["ミ", "ファ", "ミ"], "file": "mifami.wav"},
            "ファソファ": {"notes": ["ファ", "ソ", "ファ"], "file": "fasofa.wav"},
            "ソラソ": {"notes": ["ソ", "ラ", "ソ"], "file": "soraso.wav"},
            "ラシラ": {"notes": ["ラ", "シ", "ラ"], "file": "rashira.wav"},
            "シドシ": {"notes": ["シ", "ド", "シ"], "file": "shidoshi.wav"},
            "ドシド": {"notes": ["ド", "シ", "ド"], "file": "doshido.wav"}
        }
        self.sequence_selector.addItems(self.sequences.keys())
        layout.addWidget(self.sequence_selector)

        # 再生ボタン
        self.play_button = QPushButton("正解音を再生")
        self.play_button.clicked.connect(self.play_selected_sequence)
        layout.addWidget(self.play_button)

        # 録音ボタン
        self.record_button = QPushButton("録音")
        self.record_button.clicked.connect(self.record_user_audio)
        layout.addWidget(self.record_button)

        # 解析ボタン
        self.analyze_button = QPushButton("解析開始")
        self.analyze_button.clicked.connect(self.start_analysis)
        layout.addWidget(self.analyze_button)

        # 結果ラベル
        self.result_label = QLabel("結果がここに表示されます")
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)

        # ウィジェット設定
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def play_selected_sequence(self):
        """選択された正解音を再生"""
        selected_sequence = self.sequence_selector.currentText()
        sequence_data = self.sequences.get(selected_sequence)
        if sequence_data and "file" in sequence_data:
            play_wav(sequence_data["file"])
        else:
            print("エラー: ファイルが見つかりません")

    def record_user_audio(self):
        self.result_label.setText("録音中...")
        record_audio("user_audio.wav")
        self.result_label.setText("録音が完了しました。")

    def start_analysis(self):
      """録音データを解析して一致率を計算"""
      selected_sequence = self.sequence_selector.currentText()
      sequence_data = self.sequences.get(selected_sequence)
      if sequence_data and "notes" in sequence_data:
        correct_notes = sequence_data["notes"]
        detected_notes = analyze_segments("user_audio.wav", skip_initial_seconds=1.0)  # 最初の1秒を無視
        match_rate, differences = calculate_match_rate(detected_notes, correct_notes)
        self.result_label.setText(f"一致率: {match_rate}%\n間違い: {differences}")
      else:
        self.result_label.setText("エラー: 正解音リストが見つかりません")

