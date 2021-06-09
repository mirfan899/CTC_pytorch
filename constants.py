import json
import os

librispeech = open("librispeech-lexicon.json", "r")
DICTIONARY = json.load(librispeech)

# ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root

MAP_DICTIONARY = {
    "aa": "aa", "ao": "aa",
    "ah": "ah", "ax": "ah", "ax-h": "ah",
    "er": "er", "axr": "er",
    "hh": "hh", "hv": "hh",
    "ih": "ih", "ix": "ih",
    "l": "l", "el": "l",
    "m": "m", "em": "m",
    "n": "n", "en": "n", "nx": "n",
    "ng": "ng", "eng": "ng",
    "sh": "sh",
    "zh": "zh",
    "uw": "uw", "ux": "uw",
    "pcl": "sil", "tcl": "sil", "kcl": "sil", "bcl": "sil", "dcl": "sil", "gcl": "sil", "h#": "sil", "pau": "sil","epi": "sil",
    "q": "",
    "w": "w",
    "dh": "dh",
    "f": "f",
    "iy": "iy",
    "y": "y",
    "t": "t",
    "dx": "dx",
    "ey": "ey",
    "k": "k",
    "oy": "oy",
    "ow": "ow",
    "r": "r",
    "ay": "ay",
    "p": "p",
    "aw": "aw",
    "z": "z",
    "v": "v",
    "ch": "ch",
    "s": "s",
    "jh": "jh",
    "th": "th",
    "g": "g",
    "eh": "eh",
    "d": "d",
    "ae": "ae",
    "b": "b",
    "uh": "uh",
}
