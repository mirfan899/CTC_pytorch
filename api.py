import os
import string
import werkzeug
from flask import Flask
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
from accuracy import PhonemeAccuracy

from timit.myutils import generate_predicted_phonemes, save_paragraph, get_predicted_phonemes
UPLOAD_FOLDER = 'TIMIT/predict/'

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
            os.system("rm TIMIT/predict/*")
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

            os.system("./predict.sh")

            result = {}
            predicted_phonemes = get_predicted_phonemes()

            paragraph_accuracy = PhonemeAccuracy(original=paragraph, predicted=predicted_phonemes).accuracy()
            response["phonemes_accuracy"] = paragraph_accuracy
            response["status"] = 200
            response["result"] = result
        else:
            response["message"] = 'upload a .wav or .mp3 file'
            response["status"] = 404

        return response


api.add_resource(Accuracy, '/api/accuracy')

if __name__ == '__main__':
    app.run(debug=True, threaded=False, processes=1)
