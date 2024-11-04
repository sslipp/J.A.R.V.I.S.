import os
import pyttsx3
import pyautogui
import webbrowser
import json
import random
import time
import requests
import pywhatkit as kit
import screen_brightness_control as sbc
from datetime import datetime
import threading

SPOTIFY_CLIENT_ID = "89823507d268479483b70854eca4a47d"
SPOTIFY_CLIENT_SECRET = "9a15d06f1ed5494cbc3a46bb3fdb7b4e"
SPOTIFY_ACCESS_TOKEN = "BQC8eB9FwnpW2-XMe3RETfR0wzcKC8vd7mtZRfv32hfEyLwuoSg5vUA1yN1w3enA01etpVeQP1sZ3b38rNJpDV-vBCBY7vxpOoIjDneXZTvuTJfQHms"

# Инициализация синтеза речи
engine = pyttsx3.init()

# Настройка русского голоса
voices = engine.getProperty('voices')
# Найдите и установите русский голос
for voice in voices:
    if 'ru' in voice.languages or 'Russian' in voice.name:
        engine.setProperty('voice', voice.id)
        break

# Загрузка настроек из config.json
with open('config.json', 'r') as f:
    config = json.load(f)

def speak(text):
    try:
        if not config["silent_mode"]:
            engine.say(text)
            engine.runAndWait()
    except Exception as e:
        print(f"Ошибка при озвучке: {e}")

school_protocol_active = False  # Переменная для отслеживания состояния протокола
schedule_thread = None  # Переменная для потока

import screen_brightness_control as sbc

def adjust_brightness(level):
    """Adjust screen brightness to a specified level."""
    if level == 'максимум':
        sbc.set_brightness(100)
    elif level == 'минимум':
        sbc.set_brightness(0)
    else:
        try:
            brightness_level = int(level.replace('%', '').strip())
            sbc.set_brightness(brightness_level)
        except ValueError:
            print("Не удалось распознать уровень яркости. Пожалуйста, используйте значения от 0 до 100 или ключевые слова 'максимум'/'минимум'.")

def play_background_music():
    config["background_music"] = True
    save_config()
    speak("Открываю фоновую музыку")
    print("Открываю фоновую музыку")
    webbrowser.open("https://www.youtube.com/watch?v=1fueZCTYkpA")

def stop_background_music():
    config["background_music"] = False
    save_config()
    speak("Фоновая музыка выключена")
    print("Фоновая музыка выключена")
    pyautogui.hotkey('ctrl', 'w')

def load_schedule(file_path="schedule.json"):
    """Загружает расписание из JSON файла."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def execute_scheduled_action(action):
    """Выполняет действия по расписанию: переход по ссылке, клик мышью, комбинация клавиш."""
    # Переход по ссылке
    if action.get("url"):
        webbrowser.open(action["url"])
        print(f"Переход по ссылке: {action['url']}")
    time.sleep(5)

    # # Нажатие комбинации клавиш
    # keyboard_shortcut = action.get("keyboard_shortcut")
    # if keyboard_shortcut:
    #     time.sleep(2)
    #     pyautogui.hotkey(*keyboard_shortcut)
    #     print(f"Нажатие комбинации клавиш: {' + '.join(keyboard_shortcut)}")

  # Выполнение кликов мышью по указанным координатам
    mouse_clicks = action.get("mouse_clicks", [])
    for i, click in enumerate(mouse_clicks):
        x, y = click["x"], click["y"]
        time.sleep(2)  # Небольшая задержка перед каждым кликом
        pyautogui.click(x, y)
        print(f"Клик мышью #{i+1} на координатах: ({x}, {y})")

def check_schedule_loop(schedule):
    """Запускает цикл для проверки расписания и выполнения действий."""
    while school_protocol_active:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_day = now.strftime("%A")

        for action in schedule:
            if action["day"] == current_day and action["time"] == current_time:
                print(f"Выполнение действия по расписанию на {current_day} в {current_time}")
                execute_scheduled_action(action)
                time.sleep(60)  # Ждать одну минуту, чтобы избежать повторного выполнения
        time.sleep(30)  # Проверять расписание каждые 30 секунд

def toggle_school_protocol():
    """Переключает состояние протокола школы."""
    global school_protocol_active, schedule_thread
    school_protocol_active = not school_protocol_active
    
    if school_protocol_active:
        schedule = load_schedule()
        speak("Протокол 'Школа' активирован")
        print("Протокол 'Школа' активирован. Запуск проверки расписания.")
        # Запускаем цикл расписания в отдельном потоке
        schedule_thread = threading.Thread(target=check_schedule_loop, args=(schedule,))
        schedule_thread.start()
    else:
        speak("Протокол 'Школа' деактивирован")
        print("Протокол 'Школа' деактивирован.")
        school_protocol_active = False
        if schedule_thread and schedule_thread.is_alive():
            schedule_thread.join()  # Останавливаем поток корректно

def start_recorder():
    config["start_recorder"] = False
    save_config()
    speak("Запись включена")
    print("Запись включена")
    pyautogui.hotkey('ctrl', 'shift', 'e')

def stop_recorder():
    config["stop_recorder"] = True
    save_config()
    speak("Запись выключена")
    print("Запись выключена")
    pyautogui.hotkey('ctrl', 'shift', 'e')

def stop_and_start_space():
    config["stop_and_start_space"] = True
    save_config()
    print("Пробел был нажат!")
    pyautogui.hotkey('space')

# def list_devices():
#     devices_url = "https://api.spotify.com/v1/me/player/devices"
#     headers = {"Authorization": f"Bearer {SPOTIFY_ACCESS_TOKEN}"}
#     response = requests.get(devices_url, headers=headers)
    
#     if response.status_code == 200:
#         devices = response.json().get("devices", [])
#         if devices:
#             print("Список доступных устройств:")
#             for device in devices:
#                 print(f"Имя: {device['name']}, ID: {device['id']}, Активное: {device['is_active']}")
#         else:
#             print("Устройства не найдены.")
#     else:
#         print("Ошибка при получении устройств:", response.status_code)

# def play_spotify_song(song_name):
#     list_devices()  # Вызов функции для отображения списка устройств
#     devices_url = "https://api.spotify.com/v1/me/player/devices"
#     headers = {"Authorization": f"Bearer {SPOTIFY_ACCESS_TOKEN}"}
#     devices_response = requests.get(devices_url, headers=headers)
#     devices = devices_response.json().get("devices")
    
#     if not devices:
#         print("Нет активного устройства для воспроизведения.")
#         return
    
#     # Получаем ID активного устройства
#     device_id = devices[0]["id"]

#     # Поиск трека
#     search_url = "https://api.spotify.com/v1/search"
#     params = {"q": song_name, "type": "track", "limit": 1}
#     response = requests.get(search_url, headers=headers, params=params)
    
#     if response.status_code == 200:
#         track = response.json()['tracks']['items'][0]
#         track_uri = track['uri']
        
#         # Воспроизведение трека на указанном устройстве
#         play_url = "https://api.spotify.com/v1/me/player/play"
#         play_response = requests.put(
#             play_url, 
#             headers=headers, 
#             json={"uris": [track_uri]}, 
#             params={"device_id": device_id}
#         )
        
#         if play_response.status_code == 204:
#             print(f"Воспроизведение песни: {track['name']} от {track['artists'][0]['name']}")
#         else:
#             print("Ошибка воспроизведения трека.")
#     else:
#         print("Ошибка поиска трека.")

def toggle_one_house():
    config["one_house"] = not config["one_house"]
    save_config()
    if config["one_house"]:
        speak("Я вас поняла шалунишка")
        print("Я вас поняла шалунишка")
        webbrowser.open("https://sex-studentki.live/hq-porn")
    else:
        speak("Выключаю")
        print("Выключаю")

def toggle_jarvis_mode():
    config["jarvis_mode"] = not config["jarvis_mode"]
    save_config()
    speak("Режим Джарвиса включен" if config["jarvis_mode"] else "Режим Джарвиса выключен")

def toggle_acdc_music():
    config["acdc_music"] = not config["acdc_music"]
    save_config()
    if config["acdc_music"]:
        speak("Включение музыки AC/DC")
        # Здесь может быть код для проигрывания музыки
    else:
        speak("Выключение музыки AC/DC")
        # Здесь может быть код для остановки музыки
    print("Музыка AC/DC включена" if config["acdc_music"] else "Музыка AC/DC выключена")

def adjust_volume(level):
    if level == 'maximum':
        pyautogui.press('volumeup', presses=50)
    elif level == 'minimum':
        pyautogui.press('volumedown', presses=50)
    elif level == 'middle':
        pyautogui.press('volumedown', presses=25)
    print(f"Громкость установлена на {level}")

def open_website(name):
    websites = {
        "mail": "https://gmail.com",
        "youtube": "https://youtube.com",
        "netflix": "https://netflix.com"
    }
    url = websites.get(name, f"https://{name}.com")
    webbrowser.open(url)
    speak(f"Открываю {name}")
    print(f"Открываю {name}")

def play_youtube_video(query):
    kit.playonyt(query)
    speak(f"Ищу видео {query} на YouTube")
    print(f"Ищу видео {query} на YouTube")

def save_config():
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
