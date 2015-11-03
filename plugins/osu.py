import json

from commands.command_handler import Command
from discord.actions import Response, AsyncRequest
from plugins.plugin_base import Plugin


class Osu(Plugin):
    def __init__(self, bot, api_key):
        bot.register_command(["osu"], CommandOsu(self))
        self.api_key = api_key

    def on_message_create(self, event):
        pass
        # todo: check for beatmap/user links


class CommandOsu(Command):
    def __init__(self, osu):
        self.osu = osu

    def handle(self, context, args):
        if len(args) > 0:
            username = " ".join(args).strip()
            params = {"k": self.osu.api_key, "u": username}
            AsyncRequest("GET", None, None, "/api/get_user",
                         host="osu.ppy.sh", url_params=params,
                         callback=OsuResponse(self.osu, username, context)).start()
        else:
            context.channel.send_message(context.user.mention + " usage: //osu *username*")


class OsuResponse(Response):

    def __init__(self, osu, username, context):
        self.osu = osu
        self.username = username
        self.context = context
        self.msg_template = "{0} #{1} • {2}#{3} • PP: **{4}**\n• https://osu.ppy.sh/u/{5}"

    def on_response(self, response):

        message = "User *" + self.username + "* not found."
        json_string = response.read().decode("UTF-8")
        data = json.loads(json_string)
        if len(data) > 0:
            osu_user = data[0]
            osu_username = osu_user["username"]
            osu_rank = osu_user["pp_rank"]
            osu_country_rank = osu_user["pp_country_rank"]
            osu_country = osu_user["country"]
            osu_user_id = osu_user["user_id"]
            osu_pp = osu_user["pp_raw"]
            message = self.msg_template.format(osu_username, osu_rank, osu_country, osu_country_rank, osu_pp, osu_user_id)

        user = self.context.user
        channel = self.context.channel
        if channel.is_private():
            channel.send_message(message)
        else:
            channel.send_message(user.mention + " " + message)
