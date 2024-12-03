from telebot import TeleBot
from handlers import start_command, help_command, info_command, support_command, joke_command, \
    random_command, weather_command, rate_command
from utils import get_env_token  # Додаємо цей рядок

def main():
    bot = TeleBot(get_env_token())  # Замінюємо статичний токен на функцію, що читає його з .env

    # Команда /start
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        start_command(bot, message)

    # Команда /help
    @bot.message_handler(commands=['help'])
    def handle_help(message):
        help_command(bot, message)

    # Команда /info
    @bot.message_handler(commands=['info'])
    def handle_info(message):
        info_command(bot, message)

    # Команда /support
    @bot.message_handler(commands=['support'])
    def handle_support(message):
        support_command(bot, message)

    # Команда /joke
    @bot.message_handler(commands=['joke'])
    def handle_joke(message):
        joke_command(bot, message)

    # Команда /random
    @bot.message_handler(commands=['random'])
    def handle_random(message):
        random_command(bot, message)

    # Команда /weather
    @bot.message_handler(commands=['weather'])
    def handle_weather(message):
        weather_command(bot, message)

    # Команда /rate
    @bot.message_handler(commands=['rate'])
    def handle_rate(message):
        rate_command(bot, message)

    bot.polling()

if __name__ == "__main__":
    main()
