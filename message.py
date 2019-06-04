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

    def __init__(self, reply_token=None):
        self.reply_token = reply_token

    def send_text_message(self, text):
        send_text_message(self.reply_token, text)

    def send_reset_confirm_message(self, event_name, event_desc):
        send_reset_confirm_message(self.reply_token, event_name, event_desc)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    message = TextMessage("1", text)
    line_bot_api.reply_message(reply_token, message)


def send_reset_confirm_message(reply_token, event_name, event_desc):
    message = TemplateSendMessage(
        alt_text="Confirm Reset",
        template=ConfirmTemplate(
            text="{}你想要重置這個提醒嗎？".format(event_desc),
            actions=[
                MessageTemplateAction(
                    label="Yes",
                    text="/reset {}".format(event_name)
                ),
                MessageTemplateAction(
                    label="No",
                    text="/do_nothing"
                )
            ]
        )
    )
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, message)
