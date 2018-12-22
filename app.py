from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
import face_recognition
from config import *
import io, base64
import itertools
import json
from PIL import Image

app = Flask(__name__)

# Initialize DB
db = TinyDB(db_name)
# Create list of all users ids
db_data = db.all()

print('Initializing ML model...')
# Load sample pictures and learn how to recognize it
known_face_encodings = []
known_face_names = []
for user in db_data:
	user_id = user['user_id']
	user_name = user['user_name']
	user_fb = user['user_fb']
	sample = face_recognition.load_image_file('%s/%s.jpg' % (download_folder, user_id))
	sample_encoding = face_recognition.face_encodings(sample)[0]
	known_face_encodings.append(sample_encoding)
	known_face_names.append(user_name)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
print('Done.')

@app.route('/recognize', methods=['GET', 'POST'])
def recognize():
	img_b64 = json.loads(request.data)['image']
	img_data = base64.b64decode(img_b64)
	im = Image.open(io.BytesIO(img_data))
	im.thumbnail((1024, 1024))
	im = im.rotate(-90)

	stdout = io.BytesIO()
	im.save(stdout, format='JPEG')
	hex_data = stdout.getvalue()

	unknown_face = face_recognition.load_image_file(io.BytesIO(hex_data))
	unknown_face_encodings = face_recognition.face_encodings(unknown_face)

	recognized_faces = []
	for known_face_encoding, face_data in zip(known_face_encodings, db_data):
		for unknown_face_encoding in unknown_face_encodings:
			result = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding)
			if(result[0]):
				recognized_faces.append(face_data)			

	if(recognized_faces):
		return jsonify(recognized_faces)
	else:
		return jsonify('unknown face')

@app.route('/', methods=['GET'])
def main():
	return 'works'

if __name__ == '__main__':
	app.run(host='0.0.0.0')