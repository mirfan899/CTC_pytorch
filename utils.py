from string import digits
from constants import DICTIONARY
import math
import re
from collections import Counter

WORD = re.compile(r"\w+")


def clean(sentence=None):
    cleaned = sentence.replace("sil", "")
    cleaned = re.sub(" +", " ", cleaned)
    return cleaned


def get_score(phoneme, distance):
    maximum = max(len(phoneme), distance)
    minimum = min(len(phoneme), distance)
    score = ((maximum - minimum) / maximum) * 100
    return score


def get_phonemes_only(sentence):
    words = sentence.upper().split()
    phonemes = []
    phonemes_only = []
    for word in words:
        if word in DICTIONARY.keys():
            phonemes.extend(DICTIONARY[word].split())
            phonemes_only.append(DICTIONARY[word])
    phonemes_only_cleaned = []
    for ph in phonemes_only:
        p = ph.translate(str.maketrans("", "", digits))
        phonemes_only_cleaned.append(p)

    return phonemes_only_cleaned


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)
