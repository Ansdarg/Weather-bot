from constants import TOKEN
import os
import sys
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import CommandHandler
import webdriver



def get_weather():
    url = 'https://www.google.com/search?q=погода+в+тбилиси'

    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get(url)
    
    def search_by_id(id: str):
        search = driver.find_element_by_id(id)
        parameter = search.text
        return parameter
    
    temperature = search_by_id('wob_tm')
    percipation = search_by_id('wob_pp')
    humidity = search_by_id('wob_hm')
    wind = search_by_id('wob_ws')
    description = search_by_id('wob_dc')
    
    driver.quit()

    return temperature, percipation, humidity, wind, description




def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='''Привет.\nМогу показать тебе погоду в Тбилиси.\nДля этого нажми /weather.'''
    )

def weather(update: Update, context: CallbackContext):
    temperature, percipation, humidity, wind, description = get_weather()
    update.message.reply_text(
        text=f'{description}\nТемпература: {temperature}°C.\nОсадки: {percipation}.\nВлажность: {humidity}.\nСкорость ветра: {wind}.'
    )




def main():
    updater = Updater(
        token=TOKEN, 
        use_context=True,
        )
    

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("weather", weather))
    
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
