import http.client
import json
import threading
import re
from urllib.parse import quote

DISCORD_HOST = "discordapp.com"
MENTION_TEMPLATE = re.compile(r"(<@[0-9]+>)")


class AsyncRequest(threading.Thread):
    def __init__(self, request_type, headers, json_body, url, url_params=None, host=DISCORD_HOST, callback=None):
        threading.Thread.__init__(self)
        self.request_type = request_type
        self.headers = headers
        self.json_body = json_body
        self.host = host
        self.url = url
        self.callback = callback

        if url_params is not None and len(url_params) > 0:
            self.url += "?"
            for key, value in url_params.items():
                self.url += key + "=" + quote(value) + "&"
            self.url = self.url[:-1]

        if self.headers is None:
            self.headers = {}

    def run(self):
        conn = http.client.HTTPConnection(self.host, port=80)
        conn.request(self.request_type, self.url, body=self.json_body, headers=self.headers)
        response = conn.getresponse()
        # print(response.read().decode("UTF-8"))
        if self.callback:
            self.callback.on_response(response)
        else:
            return response  # in case it's ran in sync with main thread


class Response:
    def on_response(self, response):
        pass


def handle_mentions(client, message):
    mentions = []

    matches = MENTION_TEMPLATE.findall(message)
    for match in matches:
        user_id = match[2:-1]  # removes <@...> and leaves the user_id
        user = client.get_user(user_id)
        username = "*unknown*"  # markdown italics for fanciness
        if user:
            username = user.username
        message = message.replace(match, "@"+username)
        mentions.append(user_id)

    return [mentions, message]


def send_message(client, channel_id, message):
    """
    The message content may contain mentions in this form: <@user_id>.
    Note that the user_id is always numerical.
    These mentions are handled auto-magically.
    Use User.mention to generate these mentions.
    """
    mentions, new_message = handle_mentions(client, message)
    headers = {"authorization": client.token, "content-type": "application/json"}
    body = json.dumps({"content": new_message, "mentions": mentions})
    AsyncRequest("POST", headers, body, "/api/channels/" + channel_id + "/messages").start()
