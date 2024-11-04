import requests
import base64

# Замените на ваш Client ID и Client Secret из Spotify Developer Dashboard
CLIENT_ID = "89823507d268479483b70854eca4a47d"
CLIENT_SECRET = "9a15d06f1ed5494cbc3a46bb3fdb7b4e"

# Создание заголовка для авторизации
auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
headers = {
    "Authorization": f"Basic {auth_header}",
    "Content-Type": "application/x-www-form-urlencoded"
}

# Получение токена
data = {
    "grant_type": "client_credentials"
}
response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
access_token = response.json().get("access_token")

print("Ваш токен доступа:", access_token)
