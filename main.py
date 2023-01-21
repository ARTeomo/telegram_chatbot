#!/usr/bin/python3

import openai
import telegram
import logging
import json
import time
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
except json.JSONDecodeError:
    logger.error("Error load API keys and tokens from config.json file: %s", err)
    exit(1)

openai_api_key = config["openai_api_key"]
telegram_bot_token = config["telegram_bot_token"]
openweathermap_api_key = config["openweathermap_api_key"]
newsapi_api_key = config["newsapi_api_key"]
country_id = config["country_id"]
city_id = config["city_id"]

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
        "/start - start the chatbot",
        "/help - show available commands",
        "/about - learn more about me",
        "/message - send me a message",
        "/image - generate an image",
        "/weather - give me the weather forecast",
        "/news - give me the latest news",
        "/joke - tell me a joke",
    ]
    command_list = "\n".join(commands)

    # Send message to user explaining what the bot does
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hi, I am a chatbot powered by the ChatGPT model developed by OpenAI. My purpose is to assist users in having natural conversations and answering their questions to the best of my ability. I am constantly learning and improving, so feel free to ask me anything!\n\nAvailable commands:\n{command_list}",
    )


def help(update, context):
    """Help command handler. Sends a message to the user listing available commands."""
    commands = [
        "/start - start the chatbot",
        "/help - show available commands",
        "/about - learn more about me",
        "/message - send me a message",
        "/image - generate an image",
        "/weather - give me the weather forecast",
        "/news - give me the latest news",
        "/joke - tell me a joke",
    ]
    context.bot.send_message(chat_id=update.effective_chat.id, text="\n".join(commands))


def about(update, context):
    """About command handler. Sends a message to the user explaining more about the bot."""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='ChatGPT is a chatbot that uses the power of artificial intelligence to help you communicate with customers and prospects. It can be used to answer questions, provide support, and even sell products and services. The best part about ChatGPT is that it is constantly learning and evolving, which means that it gets better over time.\n\nOne of the most important aspects of any chatbot is its usability. ChatGPT is designed to be easy to use, even for those who are not familiar with chatbots. The interface is simple and straightforward, and the bot is able to understand natural language. This makes it easy to get started with ChatGPT and get the most out of it.\n\nIn addition to being easy to use, ChatGPT is also highly customizable. This means that you can tailor the chatbot to your specific needs and requirements. For example, you can choose the types of questions that it can answer, as well as the tone and style of the conversation. This allows you to create a chatbot that is truly unique to your brand.\n\nChatGPT is constantly being updated with new features and improvements. For example, the recent addition of the "smart selling" feature allows the chatbot to upsell and cross-sell products and services to customers. This is a valuable addition that can help you boost sales and revenue.\n\nLooking to the future, ChatGPT is poised to become even more powerful and useful. The team behind the chatbot is constantly working on new features and improvements. Some of the things that are in the pipeline include the ability to handle more complex conversations, integration with third-party platforms, and support for more languages.\n\nAs you can see, ChatGPT has a lot to offer in terms of usability. It is easy to use, highly customizable and constantly evolving. This makes it an ideal chatbot for businesses of all sizes. If you are looking for a chatbot that can help you boost sales and improve customer service, ChatGPT is definitely worth considering.',
    )


def message(update, context):
    """Chat command handler. Uses the ChatGPT model to generate a response to the user's message."""
    # Get user's message
    message = update.message.text

    # Use the OpenAI API to generate a response
    prompt = f"User: {message}\n" f"Chatbot: "
    endpoint = "https://api.openai.com/v1/completions"
    api_key = openai_api_key
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    data = {
        "model": "text-davinci-002",
        "prompt": prompt,
        "max_tokens": 2048,
        "temperature": 0.5,
        "frequency_penalty": 1,
        "presence_penalty": 1,
    }
    logger.info("Sending OpenAI API request with data: %s", data)
    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        response_text = response.json()["choices"][0]["text"]
        context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)
    except requests.exceptions.RequestException as err:
        logger.error("OpenAI API request failed: %s", err)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="An error occurred while generating a response",
        )


def image(update, context):
    """Image message handler. Uses the Dall-E model to generate an image in response to the user's message."""
    # Get user's message
    message = update.message.text

    # Use the OpenAI API to generate an image
    endpoint = "https://api.openai.com/v1/images/generations"
    api_key = openai_api_key
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    data = {
        "model": "image-alpha-001",
        "prompt": message,
        "num_images": 1,
        "size": "512x512",
        "response_format": "url",
    }
    logger.info("Sending OpenAI API request with data: %s", data)
    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        image_url = response.json()["data"][0]["url"]
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url)
    except requests.exceptions.RequestException as err:
        logger.error("OpenAI API request failed: %s", err)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="An error occurred while generating an image",
        )


def weather(update, context):
    """Weather command handler. Sends the weather forecast to the user."""
    # Use the OpenWeatherMap API to retrieve the weather forecast
    weather_url = (
        "https://api.openweathermap.org/data/2.5/forecast?id={}&appid={}".format(
            city_id, openweathermap_api_key
        )
    )
    response = requests.get(weather_url)
    if response.status_code == 200:  # Success
        # Parse the response and extract the weather data
        data = response.json()
        forecast_list = data["list"]
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
        context.bot.send_message(chat_id=update.effective_chat.id, text=forecast_report)
    else:  # Error
        logger.error("OpenWeatherMap API request failed: %s", err)
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="An error occurred while retrieving a weather forecast"
        )


def news(update, context):
    """News command handler. Sends the latest news to the user."""
    # Set up the request parameters
    params = {
        "apiKey": newsapi_api_key,
        "country": country_id,
        "pageSize": 5,
        "sortBy": "publishedAt",
    }

    # Send the request to the News API
    response = requests.get("https://newsapi.org/v2/top-headlines", params=params)

    # Check the status code of the response
    if response.status_code == 200:  # Success
        # Parse the response
        data = response.json()

        # Extract the news articles from the response
        articles = data["articles"]

        # Build the message to send to the user
        message = ""
        for article in articles:
            title = article["title"]
            url = article["url"]
            message += f"\n- {title}: {url}"

        # Send the message to the user
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:  # Error
        logger.error("News API request failed: %s", err)
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="An error occurred while retrieving news"
        )


def joke(update, context):
    """Joke command handler. Sends a joke to the user."""
    # Use the Chuck Norris API to retrieve a joke
    joke_url = "https://api.chucknorris.io/jokes/random"
    response = requests.get(joke_url)
    if response.status_code == 200:  # Success
        # Parse the response and extract the joke
        data = response.json()
        joke = data["value"]
        # Send the joke to the user
        context.bot.send_message(chat_id=update.effective_chat.id, text=joke)
    else:  # Error
        logger.error("Chuck Norris API request failed: %s", err)
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="An error occurred while retrieving a joke"
        )


# Set up command handlers
dispatcher.add_handler(CommandHandler("start", start))

start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler("help", help)
dispatcher.add_handler(help_handler)

about_handler = CommandHandler("about", about)
dispatcher.add_handler(about_handler)

message_handler = CommandHandler("message", message)
dispatcher.add_handler(message_handler)

image_handler = CommandHandler("image", image)
dispatcher.add_handler(image_handler)

weather_handler = CommandHandler("weather", weather)
dispatcher.add_handler(weather_handler)

news_handler = CommandHandler("news", news)
dispatcher.add_handler(news_handler)

joke_handler = CommandHandler("joke", joke)
dispatcher.add_handler(joke_handler)

# Set up message handler
message_handler = MessageHandler(Filters.text, message)
dispatcher.add_handler(message_handler)

# Start the bot
updater.start_polling()

# Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM, or SIGABRT
updater.idle()
