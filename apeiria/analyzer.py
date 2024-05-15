import re
from janome import tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
from janome.tokenizer import Tokenizer


def analyze(text):
    tokenizer = Tokenizer()
    token_filters = [CompoundNounFilter()]
    analyzer = Analyzer(tokenizer=tokenizer, token_filters=token_filters)
    result = []
    for token in analyzer.analyze(text):
        result.append([token.surface, token.part_of_speech])
    return (result)


def keyword_check(part):
    return re.match('名詞,(一般|固有名詞|サ変接続|形容動詞語幹)', part)


def parse(text):
    t = tokenizer.Tokenizer()
    tokens = t.tokenize(text)
    result = []
    for token in tokens:
        result.append(token.surface)
    return (result)


def keigo(text):
    t = tokenizer.Tokenizer()
    tokens = t.tokenize(text)
    msg = ""
    for token in tokens:
        parts = token.part_of_speech.split(',')
        parts2 = token.base_form.split(',')
        if (parts[0] == '助動詞'):
            if (parts2[0] == "ない" or parts2[0] == "ます" or parts2[0] == "ござる"):
                print("c")
            else:
                token.surface = 'です'
                token.base_form = 'です'
                token.reading = 'デス'
                token.phonetic = 'デス'
        elif (parts[0] == '助詞' and parts[1] == '終助詞'):
            token.surface = 'です'
            token.base_form = 'です'
            token.reading = 'デス'
            token.phonetic = 'デス'
        elif (parts2[0] == "私" or parts2[0] == "僕" or parts2[0] == "俺" or parts2[0] == "わたし" or parts2[0] == "ぼく" or parts2[0] == "おれ"):
            token.surface = 'アぺイリア'
            token.base_form = 'アぺイリア'
            token.reading = 'アぺイリア'
            token.phonetic = 'アぺイリア'
        elif (parts[0] == '助詞' and parts[1] == '副助詞／並立助詞／終助詞'):
            token.surface = ''
            token.base_form = ''
            token.reading = ''
            token.phonetic = ''
        msg = msg+token.surface
        msg = msg.replace("ですです", "です")
    return (msg)
