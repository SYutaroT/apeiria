# 辞書を作成するAPI
import patternItem
import re
import analyzer
import markov
from pathlib import Path

class Dictionary(object):
    def __init__(self):
        self.base_path = Path(__file__).resolve().parent / "dics"  # ← これを共通で使う
        self.random = self.makeRandomList()
        self.pattern = self.makePatternDictionary()
        self.template = self.makeTemplateDictionary()
        self.markovsentence = self.makeMarkovDictionary()

    def makeRandomList(self):
        rfile_path = self.base_path / "random.txt"
        with open(rfile_path, encoding="utf-8") as rfile:
            r_lines = rfile.readlines()
        randomList = [line.rstrip("\n") for line in r_lines if line.strip()]
        return randomList

    def makePatternDictionary(self):
        pfile_path = self.base_path / "pattern.txt"
        with open(pfile_path, encoding="utf-8") as pfile:
            p_lines = [line.rstrip("\n") for line in pfile if line.strip()]
        return [patternItem.PatternItem(*line.split('\t')) for line in p_lines]

    def makeTemplateDictionary(self):
        tfile_path = self.base_path / "template.txt"
        with open(tfile_path, encoding="utf-8") as tfile:
            t_lines = [line.rstrip("\n") for line in tfile if line.strip()]
        templateDictionary = {}
        for line in t_lines:
            count, tempstr = line.split('\t')
            templateDictionary.setdefault(count, []).append(tempstr)
        return templateDictionary

    def makeMarkovDictionary(self):  # マルコフ辞書
        sentences = []
        mark = markov.Markov()
        text = mark.make()
        sentences = text.split('\n')

        if "" in sentences:
            sentences.remove("")
        return sentences

    def study(self, input, parts):  # 学習則
        input = input.rstrip("\n")
        self.study_random(input)
        self.study_pattern(input, parts)
        self.study_template(parts)

    def study_random(self, input):
        if not input in self.random:
            self.random.append(input)

    def study_pattern(self, input, parts):
        for word, part in parts:
            if analyzer.keyword_check(part):
                depend = None
                for ptn_item in self.pattern:
                    if re.search(ptn_item.pattern, word):
                        depend = ptn_item
                        break

                if depend:
                    depend.add_phrase(input)
                else:
                    self.pattern.append(patternItem.PatternItem(word, input))

    def study_template(self, parts):
        tempstr = ""
        count = 0
        for word, part in parts:
            if (analyzer.keyword_check(part)):
                tempstr += word
        if count > 0:
            count = str(count)
            if not count in self.template:
                self.template[count] = []
            if not tempstr in self.template[count]:
                self.template[count].append(tempstr)
    def save(self):
        # random.txt
        rfile_path = self.base_path / "random.txt"
        with open(rfile_path, "w", encoding="utf-8") as f:
            f.writelines([line + "\n" for line in self.random])

        # pattern.txt
        pfile_path = self.base_path / "pattern.txt"
        with open(pfile_path, "w", encoding="utf-8") as f:
            f.writelines([ptn.make_line() + "\n" for ptn in self.pattern])

        # template.txt
        tfile_path = self.base_path / "template.txt"
        lines = []
        for key, vals in self.template.items():
            for v in vals:
                lines.append(f"{key}\t{v}\n")
        with open(tfile_path, "w", encoding="utf-8") as f:
            f.writelines(sorted(lines))
