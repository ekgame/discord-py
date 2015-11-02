from discord.users import User


class Channel:
    def __init__(self, client, channel_data):
        self.client = client
        self.id = channel_data["id"]
        self.last_message_id = channel_data["last_message_id"]

    def send_message(self, message):
        self.client.send_message(self.id, message)

    def is_private(self):
        pass


class PublicChannel(Channel):
    def __init__(self, client, guild, channel_data):
        super().__init__(client, channel_data)
        self.guild = guild
        self.name = channel_data["name"]
        self.position = channel_data["position"]
        self.topic = channel_data["topic"]
        self.type = channel_data["type"]
        # TODO: permission overrides

    def is_private(self):
        return False


class PrivateChannel(Channel):
    def __init__(self, client, channel_data):
        super().__init__(client, channel_data)
        self.user = User(channel_data["recipient"])
        self.last_message_id = channel_data["last_message_id"]
        self.id = channel_data["id"]
        client.add_user(self.user)

    def is_private(self):
        return True
