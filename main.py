import azure.cognitiveservices.speech as speechsdk
import speech_recognition as sr
import pyttsx3
import json
import requests
import re
from gemini_api import chat_with_edith
from commands import execute_command
from object_detector import ObjectDetector

API_KEY_WEATHER = "42b5a70adf7db188e78f8c14369b5e2a"
CURRENCY_API_KEY = "77f1b03f7318978ec1698eb5"

assistant_active = False
edit_commands = ["edit", "эдит", "просыпайся папочка вернулся", "просыпайся папочка на месте", "эдик"]

# Azure TTS Конфигурация
speech_key = "A6WSUnMWuJCajVJ66wZWYNI4ZY302r1vpJV1BzUquJVEs1UiaRtFJQQJ99AKACYeBjFXJ3w3AAAYACOGvO8G"
service_region = "eastus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.speech_synthesis_voice_name = "ru-RU-DariyaNeural"

# Настройка аудиовыхода
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

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

# Загрузка конфигурации
with open('config.json', 'r') as f:
    config = json.load(f)

# Инициализация детектора объектов
detector = ObjectDetector()

def convert_currency(amount, from_currency, to_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        rates = data.get("rates", {})
        if to_currency in rates:
            converted_amount = amount * rates[to_currency]
            return f"{converted_amount:.2f}"
        else:
            return "Извините, не удалось найти курс для указанной валюты."
    else:
        return "Ошибка при получении данных о курсе валют."

def get_weather(city, lang="ru"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_WEATHER}&lang={lang}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        return f"Сейчас в {city} {weather_description}, температура {temperature}°C."
    else:
        return "Извините, не удалось получить информацию о погоде."

def get_wikipedia_summary(query, lang="ru"):
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("extract")
    else:
        return "Извините, информация не найдена."

def evaluate_expression(expression):
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
    recognizer.energy_threshold = 100
    recognizer.pause_threshold = 0.7

    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            command = recognizer.recognize_google(audio, language="ru-RU").lower()
            print(f"Вы сказали: {command}")
            return command
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            print("Ошибка сервиса распознавания речи")
            return None
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None

def detect_object_on_screen():
    screenshot = detector.capture_screenshot()
    label, confidence = detector.detect_object(screenshot)
    speak(f"На экране обнаружен объект: {label} с вероятностью {confidence:.2%}")
    print(f"Объект: {label}, Вероятность: {confidence:.2%}")

currency_codes = {
    "рублей": "RUB", "руб": "RUB", "рубли": "RUB",
    "гривен": "UAH", "грн": "UAH", "гривны": "UAH", "гривна": "UAH", "griven": "UAH",
    "доллары": "USD", "долларов": "USD", "доллар": "USD", "доллоров": "USD"
}

# Основной цикл ассистента
while True:
    command = listen_command()
    if command:
        if re.match(r'^[\d\s\+\-\*/\.х]+$', command):
            expression = command.replace(' ', '')
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
            command_executed = execute_command(command)
            if not command_executed:
                if command.startswith("что такое"):
                    query = command.replace("что такое", "").strip()
                    if query:
                        summary = get_wikipedia_summary(query)
                        speak(summary)
                        print(summary)
                elif command.startswith("погода в"):
                    city = command.replace("погода в", "").strip()
                    if city:
                        weather_info = get_weather(city)
                        speak(weather_info)
                        print(weather_info)
                elif "что на экране" in command:
                    detect_object_on_screen()  # Вызов распознавания объекта на экране
                else:
                    currency_match = re.search(r'(\d+[.,]?\d*)\s*(рублей|руб|рубли|гривен|грн|гривны|гривна|доллары|долларов|доллар|доллоров)\s*в\s*(рублей|руб|рубли|гривен|грн|гривны|гривна|доллары|долларов|доллар|доллоров)', command)
                    if currency_match:
                        amount = float(currency_match.group(1).replace(' ', '').replace('.', '').replace(',', '.'))
                        from_currency = currency_match.group(2)
                        to_currency = currency_match.group(3)
                        from_currency_code = currency_codes.get(from_currency, "")
                        to_currency_code = currency_codes.get(to_currency, "")
                        if from_currency_code and to_currency_code:
                            result = convert_currency(amount, from_currency_code, to_currency_code)
                            speak(result)
                            print(result)
                        else:
                            speak("Не удалось распознать валюту для конвертации.")
                    else:
                        gpt_response = chat_with_edith(command)
                        speak(gpt_response)
                        print(gpt_response)
        else:
            print("Помощник отключен, не буду вам мешать, Сэр.")
