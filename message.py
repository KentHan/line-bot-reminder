# -*- coding: utf-8 -*-

import os
import logging

from linebot import LineBotApi
from linebot.models import (
    MessageEvent, TextMessage,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate, ConfirmTemplate, CarouselTemplate,
    PostbackTemplateAction, MessageTemplateAction, URITemplateAction,
    CarouselColumn
)

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

class MessageApi():

	def send_text_message(self, user_id, text):
		send_text_message(user_id, text)

	def send_template_confirm_message(self, user_id):
		send_template_confirm_message(user_id)

def send_text_message(user_id, text):
	line_bot_api = LineBotApi(channel_access_token)
	message = TextMessage("1", text)
	line_bot_api.push_message(user_id, message)

def send_template_confirm_message(user_id):
	line_bot_api = LineBotApi(channel_access_token)
	reset_action = MessageTemplateAction("Yes", "/help")
	do_nothing_action = MessageTemplateAction("No", "/help")
	actions = [reset_action, do_nothing_action]
	confirm_template = ConfirmTemplate("Do you want to reset?", actions)
	message = TemplateSendMessage("Confirm Template", confirm_template)
	line_bot_api.push_message(user_id, message)
