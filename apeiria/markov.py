import re
import random
from pathlib import Path
import analyzer


class Markov:
    def make(self):
        # 実行位置に依存せず安定してファイルパスを指定
        base_path = Path(__file__).resolve().parent / "dics"
        filename = base_path / "log.txt"

        if not filename.exists():
            print("⚠️ log.txt が見つかりません。マルコフ文は生成されません。")
            return ""

        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()

        # 文字列整形
        text = re.sub(">", "", text)
        text = re.sub(r"apeiria:Repeat?|apriria:Random|Apriria:Pattern|Apeiria:Template|apeiria:Markov|apeiria", "", text)
        text = re.sub(r"Apeiria System Dialogue Log:.*\n", "", text)
        text = re.sub("\n\n", "\n", text)

        wordlist = analyzer.parse(text)

        return self.makeMarkov(wordlist)

    def makeMarkov(self, wordlist):
        if not wordlist or len(wordlist) < 4:
            return "（学習データが不足しています）"

        markov = {}
        p1 = ""
        p2 = ""
        p3 = ""
        for word in wordlist:
            if p1 and p2 and p3:
                markov.setdefault((p1, p2, p3), []).append(word)
            p1, p2, p3 = p2, p3, word

        count = 0
        sentence = ""
        p1, p2, p3 = random.choice(list(markov.keys()))
        while count < 30 and (p1, p2, p3) in markov:
            tmp = random.choice(markov[(p1, p2, p3)])
            sentence += tmp
            p1, p2, p3 = p2, p3, tmp
            count += 1

        sentence = sentence.replace("「", "").replace("」", "")
        return sentence
