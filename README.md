ChatGPT Telegram Chatbot

# Description

This is a chatbot powered by the OpenAI API and integrated with Telegram. The OpenAI API uses the ChatGPT model to generate responses to user input. ChatGPT is a chatbot that uses the power of artificial intelligence to help you communicate with customers and prospects. The chatbot can be used to answer a wide range of questions, provide helpful information, and engage users in casual conversation.

In addition to answering user questions, the chatbot also provides some other functionality such as generating images, giving the weather forecast, providing news articles, and telling jokes.

The chatbot is easy to use and can be accessed through the popular messaging platform Telegram. It is designed to be user-friendly and can be used by people of all ages and technical backgrounds.

To get started with ChatGPT, simply install the necessary dependencies and obtain API keys for the required services (OpenAI API, Telegram Bot API, OpenWeatherMap API, and NewsAPI). Then, run the chatbot and start having conversations with it through Telegram. Whether you have a question, want to have a casual conversation, or just want to know the latest news or weather forecast, ChatGPT is here to help.

# Features and Functionality

ChatGPT is designed to be a fully-featured chatbot capable of answering a wide range of questions and engaging in natural conversation. Some of its features and functionality include:

    Answering general questions and providing information on a wide range of topics using the ChatGPT model
    Generating images from text with specified parameters using the DALL-E model
    Providing the weather forecast for a specified location using the OpenWeatherMap API
    Providing the latest news headlines using the NewsAPI
    Telling jokes and engaging in a light-hearted conversation using the Chuck Norris API

# Getting Started

To use ChatGPT, you will need to:

    Obtain an API key for the OpenAI API by signing up for a free account at https://beta.openai.com/signup.
    Obtain a bot token for your Telegram bot by following the instructions at https://core.telegram.org/bots#6-botfather.
    Obtain API keys for the OpenWeatherMap API (for weather functionality) and the NewsAPI (for news functionality) by signing up for free accounts at https://home.openweathermap.org/users/sign_up and https://newsapi.org/register, respectively.

# Requirements

    Python 3
    OpenAI API key
    Telegram bot token
    OpenWeatherMap API key
    NewsAPI API key

# Dependencies

    openai
    telegram
    logging
    json
    requests

# Installation

    Create the project folder in /var/www/: mkdir telegram_chatbot
    Navigate to the project directory: cd telegram_chatbot
    Clone the repository: git clone https://github.com/ARTeomo/telegram_chatbot.git
    Copy the chatbot.conf to /etc/apache2/
    Install the required packages: pip install -r 
    Create a configuration file named config.json in the project directory with the following structure:

    {
        "openai_api_key": "<your-openai-api-key>",
        "telegram_bot_token": "<your-telegram-bot-token>",
        "openweathermap_api_key": "<your-openweathermap-api-key>",
        "newsapi_api_key": "<your-newsapi-api-key>"
    }

    Create a configuration file named chatbot.conf in the /etc/apache2/sites-available directory with the following structure:

    <VirtualHost *:443>
        ServerName chatbot.example.com
        ServerAdmin webmaster@example.com
        DocumentRoot /var/www/telegram_chatbot

        WSGIDaemonProcess chatbot user=www-data group=www-data threads=5
        WSGIScriptAlias / /var/www/telegram_chatbot/chatbot.wsgi

        <Directory /var/www/telegram_chatbot>
            WSGIProcessGroup chatbot
            WSGIApplicationGroup %{GLOBAL}
            Order deny,allow
            Allow from all
        </Directory>

        LoadModule ssl_module module modules/mod_ssl.so
        SSLEngine on
        SSLCertificateFile /var/www/telegram_chatbot/ssl/cert.pem
        SSLCertificateKeyFile /var/www/telegram_chatbot/ssl/key.pem

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>

    Run the chatbot: python3 main.py

# Usage

To use the chatbot, simply send a message to the bot on Telegram. The chatbot will respond with an answer or a message indicating that it was unable to understand the request.

The chatbot also has several commands that can be used to trigger specific actions:

    /hlp - show available commands
    /abt - learn more about me
    /msg - send me a message
    /img - generate an image
    /wea - give me the weather forecast
    /news - give me the latest news
    /lol - tell me a joke
 
# Deployment

To deploy the chatbot on an Ubuntu Server with Apache2 and mod_wsgi, follow these steps:

    Install Apache2: sudo apt-get install apache2
    Install mod_wsgi: sudo apt-get install libapache2-mod-wsgi-py3
    Enable mod_wsgi: sudo a2enmod wsgi
    Install the required packages: pip install -r requirements.txt
    Enable the chatbot configuration: sudo a2ensite telegram_chatbot.conf
    Restart Apache: sudo service apache2 restart

# Logging and Error Handling

Logging is enabled by default and logs will be written to the bot.log file in the same directory as main.py. Error handling is also implemented, with the chatbot exiting and logging an error message if the configuration file is not found or there is an error decoding it.

# License

This project is licensed under the MIT License - see the 'LICENSE' file for details.

# Acknowledgements

This chatbot was developed using the OpenAI API and the python-telegram-bot library.