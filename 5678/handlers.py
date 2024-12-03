import random
from utils import get_weather

# Декоратор для логування ID користувача в термінал
def log_user_id(func):
    def wrapper(bot, message, *args, **kwargs):
        user_id = message.from_user.id  # Отримуємо ID користувача
        print(f"User ID: {user_id}, Message: {message.text}")  # Виводимо ID і текст повідомлення в термінал
        return func(bot, message, *args, **kwargs)
    return wrapper

# Команда /start
@log_user_id
def start_command(bot, message):
    try:
        menu = (
            "Привіт! Я ваш особистий бот для погоди. Ось список доступних команд:\n"
            "/weather <місто> - отримати прогноз погоди\n"
            "/info - дізнатися більше про бота\n"
            "/support - зв'язатися з командою підтримки\n"
            "/rate - залишити оцінку боту (від 1 до 10)\n"
            "/joke - почитати жарт про погоду\n"
            "/random - отримати випадкове число"
        )
        bot.send_message(message.chat.id, menu)
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка при виконанні команди /start: {str(e)}")

# Команда /help
@log_user_id
def help_command(bot, message):
    try:
        bot.send_message(message.chat.id, "Для отримання підтримки, будь ласка, звертайтеся до команди підтримки.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка при виконанні команди /help: {str(e)}")

# Команда /info
@log_user_id
def info_command(bot, message):
    try:
        info_text = "Цей бот надає прогнози погоди та жарти про погоду. Насолоджуйтесь!"
        bot.send_message(message.chat.id, info_text)
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка при виконанні команди /info: {str(e)}")

# Команда /support
@log_user_id
def support_command(bot, message):
    try:
        bot.send_message(message.chat.id, "Напишіть ваше повідомлення для підтримки.")
        bot.register_next_step_handler(message, process_support, bot)  # передаємо bot як параметр
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка при виконанні команди /support: {str(e)}")

def process_support(message, bot):  # додаємо параметр bot
    try:
        username = message.from_user.username if message.from_user.username else "без імені"
        admin_chat_id = "1145237457"  # Заміни на свій ID
        bot.send_message(admin_chat_id, f"Новий запит підтримки від @{username}:\n{message.text}")
        bot.send_message(message.chat.id, "Ваше повідомлення для підтримки надіслано!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка при обробці запиту підтримки: {str(e)}")

# Команда /rate
@log_user_id
def rate_command(bot, message):
    try:
        bot.send_message(message.chat.id, "Будь ласка, залиште вашу оцінку боту (від 1 до 10).")
        bot.register_next_step_handler(message, process_rating, bot)  # передаємо bot як параметр
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка при виконанні команди /rate: {str(e)}")

def process_rating(message, bot):  # додаємо параметр bot
    try:
        rating = int(message.text)
        if 1 <= rating <= 10:
            username = message.from_user.username if message.from_user.username else "без імені"
            admin_chat_id = "1145237457"  # Заміни на свій ID
            bot.send_message(admin_chat_id, f"Оцінка від @{username}: {rating}/10")
            bot.send_message(message.chat.id, "Дякуємо за вашу оцінку!")
        else:
            bot.send_message(message.chat.id, "Оцінка має бути від 1 до 10. Спробуйте ще раз.")
            bot.register_next_step_handler(message, process_rating, bot)  # передаємо bot як параметр
    except ValueError:
        bot.send_message(message.chat.id, "Будь ласка, введіть число від 1 до 10.")
        bot.register_next_step_handler(message, process_rating, bot)  # передаємо bot як параметр
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка при виконанні команди /rate: {str(e)}")

# Команда /weather
@log_user_id
def weather_command(bot, message):
    try:
        city = message.text.split()[1]  # Отримуємо назву міста
        weather_info = get_weather(city)
        bot.send_message(message.chat.id, weather_info)
    except IndexError:
        bot.send_message(message.chat.id, "Будь ласка, введіть місто: /weather <місто>")
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка при отриманні погоди: {str(e)}")

# Команда /joke
@log_user_id
def joke_command(bot, message):
    try:
        joke = random.choice([
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
        ])
        bot.send_message(message.chat.id, joke)
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка при виконанні команди /joke: {str(e)}")

# Команда /random
@log_user_id
def random_command(bot, message):
    try:
        number = random.randint(1, 100)
        bot.send_message(message.chat.id, f"Ваше випадкове число: {number}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка при виконанні команди /random: {str(e)}")
