import responder
import random
import dictionary
import analyzer
import patternItem
# *アぺイリアの本体クラス


class Apeiria(object):
    def __init__(self, name):
        self.name = name
        self.dictionary = dictionary.Dictionary()
        self.emotion = Emotion(self.dictionary.pattern)
        self.res_repeat = responder.RepeatResponder("Repeat?")
        self.res_random = responder.RandomResponder(
            "Random", self.dictionary.random)
        self.res_pattern = responder.PatternResponder(
            "Pattern", self.dictionary.pattern, self.dictionary.random)
        self.res_template = responder.TemplateResponder(
            "Template", self.dictionary.template, self.dictionary.random)
        self.res_markov = responder.MarcovResponder(
            "Markov", self.dictionary.markovsentence, self.dictionary.random)

    def dialogue(self, input):
        self.emotion.update(input)
        parts = analyzer.analyze(input)
        x = random.randint(1, 100)
        if x <= 85:
            self.responder = self.res_pattern
        elif 80 <= x <= 85:
            self.responder = self.res_template
        elif 86 <= x <= 90:
            self.responder = self.res_random
        elif 91 <= x <= 95:
            self.responder = self.res_markov
        else:
            self.responder = self.res_repeat
        resp = self.responder.response(input, self.emotion.mood, parts)
        fc = patternItem.response_face.face_check_num(self, resp)
        resp2 = patternItem.response_face.face_check(self, resp)
        self.dictionary.study(input, parts)
        print(resp2)

        # 高感度確認用
        print(self.emotion.mood)
        print(fc)
        return resp2, fc

    def save(self):
        self.dictionary.save()

    def get_responder_name(self):
        return self.responder.name

    def get_name(self):
        return self.name


class Emotion:
    MOOD_MIN = -15
    MOOD_MAX = 15
    MOOD_RECOVERY = 0.5

    def __init__(self, pattern):
        self.pattern = pattern
        self.mood = 0

    def update(self, input):
        if self.mood < 0:
            self.mood += Emotion.MOOD_RECOVERY
        elif self.mood > 0:
            self.mood -= Emotion.MOOD_RECOVERY

        for ptn_item in self.pattern:
            if ptn_item.match(input):
                self.adjust_mood(ptn_item.modify)
                break

    def adjust_mood(self, val):
        self.mood += int(val)
        if self.mood > Emotion.MOOD_MAX:
            self.mood = Emotion.MOOD_MAX
        elif self.mood < Emotion.MOOD_MIN:
            self.mood = Emotion.MOOD_MIN
