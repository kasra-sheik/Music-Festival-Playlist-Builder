import spotipy 

SPOTIFY_ACCESS_TOKEN = "BQCfpJnKD1QMQTipFXx_YX6xW2CD2_WV88SLSSgsSPHNuaf-WRSJdxsE0t2rJYxCGqaxe01v3l8F-4NhnZqRmdi-3FtORYF1EoKz8dGAqQpzIAIgTS-T3hQ5Us_n55990VhgVEeBoznwf8uZ80e5p9NyFgOLa4utW4ns7zBUn8Mc_P12R949nKusnuxE04iQ-K1KoZvpgTT1HC__kMxObgWtD_PIWphq-MUHD3k4i30EOR3Me6FfcIvht8ywIUqJaw"
spotify = spotipy.Spotify(SPOTIFY_ACCESS_TOKEN)

user_id = spotify.current_user()['id']

playlists = spotify.user_playlists(user_id)

while len(playlists['items']) > 0:
	print("yo")

	for playlist in playlists['items']:
		delete_id = playlist['id']

		spotify.user_playlist_unfollow(user_id, delete_id)

	playlists = spotify.user_playlists(user_id)
