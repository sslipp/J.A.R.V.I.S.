import speech_recognition as sr
import pyttsx3
import json
from commands import execute_command
import re

assistant_active = False
edit_commands = ["edit", "эдит", "просыпайся папочка вернулся", "просыпайся папочка на месте", "эдик"]

# Инициализация синтеза речи
engine = pyttsx3.init()

# Настройка русского голоса
voices = engine.getProperty('voices')
# Найдите и установите русский голос
for voice in voices:
    if 'ru' in voice.languages or 'Russian' in voice.name:
        engine.setProperty('voice', voice.id)
        break

with open('config.json', 'r') as f:
    config = json.load(f)

def speak(text):
    try:
        if not config["silent_mode"]:
            engine.say(text)
            engine.runAndWait()
    except Exception as e:
        print(f"Ошибка при озвучке: {e}")

def evaluate_expression(expression):
    """Выполняет вычисление математического выражения и озвучивает результат."""
    expression = expression.replace("х", "*")
    
    try:
        result = eval(expression)
        speak(f"{result}")
        print(f"Результат: {result}")
    except Exception as e:
        speak("Ошибка в вычислении")
        print(f"Ошибка: {e}")

def listen_command():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 150  # Настройка порога шума
    recognizer.pause_threshold = 0.5   # Увеличение времени ожидания пауз в речи

    with sr.Microphone() as source:
        print("Скажите команду...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            command = recognizer.recognize_google(audio, language="ru-RU").lower()
            print(f"Вы сказали: {command}")
            return command
        except sr.UnknownValueError:
            print("Не удалось распознать команду")
            return None
        except sr.RequestError:
            print("Ошибка сервиса распознавания речи")
            return None
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None

if __name__ == "__main__":
    while True:
        command = listen_command()
        if command:
            # Проверка на математическое выражение (цифры и знаки операций)
            if re.match(r'^[\d\s\+\-\*/\.х]+$', command):
                expression = command.replace(' ', '')  # Убираем пробелы из выражения
                evaluate_expression(expression)
            elif any(cmd in command.lower() for cmd in edit_commands):
                if "не мешай" in command:
                    assistant_active = False
                    speak("Не буду вам мешать, Сэр!")
                    print("Помощник выключен.")
                else:
                    assistant_active = True
                    speak("С возвращением!")
                    print("Помощник включен.")
            elif assistant_active:
                execute_command(command)
            else:
                print("Помощник отключен, не буду вам мешать, Сэр.")
