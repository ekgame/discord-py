import random

from commands.command_handler import Command
from plugins.plugin_base import Plugin


class Inventory(Plugin):
    def __init__(self, bot, space):
        bot.register_command(["hold", "take", "put"], CommandHold(self))
        bot.register_command(["inventory", "inv", "holding"], CommandInventory(self))

        self.holding = []
        self.space = space

    def add(self, thing):
        if len(self.holding) >= self.space:
            remove = random.randrange(self.space)
            removed = self.holding[remove]
            self.holding.pop(remove)
            self.holding.append(thing)
            return removed
        else:
            self.holding.append(thing)
            return None


class CommandHold(Command):
    def __init__(self, inventory):
        self.inventory = inventory

    def handle(self, context, args):
        prefix = ""
        if not context.channel.is_private():
            prefix = context.user.mention + " "

        if len(args) > 0:
            thing = " ".join(args)
            dropped = self.inventory.add(thing)

            if dropped:
                context.channel.send_message(prefix + "Now holding **" + thing + "**, but dropped **" + dropped + "**.")
            else:
                context.channel.send_message(prefix + "Now holding **" + thing + "**.")
        else:
            context.channel.send_message(prefix + "What do you want me to hold for you?")


class CommandInventory(Command):
    def __init__(self, inventory):
        self.inventory = inventory

    def handle(self, context, args):
        prefix = ""
        if not context.channel.is_private():
            prefix = context.user.mention + " "

        msg = "At the moment I'm holding "
        if len(self.inventory.holding) > 0:
            i = 0
            for item in self.inventory.holding:
                i += 1
                msg += "**" + item + "**"
                if i == len(self.inventory.holding)-1:
                    msg += " and "
                elif i == len(self.inventory.holding):
                    msg += "."
                else:
                    msg += ", "
        else:
            msg = "My inventory is empty."

        context.channel.send_message(prefix + msg)
