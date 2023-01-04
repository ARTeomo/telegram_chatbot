#!/usr/bin/python3
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/telegram_chatbot')

from main import updater

application = updater.dispatcher.bot
