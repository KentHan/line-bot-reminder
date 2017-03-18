# -*- coding: utf-8 -*-

import os
import logging

from linebot import LineBotApi
from linebot.models import TextMessage

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

class MessageApi():

	def send_text_message(self, user_id, text):
		send_text_message(user_id, text)

def send_text_message(self, user_id, text):
	line_bot_api = LineBotApi(channel_access_token)
	message = TextMessage("1", text)
	line_bot_api.push_message(user_id, message)