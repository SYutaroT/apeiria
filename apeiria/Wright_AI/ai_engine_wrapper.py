import os
import sys
import subprocess
import threading
import time
from PyQt5.QtCore import QCoreApplication

class AIEngineWrapper:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        engine_path = os.path.join(base_dir, "mcts_player.py")
        python_path = sys.executable

        self.proc = subprocess.Popen(
            [python_path, engine_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            text=True,
            bufsize=1
        )

        self.lock = threading.Lock()
        self._read_buffer = []
        self._reader_thread = threading.Thread(target=self._reader_loop, daemon=True)
        self._reader_thread.start()
        self._init_engine()

    def _init_engine(self):
        self.send("usi")
        self._wait_for("usiok")
        self.send("isready")
        self._wait_for("readyok")

    def _reader_loop(self):
        for line in self.proc.stdout:
            line = line.strip()
            if line:
                self._read_buffer.append(line)
                print(f"[AI OUT] {line}")

    def send(self, cmd: str):
        with self.lock:
            print(f"[AI IN] {cmd}")
            self.proc.stdin.write(cmd + "\n")
            self.proc.stdin.flush()

    def _wait_for(self, keyword: str, timeout=10.0) -> str:
        start = time.time()
        while time.time() - start < timeout:
            if self._read_buffer:
                line = self._read_buffer.pop(0)
                if keyword in line:
                    return line
            time.sleep(0.01)
        raise TimeoutError(f"タイムアウト：'{keyword}' を受信できませんでした。")

    def get_bestmove(self, position_cmd: str, byoyomi=1000) -> str:
        self.send(position_cmd)
        self.send(f"go byoyomi {byoyomi}")
        start = time.time()
        while time.time() - start < 30:
            if self._read_buffer:
                line = self._read_buffer.pop(0)
                if line.startswith("bestmove"):
                    return line.split()[1]
            time.sleep(0.01)
        raise TimeoutError("bestmove の応答がありませんでした。")

    def quit(self):
        try:
            self.send("quit")
            self.proc.terminate()
        except Exception:
            pass

    def evaluate_position(self, sfen):
        self.send(f"position sfen {sfen}")
        self.send("go byoyomi 100")
        while True:
            line = self._read_line(timeout=10.0)
            if line is None:
                break
            if line.startswith("info") and "score cp" in line:
                try:
                    cp = int(line.split("score cp")[1].split()[0])
                    return cp
                except:
                    continue
            if line.startswith("bestmove"):
                break
        return 0

    def get_bestmove_with_value(self, position_cmd):
        self.send("isready")
        self._wait_for("readyok")

        self.send(position_cmd)
        self.send("go byoyomi 1000")

        bestmove = None
        value = 0.5

        while True:
            line = self._read_line(timeout=10.0)
            if line is None:
                raise TimeoutError("bestmove の応答がありませんでした。")

            if line.startswith("info"):
                if "score cp" in line:
                    try:
                        cp_str = line.split("score cp")[1].split()[0]
                        cp = int(cp_str)
                        value = 1 / (1 + pow(10, -cp / 600))
                    except:
                        pass
            elif line.startswith("bestmove"):
                bestmove = line.split()[1]
                break

        return bestmove, value

    def _read_line(self, timeout=10.0):
        start = time.time()
        while time.time() - start < timeout:
            if self._read_buffer:
                return self._read_buffer.pop(0)
            time.sleep(0.01)
            QCoreApplication.processEvents()
        return None
    def show_board(self):
        self.send("showboard")

