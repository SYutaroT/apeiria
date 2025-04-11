import re
ai_to_kanji = {
    "-KY": "v香", "-KE": "v桂", "-GI": "v銀", "-KI": "v金", "-OU": "v玉", "-FU": "v歩",
    "-HI": "v飛", "-KA": "v角", "-UM": "v馬", "-RY": "v龍", "-TO": "vと",
    "+KY": "香",  "+KE": "桂",  "+GI": "銀",  "+KI": "金",  "+OU": "玉",  "+FU": "歩",
    "+HI": "飛",  "+KA": "角",  "+UM": "馬",  "+RY": "龍",  "+TO": "と",".":"*"
}

def extract_board_from_ai_log(lines):
    board_lines = []
    for line in lines:
        if re.match(r"^P\d", line):  # "P1", "P2", ...で始まる行
            board_lines.append(line[2:].replace(" ", ""))
    return board_lines

def extract_board_from_actual_log(lines):
    board_lines = []
    inside_board = False
    for line in lines:
        if '９ ８ ７' in line:  # ボード開始の目印
            inside_board = True
            continue
        if inside_board:
            if line.startswith('+'):
                continue
            if line.startswith('|'):
                board_lines.append(line[1:20].replace(" ", "").replace("・", "."))
            else:
                break
    return board_lines

def compare_boards(ai_board, actual_board):
    diff_lines = []
    for ai_row, actual_row in zip(ai_board, actual_board):
        diff = ''.join(' ' if a == b else '*' for a, b in zip(ai_row, actual_row))
        diff_lines.append((ai_row, actual_row, diff))
    return diff_lines

# === ログファイル読み込み ===
with open("ai_board.log", encoding="utf-8") as f:
    ai_lines = f.readlines()

with open("actual_board.log", encoding="utf-8") as f:
    actual_lines = f.readlines()

# === 盤面抽出 ===
ai_board = extract_board_from_ai_log(ai_lines)
actual_board = extract_board_from_actual_log(actual_lines)

# === 差分比較と出力 ===
diffs = compare_boards(ai_board, actual_board)

print("=== 差分 ===")
for ai, actual, diff in diffs:
    print(f"AI     : {ai}")
    print(f"Actual : {actual}")
    print(f"Diff   : {diff}\n")
