# 辞書を作成するAPI
import patternItem
import re
import analyzer
import markov


class Dictionary(object):

    def __init__(self):
        self.random = self.makeRandomList()
        self.pattern = self.makePatternDictionary()
        self.template = self.makeTemplateDictionary()
        self.markovsentence = self.makeMarkovDictionary()

    def makeRandomList(self):  # ランダムに出力する言葉の辞書
        rfile = open("apeiria/dics/random.txt",
                     "r", encoding="utf-8")
        r_lines = rfile.readlines()
        rfile.close()
        randomList = []
        for line in r_lines:
            str = line.rstrip("\n")
            if (str != ''):
                randomList.append(str)
        return randomList

    def makePatternDictionary(self):  # 定型文の辞書
        pfile = open("apeiria/dics/pattern.txt",
                     "r", encoding="utf-8")
        p_lines = pfile.readlines()
        pfile.close()
        new_lines = []
        for line in p_lines:
            str = line.rstrip("\n")
            if (str != ''):
                new_lines.append(str)
        patternItemList = []
        for line in new_lines:
            ptn, prs = line.split('\t')
            patternItemList.append(patternItem.PatternItem(ptn, prs))
        return patternItemList

    def makeTemplateDictionary(self):  # テンプレワードの辞書
        tfile = open("apeiria/dics/template.txt",
                     "r", encoding="utf-8")
        t_lines = tfile.readlines()
        tfile.close()
        new_t_lines = []
        for line in t_lines:
            str = line.rstrip("\n")
            if (str != ""):
                new_t_lines.append(str)
        templateDictionary = {}
        for line in new_t_lines:
            count, tempstr = line.split('\t')
            if not count in templateDictionary:
                templateDictionary[count] = []
            templateDictionary[count].append(tempstr)
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
        for index, element in enumerate(self.random):
            self.random[index] = element+"\n"
        with open("apeiria/dics/random.txt", "w", encoding="utf-8") as f:
            f.writelines(self.random)
        pattern = []
        for ptn_item in self.pattern:
            pattern.append(ptn_item.make_line()+"\n")
        with open("apeiria/dics/pattern.txt", "w", encoding="utf-8") as f:
            f.writelines(pattern)
        templist = []
        for key, val in self.template.items():
            for v in val:
                templist.append(key+"\t"+v+"\n")
        templist.sort()
        with open("apeiria/dics/template.txt", "w", encoding="utf-8") as f:
            f.writelines(templist)
