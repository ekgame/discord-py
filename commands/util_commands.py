from random import randint

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
        num = randint(1, upperbound)
        if context.channel.is_private():
            context.channel.send_message(str(num))
        else:
            context.channel.send_message(context.user.mention + " " + str(num))


class CommandHold(Command):
    def __init__(self):
        self.holding = None

    def handle(self, context, args):
        prefix = ""
        if not context.channel.is_private():
            prefix = context.user.mention + " "

        if len(args) > 0:
            thing = " ".join(args)
            if self.holding:
                context.channel.send_message(prefix + "Dropping **" + self.holding + "** to hold **" + thing + "**.")
            else:
                context.channel.send_message(prefix + "Now holding **" + thing + "**.")
            self.holding = thing
        else:
            context.channel.send_message(prefix + "What do you want me to hold for you?")
