import re
import pandas as pd
with open("ai_board.log", encoding="utf-8") as f:
    lines = f.readlines()

kifus = []
current = []

for line in lines:
    if re.match(r"^P1", line):  # P1が見つかったら新しい棋譜スタート
        current = [line.strip()]
    elif re.match(r"^P[2-9]", line):
        current.append(line.strip())
    elif line.strip() == "-":
        current.append("-")
        kifus.append(current)
        current = []

with open("output_kifus1.txt", "w", encoding="utf-8") as f:
    for i, board in enumerate(kifus, 1):
        f.write(f"=== 第{i}局面 ===\n")
        for line in board:
            f.write(line + "\n")
        f.write("\n")



with open("actual_board.log", encoding="utf-8") as f:
    lines = f.readlines()
# 修正：盤面の開始と終了を正しく検出
boards = []
current_board = []
collecting = False


for line in lines:
    if re.match(r"^\+[-+]+\+$", line):  # 盤面の区切り線
        if not collecting:
            current_board = [line.rstrip()]
            collecting = True
        else:
            current_board.append(line.rstrip())
            boards.append(current_board)
            collecting = False
    elif collecting:
        current_board.append(line.rstrip())
with open("output_kifus2.txt", "w", encoding="utf-8") as f:
    for i, board in enumerate(boards, 1):
        f.write(f"=== 第{i}局面 ===\n")
        for line in board:
            f.write(line + "\n")
        f.write("\n")
