import editdistance
from utils import clean

originals = list(filter(None, (line.strip() for line in open("output/original.txt"))))
predicted = list(filter(None, (line.strip() for line in open("output/predicted.txt"))))


for index, _ in enumerate(originals):
    # original = originals[index].translate(str.maketrans("", "", string.punctuation))
    # original = " ".join(get_phonemes_only(original)).lower()
    org = clean(originals[index])
    pred = clean(predicted[index])
    score = editdistance.eval(org, pred)
    per = (len(org) - score)/len(org)
    print("Percentage accuracy {}".format(per))