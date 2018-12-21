from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
import face_recognition
from config import *

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
	return 'sample'

@app.route('/', methods=['GET'])
def main():
	return 'works'

if __name__ == '__main__':
	app.run(host='0.0.0.0')