#!/usr/bin/python3

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/telegram_chatbot")

from main import webhook_server

application = webhook_server.bot
