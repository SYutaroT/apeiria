import re
import random


class PatternItem:
    SEPARATOR1 = '^((-?\d+)##)?(.*)$'
    SEPARATOR2 = "^(.*)(##(-?\d+))$"

    def __init__(self, pattern, phrases):
        self.initModifyAndPattern(pattern)
        self.initPhrases(phrases)

    def initModifyAndPattern(self, pattern):
        m = re.findall(PatternItem.SEPARATOR1, pattern)
        self.modify = 0
        if m[0][1]:
            self.modify = int(m[0][1])
        self.pattern = m[0][2]

    def initPhrases(self, phrases):
        self.phrases = []
        dic = {}
        for phrase in phrases.split("|"):
            m = re.findall(PatternItem.SEPARATOR1, phrase)
            dic["need"] = 0
            if m[0][1]:
                dic["need"] = int(m[0][1])
            dic["phrase"] = m[0][2]
            self.phrases.append(dic.copy())

    def match(self, str):
        return re.search(self.pattern, str)

    def choice(self, mood):
        choices = []
        for p in self.phrases:
            if (self.suitable(p["need"], mood)):
                choices.append(p["phrase"])
        if (len(choices) == 0):
            return None
        return random.choice(choices)

    def suitable(self, need, mood):
        if (need == 0):
            return True
        elif (need > 0):
            return (mood > need)
        else:
            return (mood < need)

    def add_phrase(self, phrase):
        for p in self.phrases:
            if p["phrase"] == phrase:
                return
        self.phrases.append({"need": 0, "phrase": phrase})

    def make_line(self):
        pattern = str(self.modify)+"##"+self.pattern
        pr_list = []
        for p in self.phrases:
            pr_list.append(str(p["need"])+"##"+p["phrase"])
        return pattern+"\t"+"|".join(pr_list)


class response_face:
    def face_check(self, check):
        if "##" in check:
            s = re.findall(PatternItem.SEPARATOR2, check)
            resp = s[0][0]
            fc = s[0][1]


        else:
            resp = check

        return resp

    def face_check_num(self, check):
        if "##" in check:
            c = re.findall(PatternItem.SEPARATOR2, check)
            fc = c[0][2]
        else:
            fc = "0"
        return fc
