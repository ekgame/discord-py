from discord.users import User


class MessageCreate:
    def __init__(self, client, data):
        self.client = client
        self.user = User(data["author"])
        self.channel_id = data["channel_id"]
        self.content = data["content"]
        self.timestamp = data["timestamp"]
        # TODO: other parameters

    def get_channel(self):
        return self.client.get_channel(self.channel_id)
