#!/usr/bin/python3

import openai
import telegram
import logging
import json
import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Set up logger
logging.basicConfig(
    filename="/var/www/telegram_chatbot/bot.log",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)

# Load API keys and tokens from configuration file
try:
    with open("/var/www/telegram_chatbot/config.json", "r") as f:
        config = json.load(f)
except FileNotFoundError:
    logger.error("config.json file not found")
    exit(1)
except json.JSONDecodeError as json_err:
    logger.error(f"Error load API keys and tokens from config.json file: {json_err}")
    exit(1)

# Set API keys and tokens
openai_api_key = config["openai_api_key"]
telegram_bot_token = config["telegram_bot_token"]
openweathermap_api_key = config["openweathermap_api_key"]
newsapi_api_key = config["newsapi_api_key"]

# Set up OpenAI API client
openai.api_key = openai_api_key

# Set up Telegram bot
updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher
bot = telegram.Bot(token=telegram_bot_token)


def start(update, context):
    """Start command handler. Sends a message to the user explaining what the bot does."""
    # List available commands
    commands = [
        "/hlp - show available commands",
        "/abt - learn more about me",
        "/msg - send me a message",
        "/img - generate an image",
        "/wea - give me the weather forecast",
        "/news - give me the latest news",
        "/lol - tell me a joke",
    ]
    command_list = "\n".join(commands)

    # Send message to user explaining what the bot does
    first_name = update.message.from_user.first_name
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hi, {first_name}! I am a chatbot powered by the ChatGPT model developed by OpenAI. My purpose is to assist users in having natural conversations and answering their questions to the best of my ability. I am constantly learning and improving, so feel free to ask me anything!\n\nAvailable commands:\n{command_list}",
    )


def hlp(update, context):
    """Help command handler. Sends a message to the user listing available commands."""
    commands = [
        "/hlp - show available commands",
        "/abt - learn more about me",
        "/msg - send me a message",
        "/img - generate an image",
        "/wea - give me the weather forecast",
        "/news - give me the latest news",
        "/lol - tell me a joke",
    ]
    context.bot.send_message(chat_id=update.effective_chat.id, text="\n".join(commands))


def abt(update, context):
    """About command handler. Sends a message to the user explaining more about the bot."""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"ChatGPT is a chatbot that uses the power of artificial intelligence to help you communicate with customers and prospects. It can be used to answer questions, provide support, and even sell products and services. The best part about ChatGPT is that it is constantly learning and evolving, which means that it gets better over time.\n\nOne of the most important aspects of any chatbot is its usability. ChatGPT is designed to be easy to use, even for those who are not familiar with chatbots. The interface is simple and straightforward, and the bot is able to understand natural language. This makes it easy to get started with ChatGPT and get the most out of it.\n\nIn addition to being easy to use, ChatGPT is also highly customizable. This means that you can tailor the chatbot to your specific needs and requirements. For example, you can choose the types of questions that it can answer, as well as the tone and style of the conversation. This allows you to create a chatbot that is truly unique to your brand.\n\nChatGPT is constantly being updated with new features and improvements. For example, the recent addition of the 'smart selling' feature allows the chatbot to upsell and cross-sell products and services to customers. This is a valuable addition that can help you boost sales and revenue.\n\nLooking to the future, ChatGPT is poised to become even more powerful and useful. The team behind the chatbot is constantly working on new features and improvements. Some of the things that are in the pipeline include the ability to handle more complex conversations, integration with third-party platforms, and support for more languages.\n\nAs you can see, ChatGPT has a lot to offer in terms of usability. It is easy to use, highly customizable and constantly evolving. This makes it an ideal chatbot for businesses of all sizes. If you are looking for a chatbot that can help you boost sales and improve customer service, ChatGPT is definitely worth considering.",
    )


def msg(update, context):
    """Chat command handler. Uses the ChatGPT model to generate a response to the user's message."""
    # Get user's message
    msg = update.message.text

    # Use the OpenAI API to generate a response
    prompt = f"User: {msg}\n" f"Chatbot: "
    endpoint = "https://api.openai.com/v1/completions"
    api_key = openai_api_key
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    msg_data = {
        "model": "text-davinci-002",
        "prompt": prompt,
        "max_tokens": 2048,
        "temperature": 0.5,
        "frequency_penalty": 1,
        "presence_penalty": 1,
    }
    logger.info(f"Sending OpenAI API request with data: {msg_data}")
    try:
        response = requests.post(endpoint, headers=headers, json=msg_data)
        response.raise_for_status()
        response_text = response.json()["choices"][0]["text"]
        context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)
    except requests.exceptions.RequestException as msg_err:
        logger.error(f"OpenAI API request failed: {msg_err}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="An error occurred while generating a response, please try again later",
        )


def img(update, context):
    """Image message handler. Uses the Dall-E model to generate an image in response to the user's message."""
    # Get user's message
    img = update.message.text

    # Use the OpenAI API to generate an image
    endpoint = "https://api.openai.com/v1/images/generations"
    api_key = openai_api_key
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    img_data = {
        "model": "image-alpha-001",
        "prompt": img,
        "num_images": 1,
        "size": "512x512",
        "response_format": "url",
    }
    logger.info(f"Sending OpenAI API request with data: {img_data}")
    try:
        response = requests.post(endpoint, headers=headers, json=img_data)
        response.raise_for_status()
        img_url = response.json()["data"][0]["url"]
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=img_url)
    except requests.exceptions.RequestException as img_err:
        logger.error(f"OpenAI API request failed: {img_err}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="An error occurred while generating an image, please try again later",
        )


def get_ip():
    """Get the user's IP address."""
    # Use the ipify API to retrieve the user's IP address
    response = requests.get("https://api64.ipify.org?format=json").json()
    return response["ip"]


def get_location():
    """Get the user's location data."""
    # Use the ipapi API to retrieve the user's location data
    ip_address = get_ip()
    response = requests.get(f"https://ipapi.co/{ip_address}/json/").json()
    location_data = {
        "ip": ip_address,
        "lat": response.get("latitude"),
        "lon": response.get("longitude"),
        "country": response.get("country_code"),
    }
    return location_data


def wea(update, context):
    """Weather command handler. Sends the weather forecast to the user."""
    # Use the OpenWeatherMap API to retrieve the weather forecast
    lat_data = get_location()["lat"]
    lon_data = get_location()["lon"]
    wea_url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}".format(
        lat_data, lon_data, openweathermap_api_key
    )
    try:
        response = requests.get(wea_url)
        if response.status_code == 200:  # Success
            # Parse the response and extract the weather data
            wea_data = response.json()
            forecast_list = wea_data["list"]
            forecast = []
            for i in range(5):
                day = forecast_list[i]
                time_stamp = day["dt_txt"]
                temperature = day["main"]["temp"]
                temperature_min = day["main"]["temp_min"]
                temperature_max = day["main"]["temp_max"]
                humidity = day["main"]["humidity"]
                wind_speed = day["wind"]["speed"]
                description = day["weather"][0]["description"]
                forecast.append(
                    {
                        "time_stamp": time_stamp,
                        "temperature": temperature,
                        "temperature_min": temperature_min,
                        "temperature_max": temperature_max,
                        "humidity": humidity,
                        "wind_speed": wind_speed,
                        "description": description,
                    }
                )
            # Format the weather forecast as a string
            forecast_report = ""
            for day in forecast:
                forecast_report += "Time: {}\n".format(day["time_stamp"])
                forecast_report += (
                    "Temperature: {:.1f}°C (min: {:.1f}°C, max: {:.1f}°C)\n".format(
                        day["temperature"] - 273.15,
                        day["temperature_min"] - 273.15,
                        day["temperature_max"] - 273.15,
                    )
                )
                forecast_report += "Humidity: {}%\n".format(day["humidity"])
                forecast_report += "Wind Speed: {} m/s\n".format(day["wind_speed"])
                forecast_report += "Conditions: {}\n".format(day["description"])
                forecast_report += "\n"
            # Send the weather forecast to the user
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=forecast_report
            )
        else:  # Error
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="An error occurred while retrieving a weather forecast",
            )
    except Exception as wea_err:
        logger.error(f"OpenWeatherMap API request failed: {wea_err}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="An error occurred while retrieving a weather forecast, please try again later",
        )


def news(update, context):
    """News command handler. Sends the latest news to the user."""
    # Set up the request parameters
    country_id = get_location()["country"]
    params = {
        "apiKey": newsapi_api_key,
        "country": country_id,
        "pageSize": 5,
        "sortBy": "publishedAt",
    }

    # Send the request to the News API
    news_url = "https://newsapi.org/v2/top-headlines"
    try:
        response = requests.get(news_url, params=params)
        if response.status_code == 200:  # Success
            # Parse the response and extract the news articles
            news_data = response.json()
            articles = news_data["articles"]

            # Build the message to send to the user
            message = ""
            for article in articles:
                title = article["title"]
                url = article["url"]
                message += f"\n- {title}: {url}"

            # Send the message to the user
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        else:  # Error
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="An error occurred while retrieving news",
            )
    except Exception as news_err:
        logger.error(f"News API request failed: {news_err}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="An error occurred while retrieving news, please try again later",
        )


def lol(update, context):
    """Joke command handler. Sends a joke to the user."""
    # Use the Chuck Norris API to retrieve a joke
    lol_url = "https://api.chucknorris.io/jokes/random"
    try:
        response = requests.get(lol_url)
        if response.status_code == 200:  # Success
            # Parse the response and extract the joke
            lol_data = response.json()
            lol = lol_data["value"]
            # Send the joke to the user
            context.bot.send_message(chat_id=update.effective_chat.id, text=lol)
        else:  # Error
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="An error occurred while retrieving a joke",
            )
    except Exception as lol_err:
        logger.error(f"Chuck Norris API request failed: {lol_err}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="An error occurred while retrieving a joke, please try again later",
        )


# Set up command handlers
dispatcher.add_handler(CommandHandler("start", start))

start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

hlp_handler = CommandHandler("hlp", hlp)
dispatcher.add_handler(hlp_handler)

abt_handler = CommandHandler("abt", abt)
dispatcher.add_handler(abt_handler)

msg_handler = CommandHandler("msg", msg)
dispatcher.add_handler(msg_handler)

img_handler = CommandHandler("img", img)
dispatcher.add_handler(img_handler)

wea_handler = CommandHandler("wea", wea)
dispatcher.add_handler(wea_handler)

news_handler = CommandHandler("news", news)
dispatcher.add_handler(news_handler)

lol_handler = CommandHandler("lol", lol)
dispatcher.add_handler(lol_handler)

# Set up message handler
msg_handler = MessageHandler(Filters.text, msg)
dispatcher.add_handler(msg_handler)

# Start the bot
updater.start_polling()

# Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM, or SIGABRT
updater.idle()
