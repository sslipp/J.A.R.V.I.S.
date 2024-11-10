import os
import pyttsx3
import azure.cognitiveservices.speech as speechsdk
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

# Azure TTS Конфигурация
speech_key = "A6WSUnMWuJCajVJ66wZWYNI4ZY302r1vpJV1BzUquJVEs1UiaRtFJQQJ99AKACYeBjFXJ3w3AAAYACOGvO8G"
service_region = "eastus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.speech_synthesis_voice_name = "ru-RU-DariyaNeural"

# Настройка аудиовыхода
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# Загрузка настроек из config.json
with open('config.json', 'r') as f:
    config = json.load(f)

def speak(text):
    if not config["silent_mode"]:
        ssml_string = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='ru-RU'>
            <voice name='ru-RU-DariyaNeural'>
                <prosody pitch='+2Hz' rate='+2%'>{text}</prosody>
            </voice>
        </speak>
        """
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        result = synthesizer.speak_ssml_async(ssml_string).get()

        if result.reason == speechsdk.ResultReason.Canceled:
            print("Ошибка синтеза речи:", result.cancellation_details.error_details)

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
    speak("Открываю фоновую музыку, Сэр")
    print("Открываю фоновую музыку")
    webbrowser.open("https://www.youtube.com/watch?v=1fueZCTYkpA")

def stop_background_music():
    config["background_music"] = False
    save_config()
    speak("Фоновая музыка выключена")
    print("Фоновая музыка выключена")
    pyautogui.hotkey('ctrl', 'w')

def minimize_window():
    speak("Сворачиваю окно")
    print("Сворачиваю окно")
    pyautogui.hotkey("win", "down")

def shutdown_computer():
    speak("Выключаю компьютер. До свидания!")
    print("Выключаю компьютер...")
    os.system("shutdown /s /t 3")

def start_weekend_mode():
    speak("Запрос выполнен, Сэр")
    print("Запрос выполнен")

    # os.system(r'start "" "C:\Users\Rodion\AppData\Roaming\Telegram Desktop\Telegram.exe"') 

def switch_keyboard_layout():
    speak("Готово, Сэр")
    print("Смена раскладки выполнена")
    pyautogui.hotkey("alt", "shift")

def start_work_mode():
    speak("Запрос выполнен, Сэр")
    print("Запрос выполнен")

    os.system("start tradingview") 
    os.system(r'start "" "C:\Users\Rodion\AppData\Roaming\Telegram Desktop\Telegram.exe"') 
    os.system("start opera") 

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

def toggle_one_house():
    config["one_house"] = not config["one_house"]
    save_config()
    if config["one_house"]:
        speak("Я вас поняла шалунишка")
        print("Я вас поняла шалунишка")
        webbrowser.open("...")
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
    if name in websites:
        url = websites[name]
        print(f"Открываю {name}")
    else:
        url = f"https://www.google.com/search?q={name.replace(' ', '+')}"
        print(f"Ищу в Google: {name}")

    webbrowser.open(url)

def play_youtube_video(query):
    kit.playonyt(query)
    speak(f"Ищу видео {query} на YouTube")
    print(f"Ищу видео {query} на YouTube")

def save_config():
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
