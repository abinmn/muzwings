import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
def search_playlist(query):
    playlist_search = sp.search(query, type='playlist')
    playlist_ids = list()
    for i in playlist_search.get('playlists').get('items'):
        playlist_ids.append(i['id'])
    return playlist_ids


def get_tracks(query):
    track_ids = set()
    playlists = search_playlist(query)
    for p in playlists:
        tracks = sp.playlist_tracks(p, fields='items(track(id))')
        for t in tracks.get('items'):
            if t.get('track'):
                track_ids.add(t['track']['id'])
    return track_ids


def get_audio_features(query):
    tracks = get_tracks(query)
    track_ids = [x for x in tracks]
    tracks_count = len(track_ids)
    audio_features = list()
    for i in range(0, tracks_count, 100):
        temp_features = sp.audio_features(track_ids[i:i + 100])
        audio_features += temp_features
    return audio_features


def get_music_data(query):
    audio_feat = get_audio_features(query)
    audio_feat = json.dumps(audio_feat)

    with open(f'{query}.json', 'w') as f:
        f.write(audio_feat)
        print(f'{query}.json')