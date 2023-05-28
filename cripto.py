import telebot
from bs4 import BeautifulSoup
import requests

BOT = telebot.TeleBot(token='5426461574:AAGnSm14svAysuYq2WUijl7TDaTJPK40vnA')


@BOT.message_handler(commands=['get_price'])
def start(message):
    BOT.send_message(message.chat.id, "Введите криптовалюту:")
    BOT.register_next_step_handler(message, get_price)


def get_price(message):
    try:
        url = "https://www.rbc.ru/crypto/currency/" + message.text.lower() + "usd"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept-Encoding": "*",
            "Connection": "keep-alive"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = soup.findAll("div", "chart__subtitle js-chart-value")
        price = " ".join(texts[0].text.split()[:2])
        BOT.send_message(message.chat.id, 'Текущий курс к доллару - ' + price + "$")
    except Exception:
        BOT.send_message(message.chat.id, "Упс..Что-то пошло не так, попробуйте снова!")


BOT.polling(none_stop=True, timeout=0)

