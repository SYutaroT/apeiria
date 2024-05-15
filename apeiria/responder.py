import random
import re
import analyzer
import itertools
# *応答のスーパークラス


class Responder(object):
    def __init__(self, name):
        self.name = name

    def response(self, input, mood, parts):
        return ""

# *オウム返しのためのサブクラス


class RepeatResponder(Responder):
    def __init__(self, name):
        super().__init__(name)

    def response(self, input, mood, parts):
        return "{}ってなんですか？".format(input)

# *ランダム応答のためのサブクラス


class RandomResponder(Responder):

    def __init__(self, name, dic_random):
        super().__init__(name)
        self.random = dic_random

    def response(self, input, mood, parts):
        return random.choice(self.random)


class PatternResponder(Responder):
    def __init__(self, name, dic_pattern, dic_random):

        super().__init__(name)
        self.pattern = dic_pattern
        self.random = dic_random

    def response(self, input, mood, parts):
        resp = None
        for ptn_item in self.pattern:
            m = ptn_item.match(input)
            if m:
                resp = ptn_item.choice(mood)
            if resp != None:
                return re.sub("%match%", m.group(), resp)

        return random.choice(self.random)


class TemplateResponder(Responder):
    def __init__(self, name, dic_template, dic_random):
        super().__init__(name)
        self.template = dic_template
        self.random = dic_random

    def response(self, input, mood, parts):
        keywords = []
        for word, part in parts:
            if analyzer.keyword_check(part):
                keywords.append(word)
        count = len(keywords)
        if (count > 0) and (str(count) in self.template):
            resp = random.choice(self.template[str(count)])
            for word in keywords:
                resp = resp.replace("%noun%", word, 1)
            return resp
        return random.choice(self.random)


class MarcovResponder(Responder):
    def __init__(self, name, dic_marcov, dic_random):
        super().__init__(name)
        self.markovsentence = dic_marcov
        self.random = dic_random

    def response(self, input, mood, parts):
        m = []
        for word, part in parts:
            if analyzer.keyword_check(part):
                for sentence in self.markovsentence:
                    find = ".*?"+word+".*"
                    tmp = re.findall(find, sentence)
                    if tmp:
                        m.append(tmp)
        m = list(itertools.chain.from_iterable(m))
        check = set(m)
        m = list(check)
        if m:
            return (random.choice(m))
        return random.choice(self.random)
