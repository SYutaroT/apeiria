    import re

    with open("actual_board.log", encoding="utf-8") as f:
        lines = f.readlines()

    actual_kifus = []
    current = []
    inside_board = False

    for line in lines:
        if "９ ８ ７" in line:
            current = []
            inside_board = True
        elif inside_board and "│" in line:  # 罫線文字を含む行
            current.append(line.strip())
        elif inside_board and "+-" in line:
            if current:  # 空でないときだけ追加
                actual_kifus.append(current)
            inside_board = False

    # === 全局面出力 ===
    for i, kifu in enumerate(actual_kifus, 1):
        print(f"=== 第 {i} 実盤面 ===".encode("utf-8").decode("cp932", errors="replace"))
        if kifu:
            for row in kifu:
                print(row.encode("utf-8").decode("cp932", errors="replace"))
        else:
            print("(盤面データなし)")
        print()
