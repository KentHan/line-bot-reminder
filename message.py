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

    def send_reset_confirm_message(self, user_id, event_name):
        send_reset_confirm_message(user_id, event_name)


def send_text_message(user_id, text):
    line_bot_api = LineBotApi(channel_access_token)
    message = TextMessage("1", text)
    line_bot_api.push_message(user_id, message)


def send_reset_confirm_message(user_id, event_name):
    message = TemplateSendMessage(
        alt_text="Confirm Reset",
        template=ConfirmTemplate(
            text="Do you want to reset {}?".format(event_name),
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
    line_bot_api.push_message(user_id, message)
