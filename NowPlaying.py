import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
import spotipy
import spotipy.util as util
import requests
import xmltodict
import pprint

scope='playlist-read-private playlist-modify-private playlist-modify-public'
username=<YOUR_SPOTIFY_USERNAME>
playlist=<TARGET_SPOTIFY_PLAYLIST>
token=''

def renew():
	global token
	token = util.prompt_for_user_token(username,scope,client_id='<SPOTIFY_CLIENT_ID>',client_secret='<SPOTIFY_APP_CLIENT_SECRET>',redirect_uri='<SPOTIFY_APP_CALLBACK>')
	return

previous= 'none'
interval  = 150
renew()
if token:
	sp = spotipy.Spotify(auth=token)
	while (1):
		url = 'http://vodafone.fm/nowplaying.xml?_=' + str(int(time.time())) + '666'
		page = requests.get(url)
		doc = xmltodict.parse(page.content)
		try:
			song = doc['RadioInfo']['Table']['DB_DALET_TITLE_NAME']
			artist = doc['RadioInfo']['Table']['DB_DALET_ARTIST_NAME']
		except KeyError:
			song = "VodafoneFM"
		if (song == 'VodafoneFM'):
			# nothing is playing
			pass
		elif (song == previous):
			# same song is playing
			pass
		else:
			previous=song
			search_str = 'track:"'+song+'"+artist:"'+artist.replace("&",'" "')+'"'
			# todo: improve search & replace for common search string bumps
			try:
				result = sp.search(search_str,type='track',market='PT')
			except spotipy.client.SpotifyException:
				# most likely an expired token. spotipy doesn't refresh token transparently, yet, so we brute force it
				renew()
				sp = spotipy.Spotify(auth=token)
				result = sp.search(search_str,type='track',market='PT')
			if (result['tracks']['items']):
				sp.user_playlist_remove_all_occurrences_of_tracks(username,playlist,[result['tracks']['items'][0]['uri']])
				sp.user_playlist_add_tracks(username,playlist,[result['tracks']['items'][0]['uri']])
				print "Added: "+artist+" - "+song
			else:
				print "Song does not exist: "+artist+" - "+song
		time.sleep(interval)
else:
	print "Can't get token for ",username
