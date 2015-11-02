import http.client, urllib.parse, json
import threading

from discord.actions import send_message
from discord.channels import PrivateChannel
from discord.guild import Guild
from discord.messages.message_create import MessageCreate
from discord.users import User
from ws4py.client.threadedclient import WebSocketClient
from time import sleep
from datetime import datetime


class Heartbeat(threading.Thread):
    def __init__(self, interval, client):
        threading.Thread.__init__(self)
        self.interval = interval
        self.client = client

    def run(self):
        while True:
            sleep(self.interval/1000)
            self.client.do_heartbeat()


class DiscordWS(WebSocketClient):
    def __init__(self, url, token, callback):
        super().__init__(url)
        self.token = token
        self.callback = callback
        self.heartbeat = None

    def start(self):
        self.connect()
        self.run_forever()

    def opened(self):
        self.send_json({"op": 2, "d": {"token": self.token, "v": 2, "properties": {"$os": "Linux", "$browser": "StorasBot", "$device": "StorasBot", "$referer": "", "$refering_domain": ""}, }})
        print("Opened")

    def closed(self, code, reason=None):
        if self.heartbeat:
            self.heartbeat.stop()
        print("Closed", code, reason)

    def received_message(self, message):
        self.handle_message(json.loads(message.data.decode("utf-8")))
        print("message: ", message.data)

    def send_json(self, data):
        self.send(json.dumps(data))

    def handle_message(self, message):
        msg_type = message["t"]
        msg_data = message["d"]

        if msg_type == "READY":
            self.heartbeat = Heartbeat(msg_data["heartbeat_interval"], self).start()
            self.callback.handle_ready(msg_data)
        elif msg_type == "MESSAGE_CREATE":
            msg = MessageCreate(self.callback, msg_data)
            self.callback.add_user(msg.user)
            self.callback.on_message_create(msg)

    def do_heartbeat(self):
        self.send_json({"op": 1, "d": datetime.now().microsecond})


class DiscordClient:

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.channels = {}
        self.token = None
        self.ws = None

        # defined after "MESSAGE_READY"
        self.user = None
        self.session_id = None
        self.guilds = {}
        self.private_channels = {}
        self.users = {}

    def login(self):
        self.token = self.get_token()
        url = self.get_gateway()
        self.ws = DiscordWS(url, self.token, self)
        self.ws.start()

    def stop(self):
        if self.ws:
            self.ws.close()

    def get_token(self):
        headers = {"content-type": "application/json"}
        body = json.dumps({"email": self.email, "password": self.password})
        conn = http.client.HTTPConnection("discordapp.com", port=80)
        conn.request("POST", "/api/auth/login", body=body, headers=headers)
        response = conn.getresponse()
        data = response.read()
        # TODO: check for errors
        return json.loads(data.decode("utf-8"))["token"]

    def get_gateway(self):
        headers = {"authorization": self.token}
        conn = http.client.HTTPConnection("discordapp.com", port=80)
        conn.request("GET", "/api/gateway", headers=headers)
        response = conn.getresponse()
        data = response.read()
        # TODO: check for errors
        return json.loads(data.decode("utf-8"))["url"]

    def add_channel(self, channel):
        self.channels[channel.id] = channel

    def get_channel(self, channel_id):
        if channel_id in self.channels:
            return self.channels[channel_id]
        elif channel_id in self.private_channels:
            return self.private_channels[channel_id]
        else:
            return None

    def add_user(self, user):
        if user.id not in self.users:
            self.users[user.id] = user

    def get_user(self, user_id):
        if user_id in self.users:
            return self.users[user_id]
        else:
            return None

    def send_message(self, channel_id, message):
        send_message(self, channel_id, message)

    def handle_ready(self, ready_data):
        for private_channel in ready_data["private_channels"]:
            channel_obj = PrivateChannel(self, private_channel)
            self.private_channels[channel_obj.id] = channel_obj

        for guild in ready_data["guilds"]:
            guild_obj = Guild(self, guild)
            self.guilds[guild_obj.id] = guild_obj

        self.user = User(ready_data["user"])
        print(self.user.id)
        self.add_user(self.user)
        self.session_id = ready_data["session_id"]
        self.on_ready()

    def on_ready(self):
        pass

    def on_message_create(self, event):
        pass
