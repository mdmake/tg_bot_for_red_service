import telebot
import requests
import yaml


def get_config(path):
    with open(path) as f:
        config = yaml.safe_load(f)
    return config


config = get_config("config.yaml")


TOKEN = config['telegram']['token']
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        init_red_server_info(message.from_user.id)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Привет. Это вспомогательный бот для сервиса "
                                               "определения красного")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /start.")


def init_red_server_info(user_id):
    url = config['web']['url']
    query_string = {'user_id': user_id, "token": TOKEN}
    try:
        requests.request('GET', url, params=query_string)
        bot.send_message(user_id, "Привет, я сервис по определению красного, "
                                  "теперь я будет тебе писать каждый раз, как мне пришлют картинку")
    except Exception as e:
        bot.send_message(user_id, "Кажется с сервисом что-то случилось... ")


bot.polling(none_stop=True, interval=0)

