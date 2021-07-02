import os
import re
import string
import werkzeug
from flask import Flask
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
from timit.myutils import save_paragraph, get_predicted_phonemes, \
    generate_word_level_audios, get_original_phonemes, get_words

# UPLOAD_FOLDER = 'TIMIT/predict/'
UPLOAD_FOLDER = 'montreal-forced-aligner/data/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)


ALLOWED_FILES = [".wav", ".mp3"]
parser = reqparse.RequestParser()

parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
parser.add_argument('paragraph', type=str, help="provide sentence of audio being uploaded.")


class Accuracy(Resource):
    def get(self):
        return {"message": "Welcome to focusmore API", "status": 200}

    def post(self):
        response = {}
        data = parser.parse_args()
        if data['file'] == "" or data["paragraph"] == "":
            return {
                'message': "File or paragraph missing",
                'status': 400
            }
        file = data['file']
        # clean string
        paragraph = data['paragraph'].translate(str.maketrans('', '', string.punctuation))
        filename = secure_filename(file.filename)
        extension = os.path.splitext(filename)[1]
        name = os.path.splitext(filename)[0]
        result = {}
        if extension in ALLOWED_FILES:
            # os.system("rm TIMIT/predict/*")
            os.system("rm montreal-forced-aligner/data/*")
            if extension in [".mp3"]:
                mp3 = name + "{}".format(extension)
                wav = name + ".wav"
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                mp3_path = os.path.join(UPLOAD_FOLDER, mp3)
                wav_path = os.path.join(UPLOAD_FOLDER, wav)
                file.save(mp3_path)
                os.system("ffmpeg -i {} -ar 16000 {}".format(mp3_path, wav_path))
                os.system("rm {}".format(mp3_path))
            elif extension in [".wav"]:
                unique_filename = name + "{}".format(extension)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))

            save_paragraph(paragraph, name)
            # run shell script using this function and get the message.

            os.system("montreal-forced-aligner/bin/mfa_align montreal-forced-aligner/data/ montreal-forced-aligner/dict/librispeech-lexicon.txt montreal-forced-aligner/pretrained_models/english.zip montreal-forced-aligner/textgrids/")
            result = {}
            message = generate_word_level_audios(name)
            # run phoneme prediction model
            os.system("./predict.sh")
            predicted_phonemes = get_predicted_phonemes()
            original_phonemes = get_original_phonemes()
            words = get_words()

            for index, word in enumerate(words):
                word_score = {}
                phoneme_score = {}
                if original_phonemes[index] == predicted_phonemes[index]:
                    for ph in original_phonemes[index].split():
                        phoneme_score[ph] = 100
                    word_score["phoneme_accuracy"] = phoneme_score
                    word_score["word_accuracy"] = 100
                else:
                    # find predicted phoneme from original by matching the indexes and score it 100 else 20 for now.
                    pp = predicted_phonemes[index].split()
                    op = original_phonemes[index]
                    for p in pp:
                        grp = re.search(p, op)
                        if grp:
                            if predicted_phonemes[index][grp.start(): grp.end()] == original_phonemes[index][grp.start(): grp.end()]:
                                phoneme_score[p] = 100
                            else:
                                phoneme_score[p] = 20
                        else:
                            phoneme_score[p] = 0
                    if phoneme_score:
                        word_score["phoneme_accuracy"] = phoneme_score
                        word_score["word_accuracy"] = round(
                            sum(phoneme_score.values()) / (len(phoneme_score.values()) * 100), 2)
                    else:
                        word_score["word_accuracy"] = 0
                        for ph in original_phonemes[index].split():
                            phoneme_score[ph] = 0
                        word_score["phoneme_accuracy"] = phoneme_score
                word_score["word"] = word
                result[str(index)] = word_score

            response["status"] = 200
            response["result"] = result
        else:
            response["message"] = 'upload a .wav or .mp3 file'
            response["status"] = 404

        return response


api.add_resource(Accuracy, '/api/accuracy')

if __name__ == '__main__':
    app.run(debug=True, threaded=False, processes=1)
