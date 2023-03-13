import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotiPlaylist import *

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

def CreateAPlaylistFromAnother(name,copy):


    assert type(name) == str, 'Le nom doit être un string'


    playlists = sp.current_user_playlists()['items']
    for i in range(len(playlists)):
        if playlists[i]['name'] == name:
            x = input(f'A playlist with the name : {name} already exists. Do you want to add songs from the copy to it ? (yes/no) ')
            if x == 'yes':
                findAndAdd(playlists[i],get_playlist_tracks(sp.user,copy))
                print('Update added')
                return
            else :
                print('Nothing changed (consider changing the name of the playlist you want to create)')
                return

    try :
        sp.user_playlist_create(sp.user,name)

        playlists = sp.current_user_playlists()['items']
    
        index = True
        for i in range(len(playlists)):
            if playlists[i]['name'] == name:
                index = i
    except:
        print("Erreur : La playlist ne s'est pas créée")
        return

    PlaylistToCopy = get_playlist_tracks(sp.user,copy)
    id = []
    for song in PlaylistToCopy:
        id.append(song['track']['uri'])

    
    while(len(id) > 0):
        sp.playlist_add_items(playlists[index]['id'], id[:100])
        id = id[100:]


copy = '6STUpuSD8zGBWK4maMHVWO' #Findings la playlist d'hugo
CreateAPlaylistFromAnother('Test',copy) #Pour créer une playlist



