import telebot
import random
import requests

# Замініть на свій токен бота
bot = telebot.TeleBot('token')

admin_chat_id = '**************'

# API для отримання погоди
API_KEY = 'key_API'
BASE_URL = 'http********************'

# Список жартів
jokes = [
    "Чому метеорологи ніколи не сперечаються? Бо у них завжди є аргумент в запасі — це їх прогнози!",
    "Яка улюблена погода у комп'ютера? Хмарно з можливістю 'снігу'!",
    "Чому вітру ніколи не цікаво? Бо він завжди 'думає' про те, куди подути!",
    "Як метеорологи запрошують один одного на вечірку? 'Прийди, буде весело, як на грозі!'",
    "Чому дощові черевики ніколи не хвилюються? Бо вони завжди готові до 'сирої' погоди!",
    "Яка улюблена пісня дощу? 'I Will Rain'!",
    "Чому сніг завжди такий щасливий? Бо він знає, що зійде з неба!",
    "Як називають дуже холодний день? 'День, коли навіть полярники залишаються вдома!'",
    "Чому хмари ніколи не відчувають голоду? Бо у них завжди є 'вода' в запасі!",
    "Чому гроза така популярна? Бо вона завжди приносить 'електричні' емоції!"
]

@bot.message_handler(commands=["start"])
def start_message(message):
    menu = (
        "Привіт! Я ваш особистий бот для погоди. Ось список доступних команд:\n"
        "/weather <місто> - отримати прогноз погоди\n"
        "/info - дізнатися більше про бота\n"
        "/support - зв'язатися з командою підтримки\n"
        "/rate - залишити оцінку боту (від 1 до 10)"
    )
    bot.send_message(message.chat.id, menu)

@bot.message_handler(commands=["weather"])
def weather_message(message):
    try:
        city = message.text.split()[1]  # Отримуємо назву міста
        response = requests.get(f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric")
        data = response.json()

        if response.status_code == 200:
            temp = data['main']['temp']
            weather_description = data['weather'][0]['description']
            comment = get_weather_comment(temp)
            joke = random.choice(jokes)

            reply = (f"Прогноз погоди в {city}:\n"
                     f"Температура: {temp}°C\n"
                     f"Опис: {weather_description}\n\n"
                     f"Коментар: {comment}\n"
                     f"Жарт: {joke}")
            bot.send_message(message.chat.id, reply)
        else:
            print(f"Помилка: {data['message']}")
            bot.send_message(message.chat.id, "Не вдалося знайти місто. Спробуйте ще раз.")

    except IndexError:
        bot.send_message(message.chat.id, "Будь ласка, введіть місто: /weather <місто>")
    #except Exception as e:
        #bot.send_message(message.chat.id, f"Виникла помилка: {e}")

@bot.message_handler(commands=["info"])
def info_message(message):
    info_text = "Цей бот надає прогнози погоди та жарти про погоду. Насолоджуйтесь!"
    bot.send_message(message.chat.id, info_text)

@bot.message_handler(commands=["support"])
def support_message(message):
    bot.send_message(message.chat.id, "Напишіть ваше повідомлення для підтримки.")
    bot.register_next_step_handler(message, process_support)

def process_support(message):
    username = message.from_user.username if message.from_user.username else "без імені"
    bot.send_message(admin_chat_id, f"Новий запит підтримки від @{username}:\n{message.text}")
    bot.send_message(message.chat.id, "Ваше повідомлення для підтримки надіслано!")

@bot.message_handler(commands=["rate"])
def rate_message(message):
    bot.send_message(message.chat.id, "Будь ласка, залиште вашу оцінку боту (від 1 до 10).")
    bot.register_next_step_handler(message, process_rating)

def process_rating(message):
    try:
        rating = int(message.text)
        if 1 <= rating <= 10:
            username = message.from_user.username if message.from_user.username else "без імені"
            bot.send_message(admin_chat_id, f"Оцінка від @{username}: {rating}/10")
            bot.send_message(message.chat.id, "Дякуємо за вашу оцінку!")
        else:
            bot.send_message(message.chat.id, "Оцінка має бути від 1 до 10. Спробуйте ще раз.")
            bot.register_next_step_handler(message, process_rating)
    except ValueError:
        bot.send_message(message.chat.id, "Будь ласка, введіть число від 1 до 10.")
        bot.register_next_step_handler(message, process_rating)

def get_weather_comment(temp):
    if temp < 0:
        return "Схоже, на вулиці холодно! Одягніть тепле."
    elif 0 <= temp < 20:
        return "На вулиці прохолодно, але це чудова погода для прогулянки!"
    elif 20 <= temp < 30:
        return "Сьогодні ідеальний день! Не забудьте сонцезахисний крем!"
    else:
        return "Схоже, на вулиці жарко! Час для пляжу!"

if __name__ == '__main__':
    bot.polling()
