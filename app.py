# -*- coding: utf-8 -*-

import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

from flask import Flask, render_template, request, redirect, url_for

from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from bo import EventBO
from message import reply_text_message, push_reset_confirm_message, MessageApi

app = Flask(__name__)

channel_secret = os.getenv('LINE_CHANNEL_SECRET')
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

MESSAGE_HELP = """
* 加入事件
/add <事件名> <提醒間隔(天)> <指定時間>
例如：/add 洗衣服 1 20:00
    
* 重置提醒
/reset <事件名>

* 移除事件
/remove <事件名>

* 列出所有事件
/list
"""

MESSAGE_ERROR = "我看不懂，試試看輸入 /help"
MESSAGE_OK = "OK!"


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>')
def send_static_file(file_name):
    return app.send_static_file(file_name)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


@app.route("/callback", methods=['POST'])
def callback():
    if channel_secret is None:
        print('Specify LINE_CHANNEL_SECRET as environment variable.')
        sys.exit(1)
    if channel_access_token is None:
        print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
        sys.exit(1)

    line_bot_api = LineBotApi(channel_access_token)
    parser = WebhookParser(channel_secret)
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)
    print("Request body: %s" % body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
        for event in events:
            if isinstance(event, MessageEvent):
                handle_message(event)
    except InvalidSignatureError:
        abort(400)

    return 'OK~~'


@app.route("/api/list_event", methods=['GET'])
def list_event():
    bo = EventBO()
    bo.handle_list_command(user_id)


def handle_message(event):
    user_id = event.source.sender_id
    source_type = event.source.type
    reply_token = event.reply_token
    text = event.message.text

    message_api = MessageApi(user_id, reply_token)
    bo = EventBO()
    bo.set_message_api(message_api)

    if text.startswith("/add"):
        result = bo.handle_add_command(user_id, command_parser(text))
    elif text.startswith("/remove"):
        result = bo.handle_remove_command(user_id, command_parser(text))
    elif text.startswith("/reset"):
        result = bo.handle_reset_command(user_id, command_parser(text))
    elif text.startswith("/list"):
        bo.handle_list_command(user_id, command_parser(text))
    elif text.startswith("/help"):
        send_text_message(reply_token, MESSAGE_HELP)
    elif text.startswith("/test"):
        send_reset_confirm_message(reply_token, "test_event_desc")
    elif text.startswith("/do_nothing"):
        pass
    else:
        if source_type == "user":
            reply_text_message(reply_token, MESSAGE_ERROR)
        else:
            return

    if "result" in locals():
        if result:
            reply_text_message(reply_token, MESSAGE_OK)
        else:
            reply_text_message(reply_token, MESSAGE_ERROR)


def command_parser(input):
    input = input.strip()
    options_start_index = input.find(" ") + 1
    if options_start_index == 0:
        return {}
    else:
        options_string = input[options_start_index:]
        keys = ["name", "interval", "alarm_time"]
        values = options_string.split(" ")
        return dict(zip(keys, values))


if __name__ == '__main__':
    app.run(debug=True)
