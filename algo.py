import re


class PhonemeScore:
    def __init__(self, words, op, pp):
        self.words = words
        self.pp = pp
        self.op = op

    def score(self):
        result = {}
        for index, word in enumerate(self.words):
            word_score = {}
            phoneme_score = {}
            if self.op[index] == self.pp[index]:
                for ph in self.op[index].split():
                    phoneme_score[ph] = 100
            elif self.pp[index] in self.op[index]:
                # handle phonemes where whole phoneme is there but starting or ending phoneme is missing by prediction
                op = self.op[index]
                pp = self.pp[index]
                grp = re.search(pp, op)
                matched_phonemes = op[grp.start():grp.end()]
                for ph in matched_phonemes.split():
                    phoneme_score[ph] = 100
                remaining_phonemes = op.replace(op[grp.start(): grp.end()], "").split()
                for ph in remaining_phonemes:
                    phoneme_score[ph] = 0
            else:
                # find predicted phoneme from original by matching the indexes and score it 100 else 20 for now.
                pp = self.pp[index].split()
                op = self.op[index]
                for p in pp:
                    grp = re.search(p, op)
                    if grp:
                        if self.op[index][grp.start(): grp.end()] == self.pp[index][grp.start(): grp.end()]:
                            phoneme_score[p] = 100
                        else:
                            phoneme_score[p] = 20
                    else:
                        phoneme_score[p] = 0

            # handle if no match found
            if not phoneme_score:
                word_score["word_accuracy"] = 0
                for ph in self.op[index].split():
                    phoneme_score[ph] = 0
            word_score["word_accuracy"] = round(sum(phoneme_score.values()) / (len(phoneme_score.values()) * 100), 2)
            word_score["word"] = word
            word_score["phoneme_accuracy"] = phoneme_score
            result[str(index)] = word_score
        return result


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    Human sorting
    """
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def get_predicted_phonemes():
    lines = open("output/predicted.txt").readlines()
    lines.sort(key=natural_keys)
    phs = [" ".join(line.split(" ")[1:]) for line in lines]
    phs = [ph.replace("sil", "").strip() for ph in phs]
    return phs


def get_original_phonemes():
    lines = open("output/original.txt").readlines()
    lines.sort(key=natural_keys)
    phs = [" ".join(line.split(" ")[1:]) for line in lines]
    phs = [ph.replace("sil", "").strip() for ph in phs]
    return phs


def get_words():
    lines = open("timit/data/predict/phn_text").readlines()
    # human sorting
    lines.sort(key=natural_keys)
    lines = ["".join(line.split(" ")[:1]) for line in lines]
    words = []
    for line in lines:
        words.append("".join(line.split("_")[1:]))
    return words


words = get_words()
original_phonemes = get_original_phonemes()
predicted_phonemes = get_predicted_phonemes()
# result = {}
result = PhonemeScore(words, original_phonemes, predicted_phonemes).score()
print(result)
# for index, word in enumerate(words):
#     word_score = {}
#     phoneme_score = {}
#     if original_phonemes[index] == predicted_phonemes[index]:
#         for ph in original_phonemes[index].split():
#             phoneme_score[ph] = 100
#     elif predicted_phonemes[index] in original_phonemes[index]:
#         # handle phonemes where whole phoneme is there but starting or ending phoneme is missing by prediction
#         op = original_phonemes[index]
#         pp = predicted_phonemes[index]
#         grp = re.search(pp, op)
#         matched_phonemes = op[grp.start():grp.end()]
#         for ph in matched_phonemes.split():
#             phoneme_score[ph] = 100
#         remaining_phonemes = op.replace(op[grp.start(): grp.end()], "").split()
#         for ph in remaining_phonemes:
#             phoneme_score[ph] = 0
#     else:
#         # find predicted phoneme from original by matching the indexes and score it 100 else 20 for now.
#         pp = predicted_phonemes[index].split()
#         op = original_phonemes[index]
#         for p in pp:
#             grp = re.search(p, op)
#             if grp:
#                 if predicted_phonemes[index][grp.start(): grp.end()] == original_phonemes[index][
#                                                                         grp.start(): grp.end()]:
#                     phoneme_score[p] = 100
#                 else:
#                     phoneme_score[p] = 20
#             else:
#                 phoneme_score[p] = 0
#
#     # handle if no match found
#     if not phoneme_score:
#         word_score["word_accuracy"] = 0
#         for ph in original_phonemes[index].split():
#             phoneme_score[ph] = 0
#     word_score["word_accuracy"] = round(sum(phoneme_score.values()) / (len(phoneme_score.values()) * 100), 2)
#     word_score["word"] = word
#     word_score["phoneme_accuracy"] = phoneme_score
#     result[str(index)] = word_score

print(result)
