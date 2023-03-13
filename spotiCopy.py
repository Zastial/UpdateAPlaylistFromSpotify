import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv
import os

SPOTIPY_CLIENT_ID = '610313e73c6d4333bf2831d16208d75f'
SPOTIPY_CLIENT_SECRET = '81527ba3f7844a8bb7c9ada01528dc74'
REDIRECT_URL = 'http://localhost:8888/callback'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope = "playlist-read-private playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private",
        redirect_uri=REDIRECT_URL,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
    )
)

sp.user = "s7df1bggy7vp04apvg6dglu0t" #C'est moi wesh

def get_playlist_tracks(username,playlist_id): #Get every songs from a playlist (spotipy allows only 100 songs/request)
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def findAndAdd(phantasma, findings):
    try:
        with open('PhanSongs.csv', 'r') as f:
            writer = csv.reader(f)

            phantasmaSongs = []
            for row in writer:
                phantasmaSongs.append(row) if row != [] else None
    except:
        print("Erreur : Impossible d'ouvrir le fichier")
        return


    new_songs = []

    phantasmaPlaylist = list(get_playlist_tracks(sp.user,phantasma['id']))
    alreadyInPhantasma=[]
    alreadyInPhantasmaID=[]
    for val in phantasmaPlaylist:
        alreadyInPhantasma.append(val['track']['name'])
        alreadyInPhantasmaID.append(val['track']['id'])


    newMoinsPlaylist = []
    for values in phantasmaSongs:
        if values[1] not in alreadyInPhantasmaID:
            newMoinsPlaylist.append(values[0])

    playlists = sp.current_user_playlists()['items']
    for i in range(len(playlists)):
        if playlists[i]['name'] == "Plus":
            plusPlaylist = list(get_playlist_tracks(sp.user,playlists[i]['id']))
            indexPlusPlaylists = i
        if playlists[i]['name'] == "Moins":
            moinsPlaylist = list(get_playlist_tracks(sp.user,playlists[i]['id']))

    for song in moinsPlaylist:
        if song['track']['name'] not in newMoinsPlaylist:
            newMoinsPlaylist.append(song['track']['name'])
            
    nameSong = []
    for song in findings:
        if song['track']['name'] not in alreadyInPhantasma and song['track']['name'] not in newMoinsPlaylist and song['track']['type'] != 'episode': 
            new_songs.append(song['track']['id'])
            nameSong.append(song['track']['name'])

    for song in plusPlaylist:
        if song['track']['name'] not in alreadyInPhantasma and song['track']['name'] not in new_songs and song['track']['name'] not in newMoinsPlaylist and song['track']['type'] != 'episode':
            new_songs.append(song['track']['id'])
            nameSong.append(song['track']['name'])
        elif song['track']['name'] in alreadyInPhantasma:
            sp.playlist_remove_all_occurrences_of_items(playlists[indexPlusPlaylists]['id'], [song['track']['uri']])
            print("Removed from Plus : ", song['track']['name'])


    while(len(new_songs) > 0):
        for item in new_songs:
            try:
                sp.playlist_add_items(phantasma['id'], [item])
                print(f'La chanson {nameSong[new_songs.index(item)]} a été ajoutée à la playlist !')
                sp.playlist_remove_all_occurrences_of_items(playlists[indexPlusPlaylists]['id'], [song['track']['uri']])
                print("Removed from Plus : ", song['track']['name'])
                new_songs.remove(item)
            except:
                print(f'Erreur : La chanson {nameSong[new_songs.index(item)]} n a pas été ajoutée à la playlist')
                new_songs.remove(item)

    newMoinsPlaylist = []
    for song in moinsPlaylist:
        newMoinsPlaylist.append(song['track']['id'])

    while(len(newMoinsPlaylist) > 0):
        sp.playlist_remove_all_occurrences_of_items(phantasma['id'], newMoinsPlaylist[:100])
        newMoinsPlaylist = newMoinsPlaylist[100:]


    phantasmaPlaylist = list(get_playlist_tracks(sp.user,phantasma['id']))
    alreadyInPhantasmaID=[]
    alreadyInPhantasma=[]
    for val in phantasmaPlaylist:
        alreadyInPhantasmaID.append(val['track']['id'])
        alreadyInPhantasma.append(val['track']['name'])

    new_phantasma = []
    for i in range(len(alreadyInPhantasma)):
        new_phantasma.append([alreadyInPhantasma[i],alreadyInPhantasmaID[i]])

    try:
        os.remove("PhanSongs.csv")
        with open('PhanSongs.csv', 'w') as creating_new_csv_file: 
            ...
        with open('PhanSongs.csv', 'w') as f:
            writer = csv.writer(f)
            for val in new_phantasma:      
                writer.writerow(val)
    except:
        with open('PhanSongs.csv', 'w') as creating_new_csv_file: 
            ...
            with open('PhanSongs.csv', 'w') as f:
                writer = csv.writer(f)
                for val in new_phantasma:      
                    writer.writerow(val)


def playlist(name,copy):


    assert type(name) == str, 'Le nom doit être un string'


    playlists = sp.current_user_playlists()['items']
    for i in range(len(playlists)):
        if playlists[i]['name'] == name:
            findAndAdd(playlists[i],get_playlist_tracks(sp.user,copy))
            print("Playlist already exists, added songs to it")
            return

    sp.user_playlist_create(sp.user,name)
    playlists = sp.current_user_playlists()['items']
    
    index = True
    for i in range(len(playlists)):
        if playlists[i]['name'] == name:
            index = i
    if index:
        print("Erreur : La playlist ne s'est pas créée")
        return

    c = get_playlist_tracks(sp.user,copy)
    id = []
    for song in c:
        id.append(song['track']['uri'])

    
    while(len(id) > 0):
        sp.playlist_add_items(playlists[index]['id'], id[:100])
        id = id[100:]

copy = '6STUpuSD8zGBWK4maMHVWO' #Findings la playlist d'hugo
# copy = '1L9usNAScb7P2yb1gQeMR8' #SayLess ma playlist

# playlist('Test',copy) #Pour créer une playlist

playlists = sp.current_user_playlists()['items']
for i in range(len(playlists)):
    if playlists[i]['name'] == 'Phantasma':
        index = i

findAndAdd(playlists[index],get_playlist_tracks(sp.user,copy))


