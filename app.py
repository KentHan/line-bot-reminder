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
from message import send_text_message

app = Flask(__name__)

channel_secret = os.getenv('LINE_CHANNEL_SECRET')
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

MESSAGE_HELP = """
* 加入事件
/add <事件名> <提醒間隔(秒)> <指定時間>
例如：/add 洗衣服 86400 20:00
    
* 重置提醒
/reset <事件名>

* 移除事件
/remove <事件名>

* 列出所有事件
/list
"""

MESSAGE_ERROR = "我看不懂，試試看輸入 /help"
MESSAGE_OK = "OK!~~"

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

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


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

def handle_message(event):
    user_id = event.source.sender_id
    source_type = event.source.type
    
    text = event.message.text
    bo = EventBO()

    if text.startswith("/add"):
        result = bo.handle_add_command(user_id, command_parser(text))
    elif text.startswith("/remove"):
        result = bo.handle_remove_command(user_id, command_parser(text))
    elif text.startswith("/reset"):
        result = bo.handle_reset_command(user_id, command_parser(text))
    elif text.startswith("/list"):
        bo.handle_list_command(user_id, command_parser(text))
    elif text.startswith("/help"):
        send_text_message(user_id, MESSAGE_HELP)
    else:
        if source_type == "user":
            send_text_message(user_id, MESSAGE_ERROR)
        else:
            return

    if "result" in locals():
        if result:
            send_text_message(user_id, MESSAGE_OK)
        else:
            send_text_message(user_id, MESSAGE_ERROR)

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
