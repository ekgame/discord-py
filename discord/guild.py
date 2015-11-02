from discord.channels import PublicChannel
from discord.users import Member


class Guild:
    def __init__(self, client, guild_data):
        self.client = client
        self.afk_channel_id = guild_data["afk_channel_id"]
        self.afk_timeout = guild_data["afk_timeout"]
        self.icon = guild_data["icon"]
        self.id = guild_data["id"]
        self.joined_at = guild_data["joined_at"]
        self.large = guild_data.get("large", False)
        self.name = guild_data["name"]
        self.owner_id = guild_data["owner_id"]
        self.region = guild_data["region"]

        self.members = {}
        for member_data in guild_data["members"]:
            member = Member(member_data)
            client.add_user(member.user)
            self.members[member.user.id] = member

        self.channels = {}
        for channel_data in guild_data["channels"]:
            channel = PublicChannel(client, self, channel_data)
            self.channels[channel.id] = channel
            client.add_channel(channel)

        # TODO: presences
        # TODO: roles
        # TODO: voice states


class Role:
    def __init__(self, role_data):
        self.color = role_data["color"]
        self.hoist = role_data["hoist"]
        self.id = role_data["id"]
        self.managed = role_data.get("managed", False)
        self.name = role_data["name"]
        self.permissions = role_data["permissions"]
        self.position = role_data["position"]
