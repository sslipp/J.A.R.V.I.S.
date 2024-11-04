# spotify_helper.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

# Загрузка конфигурации
with open("config.json", "r") as f:
    config = json.load(f)

# Авторизация в Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=config["SPOTIFY_CLIENT_ID"],
    client_secret=config["SPOTIFY_CLIENT_SECRET"],
    redirect_uri=config["SPOTIFY_REDIRECT_URI"],
    scope="user-read-playback-state user-modify-playback-state"
))

def play_song(song_name):
    # Поиск песни по названию
    results = sp.search(q=song_name, type="track", limit=1)
    if results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        track_uri = track["uri"]
        
        # Включение песни
        sp.start_playback(uris=[track_uri])
        print(f"Воспроизведение {track['name']} - {track['artists'][0]['name']}")
    else:
        print("Песня не найдена.")

def stop_playback():
    # Остановка воспроизведения
    sp.pause_playback()
    print("Воспроизведение остановлено.")
