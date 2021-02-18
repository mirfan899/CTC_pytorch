from string import digits

from constants import DICTIONARY


def clean(sentence=None):
    return sentence.replace("sil", "")


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
        p = ph.translate(str.maketrans('', '', digits))
        phonemes_only_cleaned.append(p)

    return phonemes_only_cleaned