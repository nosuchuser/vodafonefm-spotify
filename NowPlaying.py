import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
import spotipy
import spotipy.util as util
import requests
import xmltodict
import re
import htmlentitydefs, re

scope='playlist-read-private playlist-modify-private playlist-modify-public'
username=<YOUR_SPOTIFY_USERNAME>
playlist=<TARGET_SPOTIFY_PLAYLIST>
token=''

def renew():
	global token
	token = util.prompt_for_user_token(username,scope,client_id='<CLIENTID>',client_secret='<CLIENTSECRET>',redirect_uri='<CALLBACKURL>')
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
			vfmsong = str(doc['RadioInfo']['Table']['DB_DALET_TITLE_NAME'])
			vfmartist = str(doc['RadioInfo']['Table']['DB_DALET_ARTIST_NAME'])
		except KeyError:
			vfmsong = "VodafoneFM"

		if (vfmsong == 'VodafoneFM'):
			pass
		elif (vfmsong == previous):
			pass
		else:
			previous=vfmsong
			search_str = 'track:"'+vfmsong+'"+artist:"'+vfmartist.replace("&",'" "')+'"'
			try:
				result = sp.search(search_str,type='track',market='PT')
			except spotipy.client.SpotifyException:
				# most likely an expired token. spotipy doesn't refresh token transparently, yet, so we brute force it
				renew()
				sp = spotipy.Spotify(auth=token)
				result = sp.search(search_str,type='track',market='PT')
			if (result['tracks']['items']):
				try:
					sp.user_playlist_remove_all_occurrences_of_tracks(username,playlist,[result['tracks']['items'][0]['uri']])
					sp.user_playlist_add_tracks(username,playlist,[result['tracks']['items'][0]['uri']])
				except:
					print ("Exception caught on remove/add ["+vfmartist+"/"+vfmsong+"]")
			else:
				print "\nSong does not exist: "+vfmartist+" - "+vfmsong
		time.sleep(interval)
else:
	print "Can't get token for ",username
