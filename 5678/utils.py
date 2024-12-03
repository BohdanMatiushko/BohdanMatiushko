import os
import logging
import requests
from dotenv import load_dotenv

# Завантаження змінних середовища з .env файлу
def get_env_token():
    load_dotenv()  # Завантажуємо змінні середовища з .env файлу
    token = os.getenv('BOT_TOKEN')  # Отримуємо токен бота
    if not token:
        raise ValueError("Токен не знайдено в .env файлі.")
    return token

def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")  # Отримуємо API ключ OpenWeather
    if not api_key:
        raise ValueError("API ключ OpenWeather не знайдений у .env файлі.")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ua"
    response = requests.get(url)

    if response.status_code != 200:
        return "Не вдалося отримати погоду. Перевірте правильність введеного міста."

    data = response.json()
    main = data["main"]
    weather = data["weather"][0]
    temperature = main["temp"]
    description = weather["description"]
    humidity = main["humidity"]

    return (f"Погода в місті {city}:\n"
            f"Температура: {temperature}°C\n"
            f"Опис: {description}\n"
            f"Вологість: {humidity}%")

# Декоратор для логування ID користувача
def log_user_id(func):
    def wrapper(bot, message, *args, **kwargs):
        user_id = message.from_user.id  # Отримуємо ID користувача
        logging.info(f"User ID: {user_id}, Message: {message.text}")  # Логуємо ID та текст повідомлення
        return func(bot, message, *args, **kwargs)
    return wrapper
