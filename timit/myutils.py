import json
from string import digits
from constants import DICTIONARY
import math
import re
from collections import Counter
import os
import subprocess
import uuid


WORD = re.compile(r"\w+")


def get_predicted_phonemes():
    phs = open("output/predicted.txt").readlines()
    return phs[0]


def generate_predicted_phonemes():
    """just run the command run_pred.sh to generate the prediction file in output.
    First clean the output and predict directory
    """

    cmd = "cd ./timit/ && run_pred.sh"
    # os.system("cd ./timit/ && pwd")


    print("Running Phoneme process================================================")
    # process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    # process.wait()
    os.system("./run_pred.sh")

    return {"success": 200}


def clean(sentence=None):
    cleaned = sentence.replace("sil", "")
    cleaned = re.sub(" +", " ", cleaned)
    return cleaned.strip()


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


def text_to_vector(text=None):
    words = WORD.findall(text)
    return Counter(words)


def save_paragraph(text=None, filename=None):
    if text and filename:
        with open("TIMIT/predict/{}.txt".format(filename), "w") as writer:
            writer.write(text)
        return {"Message": 200, "text": text}
    else:
        return {"Text or filename missing": 400}
