from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel, QHBoxLayout,QMessageBox
from PyQt5.QtCore import Qt
import shogi
import sys
from collections import Counter
import sys
import traceback

# すべての例外をキャッチして、標準出力に表示する
def excepthook(exc_type, exc_value, exc_tb):
    print("❌ GUI内で例外が発生:")
    traceback.print_exception(exc_type, exc_value, exc_tb)

sys.excepthook = excepthook

class ShogiBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("将棋盤 - クリックで指す")
        self.board = shogi.Board()
        self.selected = None
        self.selected_hand_piece = None

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

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
        # ④ 終了ボタン
        self.quit_button = QPushButton("終了")
        self.quit_button.setFixedSize(100, 40)
        self.quit_button.setStyleSheet("font-size: 16px;")
        self.quit_button.clicked.connect(QApplication.quit)
        self.main_layout.addWidget(self.quit_button, alignment=Qt.AlignCenter)

    def init_board(self):
        for row in range(9):
            for col in range(9):
                btn = self.buttons[row][col]
                btn.setFixedSize(60, 60)
                btn.setStyleSheet("font-size: 18px;")
                btn.clicked.connect(lambda _, r=row, c=col: self.cell_clicked(r, c))
                self.grid.addWidget(btn, row, col)
        self.update_board()

    def update_board(self):
        for row in range(9):
            for col in range(9):
                sq = shogi.SQUARES[(8 - row) * 9 + col]
                piece = self.board.piece_at(sq)
                self.buttons[row][col].setText(self.unicode_piece(piece) if piece else "")
                if piece:
                    color = "#e0f7fa" if piece.color == shogi.BLACK else "#ffebee"
                    self.buttons[row][col].setStyleSheet(f"font-size: 18px; background-color: {color};")
                else:
                    self.buttons[row][col].setStyleSheet("font-size: 18px; background-color: white;")

        self.sente_hand_label.setText("先手の持ち駒: " + self.format_hand_pieces(shogi.BLACK))
        self.gote_hand_label.setText("後手の持ち駒: " + self.format_hand_pieces(shogi.WHITE))

        self.update_hand_buttons(shogi.BLACK, self.sente_hand_layout)
        self.update_hand_buttons(shogi.WHITE, self.gote_hand_layout)

    def unicode_piece(self, piece):
        if not piece:
            return ""
        symbol = piece.symbol()
        return {
            'P': '歩', 'L': '香', 'N': '桂', 'S': '銀', 'G': '金',
            'B': '角', 'R': '飛', 'K': '玉',
            '+P': 'と', '+L': '成香', '+N': '成桂', '+S': '成銀',
            '+B': '馬', '+R': '龍',
            'p': '歩', 'l': '香', 'n': '桂', 's': '銀', 'g': '金',
            'b': '角', 'r': '飛', 'k': '王',
            '+p': 'と', '+l': '成香', '+n': '成桂', '+s': '成銀',
            '+b': '馬', '+r': '龍'
        }.get(symbol, symbol)

    def coord_to_square(self, row, col):
        file = 9 - col
        rank = 9 - row
        letter = "abcdefghi"[rank - 1]
        return f"{file}{letter}"

    def cell_clicked(self, row, col):
        print("合法な打ち手:", [m.usi() for m in self.board.legal_moves if m.drop_piece_type])
        print(self.board)
        square = self.coord_to_square(row, col)
        sq_index = shogi.SQUARES[(8 - row) * 9 + col]

        if self.selected_hand_piece:
            piece = self.selected_hand_piece
            move = f"{piece}*{square}"
            print(f"打ち手: {move}")
            try:
                if move not in [m.usi() for m in self.board.legal_moves]:
                    raise ValueError(f"{move} は合法手ではありません")
                self.board.push_usi(move)
                self.update_board()
            except Exception as e:
                print("❌ 非合法手（打ち）:", e)
            self.selected_hand_piece = None
            return

        if self.selected is None:
            piece = self.board.piece_at(sq_index)
            if piece is None:
                print("⚠ 空のマスです。駒を選んでください。")
                return
            if piece.color != self.board.turn:
                print("⚠ 今はその駒の手番ではありません。")
                return
            self.selected = square
            print(f"選択: {square}")
        else:
            move = self.selected + square
            print(f"指し手: {move}")
            try:
                legal_moves = list(self.board.legal_moves)
                matched_moves = [m for m in legal_moves if m.usi().startswith(move)]

                if not matched_moves:
                    raise ValueError(f"{move} は合法手ではありません")

                # 成り選択が必要な場合（成り手と不成り手が両方ある）
                if len(matched_moves) == 2 and any(m.promotion for m in matched_moves):
                    if self.ask_promotion():
                        move_obj = [m for m in matched_moves if m.promotion][0]
                    else:
                        move_obj = [m for m in matched_moves if not m.promotion][0]
                else:
                    move_obj = matched_moves[0]  # 成り or 不成りしかない場合

                self.board.push(move_obj)
                self.update_board()

            except Exception as e:
                print("❌ 非合法手:", e)

            self.selected = None

    def format_hand_pieces(self, color):
        hands = self.board.pieces_in_hand[color]
        counter = Counter(hands)
        text = ""
        for p, n in sorted(counter.items()):
            symbol = shogi.PIECE_SYMBOLS[p]
            piece_obj = shogi.Piece.from_symbol(symbol)
            text += f"{self.unicode_piece(piece_obj)}×{n}　"
        return text.strip()

    def update_hand_buttons(self, color, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        counter = Counter(self.board.pieces_in_hand[color])
        for p, n in sorted(counter.items()):
            symbol = shogi.PIECE_SYMBOLS[p]
            piece_obj = shogi.Piece.from_symbol(symbol)
            label = self.unicode_piece(piece_obj)
            btn = QPushButton(f"{label}×{n}")
            btn.setFixedSize(60, 40)
            btn.setStyleSheet("font-size: 14px;")
            btn.clicked.connect(lambda _, s=symbol: self.select_hand_piece(s))
            layout.addWidget(btn)

    def select_hand_piece(self, symbol):
        self.selected_hand_piece = symbol.upper()
        self.selected = None
        print(f"打ち駒選択: {self.selected_hand_piece}")

    def ask_promotion(self):
        msg = QMessageBox()
        msg.setWindowTitle("成りますか？")
        msg.setText("この駒を成りますか？")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ret = msg.exec_()
        return ret == QMessageBox.Yes

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShogiBoard()
    window.show()
    sys.exit(app.exec_())