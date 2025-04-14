import time
import re
import cshogi
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

PIECE_NAME = {
    cshogi.PAWN: "歩", cshogi.LANCE: "香", cshogi.KNIGHT: "桂", cshogi.SILVER: "銀",
    cshogi.GOLD: "金", cshogi.BISHOP: "角", cshogi.ROOK: "飛", cshogi.KING: "玉",
    cshogi.PROM_PAWN: "と", cshogi.PROM_LANCE: "成香", cshogi.PROM_KNIGHT: "成桂",
    cshogi.PROM_SILVER: "成銀", cshogi.PROM_BISHOP: "馬", cshogi.PROM_ROOK: "龍"
}


script_dir = os.path.dirname(__file__)
# print(script_dir,flush=True)
log_path = os.path.join(script_dir,"log.txt")  # 2階層上なら
log_path = os.path.abspath(log_path)
last_position = 0  # 最後に読み込んだファイルの位置
with open(log_path, "a", encoding="utf-8") as f:
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    f.write(f"[{now}] [log reset request] 起動時にログを初期化します\n")
time.sleep(0.5)
with open(log_path, "w", encoding="utf-8") as f:
    f.write("[log init] ログを初期化しました\n")
print("対局スタートです\n",flush=True)

while True:
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            f.seek(last_position)
            new_lines = f.readlines()
            last_position = f.tell()  # 次回はここから読み始める

        for line in new_lines:
            # 打ち駒ログの処理
            if "[go] 打ち駒:" in line:
                match = re.search(r"打ち駒:\s*(.+?) を (\S+) に打つ", line)  # ← ここ
                if match:
                    piece = match.group(1)
                    to_sq = match.group(2)
                    print(f"{piece} を {to_sq} に打ちます", flush=True)

            elif "[go] 指し手:" in line:
                match = re.search(r"指し手:\s*(\S+)[（(](.+?)[）)]", line)  # ← ここ
                if match:
                    move = match.group(1)
                    original_piece = match.group(2)
                    from_sq = move[0:2]
                    to_sq = move[2:4]

                    if move.endswith("+"):
                        PROMOTE_MAP = {
                            "歩": "と", "香": "成香", "桂": "成桂", "銀": "成銀",
                            "角": "馬", "飛": "龍"
                        }
                        piece = PROMOTE_MAP.get(original_piece, original_piece + "成")
                    else:
                        piece = original_piece

                    print(f"{piece} を {from_sq} から {to_sq} に移動しました", flush=True)
            elif "[gameover]" in line:
                match = re.search(r"\[gameover\] 対局終了: (\w+)", line)
                if match:
                    result = match.group(1)
                    if result == "win":
                        print("勝ちました！", flush=True)
                    elif result == "lose":
                        print("負けました…", flush=True)
                    else:
                        print(f"対局終了: {result}", flush=True)


            # 対局終了キーワードを検出したらリセット
            if "[log reset request]" in line:
                print("\n📄 ログリセットリクエストを検出。監視を再開します...\n",flush=True)
                last_position = 0
                break
        time.sleep(0.5)

    except KeyboardInterrupt:
        # print("\n監視を終了しました",flush=True)
        break
    except Exception as e:
        print(f"[ERROR] {e}")
        time.sleep(2)   