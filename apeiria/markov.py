import re
import random
import analyzer


class Markov:
    def make(self):
        filename = "apeiria/dics/log.txt"
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
        text = re.sub(">", "", text)
        text = re.sub(
            "apeiria:Repeat?|apriria:Random|Apriria:Pattern|Apeiria:Template|apeiria:Markov|apeiria", "", text)
        text = re.sub("Apeiria System Dialogue Log:.*\n", "", text)
        text = re.sub("\n\n", "\n", text)
        wordlist = analyzer.parse(text)
        return self.makeMarkov(wordlist)

    def makeMarkov(self, wordlist):
        markov = {}
        p1 = ""
        p2 = ""
        p3 = ""
        for word in wordlist:
            if p1 and p2 and p3:
                if (p1, p2, p3) not in markov:
                    markov[(p1, p2, p3)] = []
                markov[(p1, p2, p3)].append(word)
            p1, p2, p3 = p2, p3, word
        count = 0
        sentence = ""
        p1, p2, p3 = random.choice(list(markov.keys()))
        while count < 30:
            if ((p1, p2, p3) in markov) == True:
                tmp = random.choice(markov[(p1, p2, p3)])
                sentence += tmp
            p1, p2, p3 = p2, p3, tmp
            count += 1
        sentence = re.sub("」", "", sentence)
        sentence = re.sub("「", "", sentence)
        return sentence
