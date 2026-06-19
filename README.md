# 🏃‍♂️ Running Weather Telegram Bot

An intuitive Telegram bot that helps runners decide if the weather outside is friendly for a run. It fetches real-time weather data, calculates a **Running Score (0-10)** based on temperature, wind speed, and humidity, and recommends the best clothing for the session.

## ✨ Features

* **Instant Running Score:** Dynamically calculates a comfort rating out of 10 for any specified city.
* **Smart Clothing Recommendations:** Suggests appropriate gear (t-shirt, hoodie, layers, or staying indoors) matching the weather conditions.
* **Detailed Weather Breakdown:** Interactive inline buttons allow users to check exact temperature, wind speed, and humidity instantly.
* **Real-time Data:** Powered by the OpenWeatherMap API.

## 🛠 Tech Stack

* **Language:** Python 3.x
* **Libraries:** `pyTelegramBotAPI`, `requests`, `python-dotenv`
* **API:** OpenWeatherMap API

## 🚀 Installation & Setup

Follow these steps to get the bot running locally:

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/running-weather-bot.git](https://github.com/YOUR_USERNAME/running-weather-bot.git)
cd running-weather-bot
2. Install Dependencies
Make sure you have Python installed, then run:

Bash
pip install pyTelegramBotAPI requests python-dotenv
3. Configure Environment Variables
To keep API keys secure, this project uses environment variables.

Create a file named .env in the root directory.

Add your custom API tokens from Telegram (BotFather) and OpenWeatherMap:

Code snippet
TELEGRAM_API_KEY=your_telegram_bot_token_here
WEATHER_API_KEY=your_openweathermap_api_key_here

4. Run the Bot
Start the application using the following command:

Bash
python Running_Weather_Telegram_Bot.py
📈 Scoring Logic
The bot evaluates weather conditions using a strict deduction system:

Temperature: Ideal range is between 10°C and 25°C. Points are deducted for extreme heat or cold.

Wind Speed: Deductions are applied if the wind exceeds 5 m/s.

Humidity: High humidity (>80%) or extremely dry air (<30%) will lower the overall score.
