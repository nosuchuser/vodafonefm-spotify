import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
import spotipy
import spotipy.util as util
import requests
from lxml import html
import datetime

scope='playlist-read-private playlist-modify-private playlist-modify-public'
username=<YOUR_SPOTIFY_USERNAME>

token = util.prompt_for_user_token(username,scope,client_id='<SPOTIFY_CLIENT_ID>',client_secret='<SPOTIFY_APP_CLIENT_SECRET>',redirect_uri='<SPOTIFY_APP_CALLBACK>')
today = datetime.date.today()

c = 0
if token:
	sp = spotipy.Spotify(auth=token)           
	result = sp.user_playlist_create(username, today.strftime('%Y.%m')+' - VodafoneFM playlist', public=True)
	playlist = result['uri']
	page = requests.get('http://vodafone.fm')
	tree = html.fromstring(page.content)

	artists = tree.xpath('//span[@class="text artist"]/text()')
	songs = tree.xpath('//span[@class="text song"]/text()')

	while (cunt<len(artists)):
		search_str = 'track:"'+songs[c]+'"+artist:"'+artists[c].replace("&","")+'"'
		result = sp.search(search_str,type='track',market='PT')
		if (result['tracks']['items']):
			sp.user_playlist_add_tracks(username,playlist,[result['tracks']['items'][0]['uri']])
			print "Added: "+artists[c]+" - "+songs[c]
		else:
			print "Song does not Exist: "+artists[c]+" - "+songs[c]
		c+=1
else:
	print "Can't get token for ",username
