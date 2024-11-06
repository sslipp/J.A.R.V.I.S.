import speech_recognition as sr
import pyttsx3
import json
import requests
from commands import execute_command
import re
import openai

API_KEY_WEATHER = "42b5a70adf7db188e78f8c14369b5e2a"
CURRENCY_API_KEY = "77f1b03f7318978ec1698eb5"
OPENAI_API_KEY = "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"  # Вставьте свой API ключ OpenAI

openai.api_key = OPENAI_API_KEY

assistant_active = False
edit_commands = ["edit", "эдит", "просыпайся папочка вернулся", "просыпайся папочка на месте", "эдик"]

# Инициализация синтеза речи
engine = pyttsx3.init()

# Настройка русского голоса
voices = engine.getProperty('voices')
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

def convert_currency(amount, from_currency, to_currency):
    """Конвертирует валюту из одной в другую, используя API."""
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
    """Запрашивает текущую погоду для указанного города."""
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
    """Запрашивает краткую информацию из Википедии по заданному запросу."""
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("extract")
    else:
        return "Извините, информация не найдена."

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

def chat_with_gpt(prompt):
    """Общение с ChatGPT для обработки сложных команд."""
    try:
        response = openai.ChatCompletion.create(
            model="text-davinci-003",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        message = response.choices[0].message['content'].strip()
        return message
    except Exception as e:
        print(f"Ошибка при обращении к ChatGPT: {e}")
        return "Произошла ошибка при обработке запроса."

if __name__ == "__main__":
    currency_codes = {
        "рублей": "RUB", "руб": "RUB", "рубли": "RUB",
        "гривен": "UAH", "грн": "UAH", "гривны": "UAH", "гривна": "UAH", "griven": "UAH",
        "доллары": "USD", "долларов": "USD", "доллар": "USD", "доллоров": "USD"
    }

    while True:
        command = listen_command()
        if command:
            # Проверка на математическое выражение (цифры и знаки операций)
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
                # Проверка на запрос к Википедии
                if command.startswith("что такое"):
                    query = command.replace("что такое", "").strip()
                    if query:
                        summary = get_wikipedia_summary(query)
                        speak(summary)
                        print(summary)
                # Проверка на запрос к погоде
                elif command.startswith("погода в"):
                    city = command.replace("погода в", "").strip()
                    if city:
                        weather_info = get_weather(city)
                        speak(weather_info)
                        print(weather_info)
                # Проверка на запрос конвертации валют
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
                    # Обработка остальных команд с помощью ChatGPT
                    gpt_response = chat_with_gpt(command)
                    speak(gpt_response)
                    print(gpt_response)
            else:
                print("Помощник отключен, не буду вам мешать, Сэр.")
