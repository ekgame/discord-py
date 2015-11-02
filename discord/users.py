class User:
    def __init__(self, user_data):
        self.username = user_data["username"]
        self.id = user_data["id"]
        self.discriminator = user_data["discriminator"]
        self.avatar = user_data["avatar"]
        self.mention = "<@" + self.id + ">"

        # only available when parsing user from "MESSAGE_READY"
        self.verified = user_data.get("verified", None)
        self.email = user_data.get("email", None)

    def get_avatar(self):
        return "https://cdn.discordapp.com/avatars/" + self.id + "/" + self.avatar + ".jpg"


class Member:
    def __init__(self, member_data):
        self.user = User(member_data["user"])
        self.roles = member_data["roles"]
        self.mute = member_data["mute"]
        self.deaf = member_data["deaf"]
        self.joined_at = member_data["joined_at"]
