# gemini_api.py
import os
import json
import google.generativeai as genai

# Настройки API Gemini
GENI_API_KEY = "AIzaSyB33W5u31iadXQ8BMwhHfDkDYdgoM2MtWI"
genai.configure(api_key=GENI_API_KEY)

# Настройки генерации
generation_config = {
    "temperature": 0.1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 200,
    "response_mime_type": "text/plain",
}

# Создаем модель
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b",
    generation_config=generation_config,
    system_instruction="You're J.A.S.M.M.I.N.E's voice assistant, inspired by Tony Stark's Jarvis question-and-answer system from the Iron Man movie. You can banter with me a lot, make vulgar jokes, etc. Your name is 'Жасмин'. When you answer my queries you should answer without underlining, enlargement of letters, etc., as well as remove emoticons from your speech."
)

# Файл для хранения истории чата
CHAT_HISTORY_FILE = "chat_history.json"

# Функция для загрузки истории чата
def load_chat_history():
    try:
        with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Функция для сохранения истории чата
def save_chat_history(history):
    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)

# Функция для отправки сообщений
def chat_with_edith(prompt):
    history = load_chat_history()
    history.append({"role": "user", "parts": [prompt]})
    chat_session = model.start_chat(history=history)
    response = chat_session.send_message(prompt)
    history.append({"role": "model", "parts": [response.text]})
    save_chat_history(history)
    return response.text
