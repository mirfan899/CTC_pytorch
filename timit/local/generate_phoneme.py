# encoding=utf-8

import os
import sys
import argparse
from string import digits
import json

librispeech = open("local/librispeech-lexicon.json", "r")
DICTIONARY = json.load(librispeech)

parser = argparse.ArgumentParser(description="Normalize the phoneme on TIMIT")
parser.add_argument("--src", default='./data/predict/wrd_text', help="The source file to mapping")
parser.add_argument("--tgt", default='./data/predict/phn_text', help="The target file after mapping")


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


def main():
    args = parser.parse_args()
    with open(args.src, 'r') as rf, open(args.tgt, 'w') as wf:
        for line in rf.readlines():
            line = line.strip().split(' ')
            uttid, utt = line[0], " ".join(line[1:])

            map_utt = get_phonemes_only(utt)
            map_utt = "sil " + " ".join(map_utt).lower() + " sil"
            wf.writelines(uttid + ' ' + map_utt + '\n')


if __name__ == "__main__":
    main()
