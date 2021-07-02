from string import digits
from constants import DICTIONARY
import math
import re
from collections import Counter
import os
from pydub import AudioSegment
from praatio.tgio import openTextgrid

WORD = re.compile(r"\w+")


def get_predicted_phonemes():
    phs = open("output/predicted.txt").readlines()
    phs = [ph.replace("sil", "").strip() for ph in phs]
    return phs


def get_original_phonemes():
    phs = open("output/original.txt").readlines()
    phs = [ph.replace("sil", "").strip() for ph in phs]
    return phs


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    Human sorting
    """
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def get_words():
    lines = open("timit/data/predict/phn_text").readlines()
    # human sorting
    lines.sort(key=natural_keys)
    lines = ["".join(line.split(" ")[:1]) for line in lines]
    words = []
    for line in lines:
        words.append("".join(line.split("_")[1:]))
    return words


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
        # with open("TIMIT/predict/{}.txt".format(filename), "w") as writer:
        with open("montreal-forced-aligner/data/{}.txt".format(filename), "w") as writer:
            writer.write(text)
        return {"Message": 200, "text": text}
    else:
        return {"Text or filename missing": 400}


def generate_word_level_audios(name=None):
    """
    split audio to words using textgrid file and save it in timit predict directory.
    """
    audio = AudioSegment.from_wav("montreal-forced-aligner/data/{}.wav".format(name))
    tg = openTextgrid("montreal-forced-aligner/textgrids/data/{}.TextGrid".format(name), readAsJson=False)
    # clean predict directory first
    os.system("rm TIMIT/predict/*.*")
    for index, entry in enumerate(tg.tierDict["words"].entryList):
        word = str(index) + "_" + entry.label
        # time in seconds
        start = entry.start * 1000
        end = entry.end * 1000

        chunk = audio[start:end]
        sound = chunk.set_frame_rate(16000).set_channels(1)
        silence = AudioSegment.silent(200)
        total = sound + silence
        total.export("TIMIT/predict/{}.wav".format(word), format="wav")
        with open("TIMIT/predict/{}.txt".format(word), "w") as writer:
            writer.write(entry.label)

    return {"message": 200}
