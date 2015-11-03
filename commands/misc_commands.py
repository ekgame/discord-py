import random

from commands.command_handler import Command


def is_int(x):
    try:
        int(x)
        return True
    except ValueError:
        return False


class CommandRoll(Command):
    def handle(self, context, args):
        upperbound = 6
        if len(args) > 0 and is_int(args[0]):
            upperbound = int(args[0])
        if upperbound < 1:
            upperbound = 6
        num = random.randint(1, upperbound)
        if context.channel.is_private():
            context.channel.send_message(str(num))
        else:
            context.channel.send_message(context.user.mention + " " + str(num))