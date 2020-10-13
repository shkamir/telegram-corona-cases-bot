# This Python file uses the following encoding: utf-8
#                                                    simple telegram bot that sends some stuff      Powered by nUmberX
#           mian libraries for telegram API

from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler
# get updates
from telegram import Update
#       actions of chat
from telegram.chataction import ChatAction

#       for keyboards in chat :)
from telegram import ReplyKeyboardMarkup

# for filtering messages
from telegram.ext.filters import Filters

# to make  delay to the code
from time import sleep

# for choosing random things in iterables
from random import choice
import requests
from bs4 import BeautifulSoup


def get_whole_cases():
    url = "https://www.worldometers.info/coronavirus/"
    req = requests.get(url)
    bsObj = BeautifulSoup(req.text, "html.parser")
    data = bsObj.find_all("div", class_="maincounter-number")

    all_cases = " مبتلایان : {}".format(data[0].text.strip())
    deaths = "مردگان : {}".format(data[1].text.strip())
    recovered = "خوب شده:  {}".format(data[2].text.strip())
    return all_cases, deaths, recovered

def get_by_country(country):
    url = "https://www.worldometers.info/coronavirus/country/{}".format(country)
    req = requests.get(url)
    bsObj = BeautifulSoup(req.text, "html.parser")
    data = bsObj.find_all("div", class_="maincounter-number")

    all_cases = " مبتلایان : {}".format(data[0].text.strip())
    deaths = "مردگان : {}".format(data[1].text.strip())
    recovered = "خوب شده:  {}".format(data[2].text.strip())
    return all_cases, deaths, recovered


token = "your token goes here"
messages = {
    "start_text": "با سلام {} خوش امدید ",
    "help_cmd": "اگر به مشکلی در استفاده با منو برخورد کردید لطفا با ما تماش بگیرید و مشکل را بیان کنید❤️ ",
    # TODO declare the btns
    "all_countries_btn": "نشان دادن وضعیت جهانی کرونا",
    "per_countru_btn": "نشان دادن وضعیت ایران"

}


def start_cmd(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    firstname = update.message.chat.first_name
    lastname = update.message.chat.last_name
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    update.message.reply_text(
        text=messages["start_text"].format(firstname)
    )
    main_menu(update, context)
    print(f"{firstname} {lastname} with chat id of {chat_id} has started using the bot")


# TODO ساخت بات کرونا
# TODO ساخت فانکشن ها
def help_cmd(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=messages['help_cmd']
    )


def main_menu(update: Update, context: CallbackContext):
    buttons = [
        [
            messages["all_countries_btn"]
        ],
        [
            messages["per_countru_btn"]
        ]
    ]
    update.message.reply_text(
        text="انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(keyboard=buttons,resize_keyboard=True)
    )
def whole_handler(update: Update, context: CallbackContext):
    text = """
    
    """
    allcases,deaths,recoverd = get_whole_cases()
    text+= str(allcases+"\n"+deaths+"\n"+recoverd).replace(",", "")
    update.message.reply_text(text=text)

def country_handler(update: Update, context: CallbackContext):
    text = """
    """
    allcases, deaths, recoverd = get_by_country("iran")
    text += str(allcases + "\n\t" + deaths + "\n\t" + recoverd).replace(",", "")
    update.message.reply_text(text=text)


def main():
    updater = Updater(token=token, use_context=True)

    start = CommandHandler('start', start_cmd)
    help = CommandHandler('help', help_cmd)
    updater.dispatcher.add_handler(start)
    updater.dispatcher.add_handler(help)
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["all_countries_btn"]),whole_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages["per_countru_btn"]),country_handler))
    while True:
        try:
            updater.start_polling()
            updater.idle()
        except Exception:
            sleep(15.30)

if __name__=="__main__":
    main()
