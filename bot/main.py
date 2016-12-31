from objects import glob
from helpers import console
from constants import bcolors
from bot import role
from bot import mycolor
from objects import command

COMMANDS = {
	"!role": command.Command(role.handle, "<color> <name>"),
	"!mycolor": command.Command(mycolor.handle),
	"!mycolour": command.Command(mycolor.handle),
	"!color": command.Command(mycolor.handle)
}

@glob.client.event
async def on_ready():
	# Logged in successfully!
	console.done()
	console.colored("Discord bot logged in as {} ({})".format(glob.client.user.name, glob.client.user.id), bcolors.GREEN)

@glob.client.event
async def on_message(message):
	# The bot has received a message
	for trigger, cmd in COMMANDS.items():
		if message.content.startswith(trigger):
			# This message has triggered the 'i' command
			if cmd.syntax != "":
				# Split 'passed' and 'syntax' arguments
				args = message.content.split(" ")[1:]
				required_args = cmd.syntax.split(" ")

				# Syntax check
				if len(args) < len(required_args):
					# Invalid syntax
					await glob.client.send_message(message.channel, "Wrong syntax: {} {}".format(trigger, cmd.syntax))
					return

			# Syntax is valid. Run the callback
			# We pass the message split by spaces if this command has syntax
			# Otherwise, we pass the message content
			await cmd.callback(message)