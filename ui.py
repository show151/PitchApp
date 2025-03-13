from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QComboBox, QWidget, QProgressBar
from PySide6.QtCore import Qt
from audio_player import play_wav
from audio_recorder import record_audio
from pitch_analysis import analyze_segments, calculate_match_rate

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("音声一致率解析アプリ")
        self.setFixedSize(600, 400)

        # メインレイアウト
        layout = QVBoxLayout()

        # 背景色と全体のスタイル設定
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f7f7f7;
            }
            QLabel {
                font-size: 16px;
                color: #333333;
            }
            QComboBox {
                font-size: 14px;
                padding: 6px;
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QProgressBar {
                border: 2px solid #555;
                border-radius: 8px;
                background-color: #eee;
                height: 30px; /* バー全体の高さ */
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50; /* プログレスバーの色（緑） */
                width: 20px; /* バーの太さ */
                margin: 1px;
            }
        """)

        # プルダウンメニュー（正解音リストとファイル名の対応）
        self.sequence_selector = QComboBox()
        self.sequences = {
            "ドレド": {"notes": ["ド", "レ", "ド"], "file": "doredo.wav"},
            "レミレ": {"notes": ["レ", "ミ", "レ"], "file": "remire.wav"},
            "ミファミ": {"notes": ["ミ", "ファ", "ミ"], "file": "mifami.wav"},
            "ファソファ": {"notes": ["ファ", "ソ", "ファ"], "file": "fasofa.wav"},
            "ソラソ": {"notes": ["ソ", "ラ", "ソ"], "file": "solaso.wav"},
            "ラシラ": {"notes": ["ラ", "シ", "ラ"], "file": "rashira.wav"},
            "シドシ": {"notes": ["シ", "ド", "シ"], "file": "shidoshi.wav"}
        }
        self.sequence_selector.addItems(list(self.sequences.keys()))
        layout.addWidget(self.sequence_selector)

        # 再生ボタン
        self.play_button = QPushButton("正解音を再生")
        self.play_button.clicked.connect(self.play_selected_sequence)
        layout.addWidget(self.play_button)

        # 録音ボタン
        self.record_button = QPushButton("録音")
        self.record_button.clicked.connect(self.record_user_audio)
        layout.addWidget(self.record_button)

        # ボタン: 解析
        self.analyze_button = QPushButton("解析開始")
        self.analyze_button.clicked.connect(self.start_analysis)
        layout.addWidget(self.analyze_button)

        # プログレスバー: 一致率表示
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)  # 0%〜100%
        self.progress_bar.setValue(0)  # 初期値
        self.progress_bar.setFormat("一致率: %p%")
        layout.addWidget(self.progress_bar)

        # 結果ラベル
        self.result_label = QLabel("結果がここに表示されます")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 1px solid #cccccc;
                padding: 10px;
                border-radius: 5px;
            }
        """)
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
        self.progress_bar.setValue(int(match_rate))
        self.result_label.setText(f"一致率: {match_rate}%\n間違い: {differences}")
      else:
        self.result_label.setText("エラー: 正解音リストが見つかりません")

