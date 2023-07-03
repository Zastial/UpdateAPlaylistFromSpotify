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
    
    try:
        with open('MoinSongs.csv', 'r') as f:
            writer = csv.reader(f)

            moins = []
            for row in writer:
                moins.append(row) if row != [] else None
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
        if playlists[i]['name'] == "Moins":
            moinsPlaylist = list(get_playlist_tracks(sp.user,playlists[i]['id']))

    newMoinsPlaylistID = []
    for song in moinsPlaylist:
        if song['track']['name'] not in newMoinsPlaylist:
            newMoinsPlaylist.append(song['track']['name'])
            newMoinsPlaylistID.append(song['track']['id'])
    
    nameSong = []
    for song in findings:
        if song['track']['name'] not in alreadyInPhantasma and song['track']['name'] not in newMoinsPlaylist and song['track']['type'] != 'episode': 
            new_songs.append(song['track']['id'])
            nameSong.append(song['track']['name'])

    while(len(new_songs) > 0):
        for item in new_songs:
            try:
                sp.playlist_add_items(phantasma['id'], [item])
                print(f'La chanson {nameSong[new_songs.index(item)]} a été ajoutée à la playlist !')
                new_songs.remove(item)
            except:
                print(f'Erreur : La chanson {nameSong[new_songs.index(item)]} n a pas été ajoutée à la playlist')
                new_songs.remove(item)



    copynewMoinsPlaylistID = newMoinsPlaylistID
    while(len(newMoinsPlaylistID) > 0):
        sp.playlist_remove_all_occurrences_of_items(phantasma['id'], newMoinsPlaylistID[:100])
        newMoinsPlaylistID = newMoinsPlaylistID[100:]
    
    moinsID = []
    for val in moins:
        moinsID.append(val[1])
    for id in copynewMoinsPlaylistID:
        if id not in moinsID:
            name = sp.track(id)['name']
            print(f'La chanson {name} a été supprimée de la playlist !')


    phantasmaPlaylist = list(get_playlist_tracks(sp.user,phantasma['id']))
    alreadyInPhantasmaID=[]
    alreadyInPhantasma=[]
    for val in phantasmaPlaylist:
        try :
            alreadyInPhantasmaID.append(val['track']['id'])
            alreadyInPhantasma.append(val['track']['name'])    
        except:
            ...


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


    moins = []
    print("newMoinsPlaylist : ", len(newMoinsPlaylist))
    print("copynewMoinsPlaylistID : ", len(copynewMoinsPlaylistID))
    for i in range(len(newMoinsPlaylist)):
        try :
            moins.append([newMoinsPlaylist[i], copynewMoinsPlaylistID[i]])
        except:
            ...
    try:
        os.remove("MoinSongs.csv")
        with open('MoinSongs.csv', 'w', encoding='utf-8') as creating_new_csv_file: 
            ...
        with open('MoinSongs.csv', 'w') as f:
            writer = csv.writer(f)
            for val in moins:      
                writer.writerow(val)
    except:
        with open('MoinSongs.csv', 'w', encoding='utf-8') as creating_new_csv_file: 
            ...
        with open('MoinSongs.csv', 'w') as f:
            writer = csv.writer(f)
            for val in moins:
                try :
                    writer.writerow(val)
                except:
                    writer.writerow(['weirdCharacter', val[1]])

copy = '6STUpuSD8zGBWK4maMHVWO' #Findings la playlist d'hugo
# copy = "7B2yC8hRrdKrWbfyd37r7j" #playlist de Test

playlists = sp.current_user_playlists()['items']
for i in range(len(playlists)):
    if playlists[i]['name'] == 'Phantasma':
        index = i


findAndAdd(playlists[index],get_playlist_tracks(sp.user,copy))


