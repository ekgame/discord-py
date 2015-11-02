from commands.command_handler import CommandContext, CommandHandler
from commands.util_commands import CommandRoll, CommandHold
from discord.client import DiscordClient


class DiscordBot(DiscordClient):
    def __init__(self, email, password):
        super().__init__(email, password)
        self.command_handler = CommandHandler()
        self.command_handler.add_command(["roll"], CommandRoll())
        self.command_handler.add_command(["hold"], CommandHold())

    def on_ready(self):
        # for key, channel in self.private_channels.items():
        #    channel.send_message("Hello " + channel.user.mention)
        pass

    def on_message_create(self, event):
        if event.content.strip().startswith("//"):
            self.command_handler.handle_command(event.content, CommandContext(event.get_channel(), event.user))
