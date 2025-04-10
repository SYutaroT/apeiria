import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsItem
import cshogi

class ShogiPiece(QGraphicsItem):
    def __init__(self, x, y, color, name):
        super().__init__()
        self.setPos(x, y)
        self.color = color
        self.name = name
        self.setFlag(QGraphicsItem.ItemIsMovable)  # ドラッグ可能にする

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(self.color))
        painter.drawRect(0, 0, 50, 50)  # 駒を50x50の矩形として描画
        painter.setPen(QColor(0, 0, 0))
        painter.drawText(0, 0, 50, 50, Qt.AlignCenter, self.name)

    def boundingRect(self):
        return QRectF(0, 0, 50, 50)

class ShogiBoard(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)

        self.board_size = 9
        self.square_size = 60
        self.board = cshogi.Board()  # cshogiの盤面を使う
        self.setup_board()
        self.create_pieces()

    def setup_board(self):
        # 将棋盤のマス目を描画
        for row in range(self.board_size):
            for col in range(self.board_size):
                x = col * self.square_size
                y = row * self.square_size
                square = QGraphicsRectItem(x, y, self.square_size, self.square_size)
                square.setPen(QColor(0, 0, 0))
                square.setBrush(QBrush(QColor(240, 217, 181)))  # 明るい木目調の色
                self.scene.addItem(square)

    def create_pieces(self):
        # 駒を配置（cshogiの盤面を元にして駒を描画）
        self.pieces = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                piece = self.board[cshogi.Position(row, col)]  # 修正: Pos -> Position に変更
                if piece != cshogi.PIECE_NONE:
                    color = QColor(255, 0, 0) if piece > 0 else QColor(0, 0, 255)  # 先手は赤、後手は青
                    name = self.get_piece_name(piece)
                    x = col * self.square_size
                    y = row * self.square_size
                    shogi_piece = ShogiPiece(x, y, color, name)
                    self.scene.addItem(shogi_piece)
                    self.pieces.append(shogi_piece)

    def get_piece_name(self, piece):
        piece_dict = {
            cshogi.PIECE_PAWN: "歩", cshogi.PIECE_KNIGHT: "桂", cshogi.PIECE_LANCE: "香",
            cshogi.PIECE_BISHOP: "角", cshogi.PIECE_ROOK: "飛", cshogi.PIECE_KING: "玉",
            cshogi.PIECE_GOLD: "金", cshogi.PIECE_SILVER: "銀", cshogi.PIECE_COPPER: "銅",
        }
        return piece_dict.get(piece, "")

    def mouseReleaseEvent(self, event):
        # 駒を移動する処理を追加
        item = self.itemAt(event.pos())
        if isinstance(item, ShogiPiece):
            # 駒が移動可能な場合、cshogiの盤面に移動を反映
            start_pos = self.get_board_pos(item.x(), item.y())
            # ここで駒の移動処理を追加
            print(f"移動: {start_pos}")

    def get_board_pos(self, x, y):
        row = int(y // self.square_size)
        col = int(x // self.square_size)
        return cshogi.Pos(row, col)

class ShogiWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("動かせる将棋盤")
        self.setGeometry(100, 100, 600, 600)
        
        self.shogi_board = ShogiBoard()
        self.setCentralWidget(self.shogi_board)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShogiWindow()
    window.show()
    sys.exit(app.exec_())
