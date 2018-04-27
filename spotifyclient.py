from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import time
import sys
import pprint

clientid = '80c0be28d7c244148044c27a87653074'
secret = '3b7ff2e371174bd8891b51744c06488f'

def getArtistProperties(artist_name, genres):
    #Takes in a string for artist name and list of allowed genres
    #Returns relevant genres for the first result in a search for the artist,
    #and None if the search is unsuccessful
    client_credentials_manager = SpotifyClientCredentials(clientid, secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace=False
    results = sp.search(q=artist_name, limit=1, type='artist')
    popularity = 0
    try:
        popularity = results['artists']['items'][0]['popularity']
    except Exception as e:
        print("Error getting popularity")
        popularity = 0
        raise

    uri = None
    for i, t in enumerate(results['artists']['items']):
        uri = t['uri']

    if not uri:
        return None

    artist = sp.artist(uri)
    matches = []
    for genre in artist['genres']:
        matches.append(genre)

    if len(matches) == 0:
        matches = None
    return matches


def getAlbumProperties(album_name):
    client_credentials_manager = SpotifyClientCredentials(clientid, secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace=False
    results = sp.search(q=album_name, limit=1, type='album')
    return results


def getSongProperties(song_name, artist_name):
    #print("Song Properites search:", song_name, artist_name)
    client_credentials_manager = SpotifyClientCredentials(clientid, secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace=False
    results = sp.search(q=song_name + " " + artist_name, limit=20, type='track')
    tracks = results['tracks']['items']
    toRet = None
    for item in tracks:
        artists = item['artists']
        for artistInfo in artists:
            if(artist_name.lower() in artistInfo['name'].lower()):
                duration = item['duration_ms']
                popularity = item['popularity']
                toRet = {"duration_ms": duration, "popularity" : popularity}
                break
        if toRet != None:
            break
    return toRet
