import time
import re
import cshogi
import sys

sys.stdout.reconfigure(encoding='utf-8')

PIECE_NAME = {
    cshogi.PAWN: "歩", cshogi.LANCE: "香", cshogi.KNIGHT: "桂", cshogi.SILVER: "銀",
    cshogi.GOLD: "金", cshogi.BISHOP: "角", cshogi.ROOK: "飛", cshogi.KING: "玉",
    cshogi.PROM_PAWN: "と", cshogi.PROM_LANCE: "成香", cshogi.PROM_KNIGHT: "成桂",
    cshogi.PROM_SILVER: "成銀", cshogi.PROM_BISHOP: "馬", cshogi.PROM_ROOK: "龍"
}

log_path = "log.txt"
last_position = 0  # 最後に読み込んだファイルの位置

print("log.txt を監視中... 指し手と駒を表示します\n")

while True:
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            f.seek(last_position)
            new_lines = f.readlines()
            last_position = f.tell()  # 次回はここから読み始める

        for line in new_lines:
            # 打ち駒ログの処理
            if "[go] 打ち駒:" in line:
                match = re.search(r"打ち駒:\s*(.+?) を (\S+) に打つ", line)
                if match:
                    piece = match.group(1)
                    to_sq = match.group(2)
                    print(f"{piece} を {to_sq} に打つ")

            elif "[go] 指し手:" in line:
                match = re.search(r"指し手:\s*(\S+)[（(](.+?)[）)]", line)
                if match:
                    move = match.group(1)
                    original_piece = match.group(2)
                    from_sq = move[0:2]
                    to_sq = move[2:4]

                    # 成り判定（末尾が + なら成り）
                    if move.endswith("+"):
                        PROMOTE_MAP = {
                            "歩": "と", "香": "成香", "桂": "成桂", "銀": "成銀",
                            "角": "馬", "飛": "龍"
                        }
                        piece = PROMOTE_MAP.get(original_piece, original_piece + "成")
                    else:
                        piece = original_piece

                    print(f"{piece} を {from_sq} から {to_sq} に移動")


            # 対局終了キーワードを検出したらリセット
            if "[log reset request]" in line:
                print("\n📄 ログリセットリクエストを検出。監視を再開します...\n")
                last_position = 0
                break
        time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n監視を終了しました")
        break
    except Exception as e:
        print(f"[ERROR] {e}")
        time.sleep(2)