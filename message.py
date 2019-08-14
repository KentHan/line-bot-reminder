# -*- coding: utf-8 -*-

import os

from linebot import LineBotApi
from linebot.models import (
    TextMessage,
    TemplateSendMessage,
    ConfirmTemplate, MessageTemplateAction
)

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')


class MessageApi():

    def __init__(self, user_id = None, reply_token=None):
        self.user_id = user_id
        self.reply_token = reply_token

    def set_user_id(self, user_id):
        self.user_id = user_id

    def reply_text_message(self, text):
        reply_text_message(self.reply_token, text)

    def push_reset_confirm_message(self, event_name, event_desc):
        push_reset_confirm_message(self.user_id, event_name, event_desc)


def reply_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    message = TextMessage("1", text)
    line_bot_api.reply_message(reply_token, message)


def push_reset_confirm_message(target_id, event_name, event_desc):
    message = TemplateSendMessage(
        alt_text="Confirm Reset",
        template=ConfirmTemplate(
            text=f"{event_desc}你想要重置這個提醒嗎？",
            actions=[
                MessageTemplateAction(
                    label="Yes",
                    text=f"/reset {event_name}"
                ),
                MessageTemplateAction(
                    label="No",
                    text="/do_nothing"
                )
            ]
        )
    )
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(target_id, message)
