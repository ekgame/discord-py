from commands.command_handler import CommandContext, CommandHandler
from commands.misc_commands import CommandRoll
from discord.client import DiscordClient


class DiscordBot(DiscordClient):
    def __init__(self, email, password):
        super().__init__(email, password)
        self.command_handler = CommandHandler()
        self.register_command(["roll"], CommandRoll())
        self.plugins = []

    def register_command(self, labels, command):
        self.command_handler.add_command(labels, command)

    def register_plugin(self, plugin):
        self.plugins.append(plugin)

    def on_ready(self):
        for plugin in self.plugins:
            plugin.on_ready()

    def on_message_create(self, event):
        for plugin in self.plugins:
            plugin.on_message_create(event)

        if event.content.strip().startswith("//"):
            self.command_handler.handle_command(event.content, CommandContext(event.get_channel(), event.user))
