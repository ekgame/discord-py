class Command:
    def handle(self, context, args):
        pass


class CommandContext:
    def __init__(self, channel, user):
        self.channel = channel
        self.user = user


class CommandHandler:
    def __init__(self):
        self.command_prefix = "//"
        self.commands = {}

    def add_command(self, labels, executor):
        for label in labels:
            self.commands[label] = executor

    def handle_command(self, command, context):
        command = command[len(self.command_prefix):]
        args = command.split(" ")
        if args[0] in self.commands:
            self.commands[args[0]].handle(context, args[1:])
