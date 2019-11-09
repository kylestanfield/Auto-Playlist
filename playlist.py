import configparser
from xml.etree import ElementTree
import requests
import spotipy
import spotipy.util as util

def get_top_tracks(user, api_key, period):
    """Query last.fm for the user's top 50 tracks over the period.

    Songs are returned as an array of tuples, consisting of song title
    and artist name.
    """

    api_method = 'method=user.gettoptracks'

    last_fm_url = 'http://ws.audioscrobbler.com/2.0/'
    api_call_url = (last_fm_url + '?' + api_method \
                     + '&user=' + user + '&period=' + period \
                    + '&api_key=' + api_key).encode('utf-8')
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'From': 'stanfield@ucsb.edu'
    }
    api_response = requests.get(api_call_url, headers=headers)

    tree = ElementTree.fromstring(api_response.content)

    track_list = []
    if tree.attrib['status'] == 'ok':
        for i in range(50):
            track_list.append((tree[0][i][0].text, tree[0][i][6][0].text))
    else:
        print("Not able to retrieve tracks from Last.fm")
        return -1
    return track_list

def get_playlist_id(playlist_name, playlists):
    """Search a list of Spotify playlists in JSON for the given playlist name."""

    for playlist in playlists['items']:
        if playlist['name'] == 'Auto Playlist':
            return playlist['id']
    return ''

def get_track_ids(track_list, spotipy_obj):
    """Search Spotify for songs in the given list, by title and artist.
    Return an array of the tracks' Spotify IDs."""

    result = []
    for track in track_list:
        song = track[0]
        artist = track[1]
        search_res = spotipy_obj.search(song + ' ' + artist)
        for item in search_res['tracks']['items']:
            if item['name'] == song and item['artists'][0]['name'] == artist:
                result.append(item['id'])
                break
    return result

def search_and_make_playlist(user, spotify_secret, playlist_name, tracks):
    """Handle the authentication, song searching, and playlist creation through
    the Spotify API."""

    client = 'd753fecc04794934af9be02665e740aa'
    redirect = 'http://kylestanfield.net'
    scope = 'playlist-modify-public' #All this info is for the authorization token

    token = util.prompt_for_user_token(user, scope, client_id=client,
                                       client_secret=spotify_secret, redirect_uri=redirect)
    if not token:
        print("Could not authenticate " + user + ".")
        return 1

    sp = spotipy.Spotify(auth=token)
    #Read user Playlists, check if Auto-Playlist exists, get ID
    #Otherwise, make a new playlist 
    #Then add the new songs for both cases

    playlists = sp.current_user_playlists()
    auto_playlist_id = get_playlist_id(playlist_name, playlists)

    if not auto_playlist_id: #no auto playlist
        new_pl = sp.user_playlist_create(user, playlist_name)
        auto_playlist_id = new_pl['id']
    #Now use spotify API to search for the track IDs of top tracks
    result = get_track_ids(tracks, sp)

    results = sp.user_playlist_replace_tracks(user, auto_playlist_id, result)

def main():
    """Get top tracks from last.fm, then send them to the Spotify logic."""

    #First, parse the last.fm API key from the local config file
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    last_fm_key = parser.get('API Keys', 'last_fm')

    tracks = get_top_tracks('sonfon', last_fm_key, '7day')

    user = 'kylesonfon' #DEBUG
    playlist_name = 'Auto Playlist'
    spotify_secret = parser.get('API Keys', 'spotify')

    search_and_make_playlist(user, spotify_secret, playlist_name, tracks)

if __name__ == '__main__':
    main()
