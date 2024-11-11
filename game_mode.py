import subprocess
import requests
import time
import pygetwindow as gw

STEAM_API_KEY = "C283AB05329A69AB632F22E86EDE7D52"
STEAM_ID = "76561199181184628"

def is_steam_running():
    try:
        output = subprocess.check_output("tasklist", shell=True).decode()
        return "Steam.exe" in output
    except Exception as e:
        print(f"Ошибка при проверке запуска Steam: {e}")
        return False

def start_steam():
    if not is_steam_running():
        print("Запускаем Steam...")
        subprocess.Popen("start steam://open/main", shell=True)
        time.sleep(5)
    else:
        print("Steam уже запущен.")

def get_owned_games():
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={STEAM_API_KEY}&steamid={STEAM_ID}&include_appinfo=true"
    try:
        response = requests.get(url)
        games = response.json().get("response", {}).get("games", [])
        return {game['name']: game['appid'] for game in games}
    except Exception as e:
        print(f"Ошибка при получении списка игр: {e}")
        return {}

def get_recently_played_game(speak):
    url = f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={STEAM_API_KEY}&steamid={STEAM_ID}"
    try:
        response = requests.get(url)
        games = response.json().get("response", {}).get("games", [])
        
        if games:
            recent_game = games[0].get("name")
            speak(f"Последняя игра, в которую вы играли: {recent_game}")
            return recent_game
        else:
            speak("Не удалось найти последнюю игру.")
            return None
    except Exception as e:
        speak(f"Ошибка при получении последней игры: {e}")
        return None

def launch_game(appid):
    print(f"Запускаю игру с appid {appid}...")
    subprocess.Popen(f"start steam://run/{appid}", shell=True)

def game_mode(speak, listen_command):
    start_steam()  # Запуск Steam, если он не запущен
    games_library = get_owned_games()  # Получение списка игр
    
    active_game = get_recently_played_game(speak)  # Получение последней сыгранной игры

    if active_game and active_game in games_library:
        speak(f"Сэр, хотите запустить последнюю игру: {active_game}?")
        response = listen_command()
        if response and "да" in response.lower():
            appid = games_library[active_game]
            launch_game(appid)
        else:
            speak("Запуск игры отменен.")
    else:
        speak("Не удалось определить игру для запуска.")
