import telebot
from telebot import types
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

bot = telebot.TeleBot(TELEGRAM_API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "👋 Welcome to *Running Weather Bot*! 🏃\n\nSend me your city and I'll tell you how good the weather is for running today!",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(message, ask_city)

def ask_city(message):
    city = message.text
    rating, recommendation = rate_running_weather(city)

    if rating is None:
        bot.send_message(message.chat.id, "⚠️ City not found. Please try again.")
        return

    bot.send_message(
        message.chat.id,
        f"🏃‍♂️ *Running Score* for *{city}*: *{rating}/10*\n\n👕 {recommendation}",
        parse_mode='Markdown'
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🌡 Temperature", callback_data=f"temp_{city}"))
    markup.add(types.InlineKeyboardButton("💨 Wind", callback_data=f"wind_{city}"))
    markup.add(types.InlineKeyboardButton("💧 Humidity", callback_data=f"hum_{city}"))
    bot.send_message(message.chat.id, "Tap a button below to see more details:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if '_' in call.data:
        action, city = call.data.split('_', 1)
        weather = get_weather(city)
        if weather is None:
            bot.send_message(call.message.chat.id, "⚠️ Couldn't fetch data.")
            return

        if action == "temp":
            bot.send_message(call.message.chat.id, f"🌡 Temperature in {city}: {weather['temp']}°C")
        elif action == "wind":
            bot.send_message(call.message.chat.id, f"💨 Wind speed in {city}: {weather['wind']} m/s")
        elif action == "hum":
            bot.send_message(call.message.chat.id, f"💧 Humidity in {city}: {weather['humidity']}%")

def get_weather(city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    return {
        "temp": data["main"]["temp"],
        "wind": data["wind"]["speed"],
        "humidity": data["main"]["humidity"]
    }

def rate_running_weather(city):
    weather = get_weather(city)
    if weather is None:
        return None, None

    score = 10

    temp = weather["temp"]
    wind = weather["wind"]
    humidity = weather["humidity"]

    if temp < 0 or temp > 30:
        score -= 4
    elif temp < 10 or temp > 25:
        score -= 2

    if wind > 8:
        score -= 3
    elif wind > 5:
        score -= 1

    if humidity > 80:
        score -= 2
    elif humidity < 30:
        score -= 1

    if score >= 8:
        recommendation = "Perfect for running! Wear light gear like a t-shirt and shorts."
    elif score >= 5:
        recommendation = "Okay weather. Consider a light jacket or hoodie."
    elif score >= 3:
        recommendation = "Not ideal. Wear layers and be cautious."
    else:
        recommendation = "Better not to run today. Stay indoors and stay safe. 🛑"

    return score, recommendation

bot.polling()