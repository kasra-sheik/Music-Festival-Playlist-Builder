from bs4 import BeautifulSoup
import requests
import spotipy
import psycopg2
import edit_distance

#might want to add a list of websites for broader reach 
FESTIVALS_PAGE = "https://www.jambase.com/festivals"

SPOTIFY_ACCESS_TOKEN = os.environ['spotify_token']
spotify = spotipy.Spotify(SPOTIFY_ACCESS_TOKEN)

SPOTIFY_USER_ID = spotify.current_user()['id']

class Festival(object):
    def __init__(self, name, artists, link):
        self.name = name 
        self.artists = artists
        self.link = link 
    def __str__(self):
        return "{}: {}".format(self.name, self.artists)
    def __repr__(self):
        return str(self)

def setup_db():
    db_name = os.environ['dw_database']
    db_user = os.environ['dw_user']
    db_pass = os.environ['dw_password']
    db_host = os.environ['dw_host']
    db_port = os.environ['dw_port']

    db = psycopg2.connect(
        user = db_user,
        password = db_pass,
        host = db_host,
        port = db_port,
        database = db_name)

    return db.cursor(), db

def get_supporting_acts(festival_link):
    festival_page = requests.get(festival_link, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}) 
    festival_lineup = []

    soup = BeautifulSoup(festival_page.content, 'html.parser')
    lineup = soup.find('ul', {'class' : 'list-inline list-festival-lineup'})

    if lineup is None:
        return []

    acts = lineup.find_all('span', {'itemprop' : 'name'})

    for act in acts:
        try:
            artist = act.contents[0].strip()
            festival_lineup.append(artist)
        except:
            pass

    return festival_lineup

#checks db to verify this is a new playlist 
def is_new_festival(festival_name):
    DB.execute("SELECT * from PLAYLISTS WHERE name='{}'".format(festival_name))
    exists = DB.fetchone()
    return exists is None 

#scrapes web for new music festivals -> list of festival objects
def get_festival_lineups():
    festivals = []

    festivals_page = requests.get(page, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
    soup = BeautifulSoup(festivals_page.content, 'html.parser')

    #this is pretty hardcodey - might want to add more robust checks in the future
    festival_elements = soup.find_all('div', {'class' : 'col-xs-10 col-sm-12'})
    
    if(festival_elements == []):
        break

    for festival_data in festival_elements:
        festival_name = list(festival_data.find('span').children)[0].strip()
        # print(festival_name)

        if(not is_new_festival(festival_name)):
            break 

        festival_link = festival_data.find('a', {'class' : 'h3 post-title break-word'})['href'].strip()
        festival_artists = get_supporting_acts(festival_link)
        
        new_festival = Festival(festival_name, festival_artists, festival_link)
        festivals.append(new_festival)

    return festivals

#get top songs for an artist
def get_top_songs(artist):
    top_songs = []

    #might want to have this number be dynamic based on attribute ie. set time/popularity? 
    song_count = 5

    artist_search = spotify.search(q='artist:' + artist, type='artist')

    if len(artist_search['artists']['items']) == 0:
        return []

    result_name = artist_search['artists']['items'][0]['name']

    #comparing edit distance might be useful
    if(result_name.lower() == artist.lower() or edit_distance.SequenceMatcher(artist.lower(), result_name.lower()).ratio() >= 66):

        artist_id = artist_search['artists']['items'][0]['id']
        top_tracks = spotify.artist_top_tracks(artist_id)['tracks']

        for track in top_tracks:
            top_songs.append(track['id'])
            
            if len(top_songs) >= song_count:
                break
    else:
        print("error could not find artist spotify name {} scraped name {}".format(result_name, artist))
    return top_songs

def create_festival_playlist(festival):
    playlist_name = festival.name
    playlist_description = "Generated Festival Playlist: Find more at {}".format(festival.link)

    playlist_songs = []

    for artist in festival.artists:
        top_songs = get_top_songs(artist)
        playlist_songs += top_songs

    try: 
        new_playlist = spotify.user_playlist_create(SPOTIFY_USER_ID, playlist_name, public=True)
        
        #spotify's api rate limits, so we have to batch this request
        add_count = 0 
        while(add_count < len(playlist_songs)):
            batch = add_count + 100 

            if batch >= len(playlist_songs):
                spotify.user_playlist_add_tracks(SPOTIFY_USER_ID, new_playlist['id'], playlist_songs[add_count:])
            else:
                spotify.user_playlist_add_tracks(SPOTIFY_USER_ID, new_playlist['id'], playlist_songs[add_count:batch])

            add_count = batch 
       
        DB.execute("INSERT INTO PLAYLISTS (name, spotify_id) VALUES ('{}', '{}')".format(playlist_name, new_playlist['id']))
        DBCONN.commit()

        #TODO: figure out why we cant add playlist description on creation 
        # spotify.user_playlist_change_details(SPOTIFY_USER_ID, new_playlist['id'], description=playlist_description)
    except Exception as playlist_creation_error:
        print("error creating new festival playlist. {}".format(playlist_creation_error))

def generate_playlists():
    new_festivals = get_festival_lineups()

    for festival in new_festivals:
        create_festival_playlist(festival)

DB, DBCONN = setup_db()

if __name__ == '__main__':
    generate_playlists()
