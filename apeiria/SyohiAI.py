import subprocess
import time
import os

# 相対パスに対応
current_dir = os.path.dirname(os.path.abspath(__file__))

# GUIのPyQtプログラムを起動（バックグラウンド）
syogi_path = os.path.join(current_dir, "syougi.py")
syogi_proc = subprocess.Popen(
    ["python", syogi_path],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True
)

# AIの思考エンジンを起動（別プロセス）
ai_proc = subprocess.Popen(
    ["python", "-m", "pydlshogi2.player.mcts_player"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True,
    bufsize=1,
    cwd=os.path.join(current_dir, "shigi")  # 相対パスでAIモジュール起動
)

# checkpointの指定を反映（modelfile オプション）
ai_proc.stdin.write("usi\n")
ai_proc.stdin.flush()

# checkpoint-005.pth を使用（相対パス）
ai_proc.stdin.write("setoption name modelfile value checkpoints/checkpoint-005.pth\n")
ai_proc.stdin.flush()

# エンジンが ready になるまで
ai_proc.stdin.write("isready\n")
ai_proc.stdin.flush()

# 表示（デバッグ用）
while True:
    line = ai_proc.stdout.readline()
    if line:
        print("[AI]", line.strip())
    if "readyok" in line:
        break

# 終了処理（GUI閉じたときなど）
try:
    syogi_proc.wait()
finally:
    ai_proc.kill()
