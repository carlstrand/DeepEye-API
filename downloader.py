import requests
import urllib.request
from tinydb import TinyDB, Query
from config import *

db = TinyDB(db_name)

with open('list.txt', 'r') as f:
	for line in f.readlines():
		user_id, user_fb = line.split('$')
		user_id, user_fb = user_id.strip(), user_fb.strip()

		# Download user's data
		user_data_url = 'https://graph.facebook.com/%s?fields=picture.width(9999).height(9999).type(large),gender,name&access_token=%s' % (user_id, access_token)
		user_data = requests.get(user_data_url).json()

		name = user_data['name']
		picture_url = user_data['picture']['data']['url']
		urllib.request.urlretrieve(picture_url, download_folder + '/' + user_id + '.jpg') # Download profile picture

		# Add entry into a database
		db.insert({'user_id': user_id, 'user_name': name, 'user_fb': user_fb})