import subprocess
import os

# 相対パスのベース
directory = os.path.dirname(os.path.abspath(__file__))
checkpoint_path = os.path.join(directory, "checkpoint-005.pth")
bat_path = os.path.join(directory, "dlshogi_engine.bat")
syougi_path = os.path.join(directory, "syougi.py")

# 確認用
if not os.path.exists(syougi_path):
    print(f"❌ syougi.py が見つかりません: {syougi_path}")
    exit(1)
if not os.path.exists(bat_path):
    print(f"❌ dlshogi_engine.bat が見つかりません: {bat_path}")
    exit(1)

# GUIのPyQtプログラムを起動（バックグラウンド）
print("▶ syougi.py を起動します...")
syogi_proc = subprocess.Popen(
    ["python", "syougi.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True,
    cwd=directory
)

# AIエンジンをバッチファイル経由で起動
print("▶ AIエンジンを起動します...")
ai_proc = subprocess.Popen(
    ["cmd", "/c", bat_path],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True,
    bufsize=1,
    cwd=directory
)

# USIとモデルファイルの指定
print("▶ AI に USI を送信します...")
try:
    ai_proc.stdin.write("usi\n")
    ai_proc.stdin.flush()
    ai_proc.stdin.write(f"setoption name modelfile value {checkpoint_path}\n")
    ai_proc.stdin.flush()
    ai_proc.stdin.write("isready\n")
    ai_proc.stdin.flush()
except Exception as e:
    print("❌ AIエンジンへのコマンド送信失敗:", e)

# ログ表示（GUIとAI両方）
print("=== 起動ログ ===")
try:
    while True:
        ai_line = ai_proc.stdout.readline()
        if ai_line:
            print("[AI]", ai_line.strip())
        gui_line = syogi_proc.stdout.readline()
        if gui_line:
            print("[GUI]", gui_line.strip())
        if syogi_proc.poll() is not None:
            print("🛑 syougi.py が終了しました")
            break
except KeyboardInterrupt:
    print("🛑 強制終了（Ctrl+C）")

# 末尾の finally に以下を追加して確認
finally:
    print(f"🔚 syougi.py 終了コード: {syogi_proc.poll()}")
    print("🔚 AIプロセスを終了します...")
    ai_proc.kill()
