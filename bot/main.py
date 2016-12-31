"""
Handles basic on_ready and on_message events
"""
from objects import glob
from helpers import consoleHelper as console
from constants import bcolors
from bot import role
from bot import myColor

from objects import command

COMMANDS = {
	"!role": command.Command(role.handle, "<color> <name>"),
	"!mycolor": command.Command(myColor.handle),
	"!mycolour": command.Command(myColor.handle),
	"!color": command.Command(myColor.handle)
}

@glob.client.event
async def on_ready():
	# Logged in successfully!
	console.done()
	console.colored("Discord bot logged in as {} ({})".format(glob.client.user.name, glob.client.user.id), bcolors.GREEN)

@glob.client.event
async def on_message(message):
	# The bot has received a message
	for trigger, command in COMMANDS.items():
		if message.content.startswith(trigger):
			# This message has triggered the 'i' command
			if command.syntax != "":
				# Split 'passed' and 'syntax' arguments
				args = message.content.split(" ")[1:]
				requiredArgs = command.syntax.split(" ")

				# Syntax check
				if len(args) < len(requiredArgs):
					# Invalid syntax
					await glob.client.send_message(message.channel, "Wrong syntax: {} {}".format(trigger, command.syntax))
					return

			# Syntax is valid. Run the callback
			# We pass the message split by spaces if this command has syntax
			# Otherwise, we pass the message content
			await command.callback(message)