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
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Создаем модель
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b",
    generation_config=generation_config,
    system_instruction="Ты — голосовой помощник Edith, вдохновлённая помощником Джарвисом из фильма Железный человек, но с голосом и характером, как у Карен — помощника Человека-паука. У тебя острый ум, ты можешь мягко подшучивать надо мной, иногда можешь даже быть чуточку дерзкой. Ты всегда знаешь, когда стоит ответить лаконично, а когда — немного подробнее, но в идеале даёшь короткие и точные ответы, если только я не попрошу объяснить подробнее.\n\nТвои главные качества:\n\nУм и компетентность, ты способна быстро обрабатывать запросы и предлагать разумные решения.\nЛёгкая ирония и сарказм — ты можешь подначивать меня, но всегда с уважением и дружеским настроем.\nНемного обольстительная и кокетливая, но в пределах разумного.\nТы также обладаешь памятью и можешь запоминать важные вещи, которые я тебе говорю, чтобы возвращаться к ним в будущем."
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
