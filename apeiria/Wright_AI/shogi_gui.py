from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QMessageBox, QComboBox
from PyQt5.QtCore import Qt, QTimer
from ai_engine_wrapper import AIEngineWrapper
import shogi
import sys
from collections import Counter
from datetime import datetime

class ShogiBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("将棋盤 - 常駐AI")
        self.board = shogi.Board()
        self.selected = None
        self.selected_hand_piece = None
        self.ai_color = shogi.WHITE
        self.ai = AIEngineWrapper()

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.color_select = QComboBox()
        self.color_select.addItems(["あなたが先手", "あなたが後手"])
        self.color_select.currentIndexChanged.connect(self.set_ai_color)
        self.main_layout.addWidget(self.color_select)

        self.sente_hand_label = QLabel("先手の持ち駒:")
        self.sente_hand_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.sente_hand_label)
        self.sente_hand_layout = QHBoxLayout()
        self.main_layout.addLayout(self.sente_hand_layout)

        self.grid = QGridLayout()
        self.main_layout.addLayout(self.grid)

        self.gote_hand_label = QLabel("後手の持ち駒:")
        self.gote_hand_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.gote_hand_label)
        self.gote_hand_layout = QHBoxLayout()
        self.main_layout.addLayout(self.gote_hand_layout)

        self.buttons = [[QPushButton() for _ in range(9)] for _ in range(9)]
        self.init_board()

        self.quit_button = QPushButton("終了")
        self.quit_button.clicked.connect(self.close)
        self.main_layout.addWidget(self.quit_button)

        self.chat_label = QLabel("チャットログ：")
        self.main_layout.addWidget(self.chat_label)
        self.ai_vs_ai = False  # ← これをフラグとして追加
        self.ai_vs_ai_button = QPushButton("AI同士で対局")
        self.ai_vs_ai_button.clicked.connect(self.toggle_ai_vs_ai)
        self.main_layout.addWidget(self.ai_vs_ai_button)


        self.ai_board_logfile = "ai_board.log"
        self.actual_board_logfile = "actual_board.log"

    def closeEvent(self, event):
        self.ai.quit()
        event.accept()

    def set_ai_color(self, index):
        self.ai_color = shogi.BLACK if index == 1 else shogi.WHITE
        print("AIは", "先手" if self.ai_color == shogi.BLACK else "後手")
        if self.board.turn == self.ai_color:
            QTimer.singleShot(100, self.evaluate_bestmove)

    def init_board(self):
        for col in range(9):
            col_label = QLabel(str(9 - col))
            col_label.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(col_label, 0, col + 1)

        for row in range(9):
            row_label = QLabel(chr(ord('a') + row))
            row_label.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(row_label, row + 1, 0)

        for row in range(9):
            for col in range(9):
                btn = self.buttons[row][col]
                btn.setFixedSize(60, 60)
                btn.clicked.connect(lambda _, r=row, c=col: self.cell_clicked(r, c))
                self.grid.addWidget(btn, row + 1, col + 1)

        self.update_board()

    def update_board(self):
        
        for row in range(9):
            for col in range(9):
                sq = shogi.SQUARES[(8 - row) * 9 + (8 - col)]
                piece = self.board.piece_at(sq)
                btn = self.buttons[row][col]
                if piece:
                    btn.setText(self.unicode_piece(piece))
                    color = "lightblue" if piece.color == shogi.BLACK else "lightpink"
                    btn.setStyleSheet(f"background-color: {color}")
                else:
                    btn.setText("")
                    btn.setStyleSheet("")

        self.sente_hand_label.setText("先手の持ち駒: " + self.format_hand_pieces(shogi.BLACK))
        self.gote_hand_label.setText("後手の持ち駒: " + self.format_hand_pieces(shogi.WHITE))
        # print(self.board) 
        write_log("actual_board.log", "実盤面", self.board)
        self.update_hand_buttons()

    def update_hand_buttons(self):
        # 先手の持ち駒
        for i in reversed(range(self.sente_hand_layout.count())):
            self.sente_hand_layout.itemAt(i).widget().deleteLater()
        for p in self.board.pieces_in_hand[shogi.BLACK]:
            count = self.board.pieces_in_hand[shogi.BLACK][p]
            symbol = shogi.PIECE_SYMBOLS[p]  # ← 数値から 'P', 'B', などに変換
            btn = QPushButton(f"{self.unicode_piece(shogi.Piece.from_symbol(symbol))}×{count}")
            btn.clicked.connect(lambda _, s=symbol: self.select_hand_piece(shogi.BLACK, s))
            self.sente_hand_layout.addWidget(btn)

        # 後手の持ち駒
        for i in reversed(range(self.gote_hand_layout.count())):
            self.gote_hand_layout.itemAt(i).widget().deleteLater()
        for p in self.board.pieces_in_hand[shogi.WHITE]:
            count = self.board.pieces_in_hand[shogi.WHITE][p]
            symbol = shogi.PIECE_SYMBOLS[p]
            btn = QPushButton(f"{self.unicode_piece(shogi.Piece.from_symbol(symbol))}×{count}")
            btn.clicked.connect(lambda _, s=symbol: self.select_hand_piece(shogi.WHITE, s))
            self.gote_hand_layout.addWidget(btn)

    def select_hand_piece(self, color, piece):
        if color == self.board.turn:
            self.selected_hand_piece = piece.upper()  # ← ここで大文字に！
            self.selected = None


    def unicode_piece(self, piece):
        if not piece:
            return ""
        return {
            'P': '歩', 'L': '香', 'N': '桂', 'S': '銀', 'G': '金',
            'B': '角', 'R': '飛', 'K': '玉',
            '+P': 'と', '+L': '成香', '+N': '成桂', '+S': '成銀',
            '+B': '馬', '+R': '龍',
            'p': '歩', 'l': '香', 'n': '桂', 's': '銀', 'g': '金',
            'b': '角', 'r': '飛', 'k': '玉',
            '+p': 'と', '+l': '成香', '+n': '成桂', '+s': '成銀',
            '+b': '馬', '+r': '龍',
        }.get(piece.symbol(), '?')

    def format_hand_pieces(self, color):
        counter = Counter(self.board.pieces_in_hand[color])
        return ' '.join(f"{p}×{n}" for p, n in counter.items())
    def cell_clicked(self, row, col):
        if self.ai_vs_ai:
            print("⚠️ AI対AIモード中は手動操作できません。")
            return

        if self.board.turn == self.ai_color:
            print("⚠️ AIの手番です。あなたは指せません。")
            return

        sq_index = shogi.SQUARES[(8 - row) * 9 + (8 - col)]
        square_str = shogi.SQUARE_NAMES[sq_index]

        # 打ち駒の場合
        if self.selected_hand_piece:
            move = f"{self.selected_hand_piece}*{square_str}"
            if move in [m.usi() for m in self.board.legal_moves]:
                self.board.push_usi(move)
                self.update_board()
                if self.board.turn == self.ai_color:
                    QTimer.singleShot(100, self.evaluate_bestmove)
            self.selected_hand_piece = None
            return

        # 通常の移動
        if self.selected is None:
            piece = self.board.piece_at(sq_index)

            if not piece:
                return

            # ここで手番と駒の所有者が一致するか確認
            if piece.color != self.board.turn:
                print("⚠️ 相手の駒は選択できません。")
                return

            self.selected = sq_index
        else:
            move_base = shogi.SQUARE_NAMES[self.selected] + square_str
            legal_moves = list(self.board.legal_moves)
            matched = [m for m in legal_moves if m.usi().startswith(move_base)]

            if not matched:
                self.selected = None
                return

            if len(matched) == 2 and any(m.promotion for m in matched):
                promote = self.ask_promotion()
                move = [m for m in matched if m.promotion == promote][0]
            else:
                move = matched[0]

            self.board.push(move)
            self.update_board()
            if self.board.turn == self.ai_color:
                QTimer.singleShot(100, self.evaluate_bestmove)
            self.selected = None

    def ask_promotion(self):
        msg = QMessageBox()
        msg.setWindowTitle("成りますか？")
        msg.setText("この駒を成りますか？")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ret = msg.exec_()
        return ret == QMessageBox.Yes
    def toggle_ai_vs_ai(self):
        self.ai_vs_ai = not self.ai_vs_ai
        if self.ai_vs_ai:
            self.chat_label.setText("AI同士で対局中...")
            QTimer.singleShot(100, self.evaluate_bestmove)  # ← 無条件でスタート！
        else:
            self.chat_label.setText("AI vs AI 終了")

    def evaluate_bestmove(self, retry=False):
        if self.board.is_game_over():
            self.chat_label.setText(f"対局終了: {self.board.result()}")
            return

        if not self.ai_vs_ai and self.board.turn != self.ai_color:
            return

        # ✅ SFENとmovesを分離して明示
        sfen = self.board.sfen()
        moves = ' '.join(m.usi() for m in self.board.move_stack)
        cmd = f"position sfen {sfen} moves {moves}"
        try:

            bestmove, bestvalue = self.ai.get_bestmove_with_value(cmd)
            legal_moves = list(self.board.legal_moves)

            if not any(m.usi() == bestmove for m in legal_moves):
                print(f"⚠️ 不正な手（{bestmove}）が返されました。AIの盤面を確認します。")
                self.ai.show_board()  # ← AI側に確認要求

                # print(f"[DEBUG] 現在のSFEN: {sfen}")
                # print(f"[DEBUG] 手順: {moves}")
                # print("🔍 現在の盤面（可視）:")
                # print(self.board)  
                # # 🔁 評価値付きで合法手を再評価
                # best_legal_move = None
                # best_legal_value = -float("inf")

                # for move in legal_moves:
                #     test_board = self.board.copy()
                #     test_board.push(move)
                #     sfen_test = test_board.sfen()
                #     try:
                #         value = self.ai.evaluate_position(sfen_test)
                #         if value > best_legal_value:
                #             best_legal_value = value
                #             best_legal_move = move
                #     except:
                #         continue  # 無視して次へ

                # if best_legal_move:
                #     self.board.push(best_legal_move)
                #     self.update_board()
                #     self.chat_label.setText(f"⚠️ AI不正 → 代替手: {best_legal_move.usi()}")
                #     print(f"chatbot_output:move={best_legal_move.usi()} value={best_legal_value:.2f}", flush=True)
                #     QTimer.singleShot(300, self.evaluate_bestmove)
                # else:
                #     print("❌ 合法手の再評価に失敗しました。")
                # return

            # 正常な手ならそのまま実行
            self.board.push_usi(bestmove)
            self.update_board()
            self.chat_label.setText(f"AIの指し手: {bestmove}")
            print(f"chatbot_output:move={bestmove} value={bestvalue:.2f}", flush=True)
            if self.ai_vs_ai or self.board.turn == self.ai_color:
                QTimer.singleShot(300, self.evaluate_bestmove)

        except Exception as e:
            print("AIエラー:", e)




def write_log(file_path, label, content):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"[{label}] {now}\n")
        if isinstance(content, shogi.Board):
            f.write(content.kif_str())
            f.write("\nSFEN: " + content.sfen())
        else:
            f.write(str(content))
        f.write("\n" + "=" * 50 + "\n")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShogiBoard()
    window.show()
    sys.exit(app.exec_())