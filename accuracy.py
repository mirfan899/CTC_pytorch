import editdistance
from utils import get_phonemes_only, clean, get_score
import string

text = "go do you hear"
text = text.translate(str.maketrans('', '', string.punctuation))

predicted = "g ow sil iy uw y ih er"
original = " ".join(get_phonemes_only(text)).lower()

text = clean(text)
predicted = clean(predicted)

result = {}
for word in text.split():
    phonemes = get_phonemes_only(word)[0].lower()
    ph_size = len(phonemes)
    predicted_phonemes = predicted[:ph_size].strip()
    print("Word level phoneme Accuracy")
    wd = editdistance.eval(phonemes, predicted_phonemes)
    # print((wd/len(phonemes))*100)
    if len(phonemes.split()) == len(predicted_phonemes.split()):
        for index, p in enumerate(phonemes.split()):
            pd = editdistance.eval(p, predicted_phonemes.split()[index])
            score = get_score(p, pd)
            result[p] = score
    else:
        predicted_phonemes_ = predicted_phonemes.split()
        size = len(predicted_phonemes_)
        phonemes_ = phonemes.split()
        for index, p in enumerate(phonemes_):
            if index < size:
                pd = editdistance.eval(p, predicted_phonemes_[index])
                score = get_score(p, pd)
                result[p] = score
            else:
                pd = len(p)
                score = get_score(p, pd)
                result[p] = score
    predicted = predicted[ph_size:]
# original = " ".join(get_phonemes_only(text)).lower()
# original = "sil g ow d uw y uw hh iy r sil"


print(result)
# distance = editdistance.eval(original.split(), predicted.split())
#
# print(original)
# print(predicted)
# print("PER")
# per = ((len(original) - distance)/len(original))*100
#
# print(100-per)
