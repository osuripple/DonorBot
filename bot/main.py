"""
Handles basic on_ready and on_message events
"""
from objects import glob
from helpers import consoleHelper as console
from constants import bcolors
from bot import role
from bot import myColor

COMMANDS = [
	#{
	#	"trigger": "!hello",
	#	"callback": lambda message: glob.client.send_message(message.channel, "Hi!")
	#},
	{
		"trigger": "!role",
		"syntax": "<color> <name>",
		"callback": role.handle
	}, {
		"trigger": "!mycolor",
		"callback": myColor.handle
	}, {
		"trigger": "!mycolour",
		"callback": myColor.handle
	}, {
		"trigger": "!color",
		"callback": myColor.handle
	}
]

# Commands list default values
for i in COMMANDS:
	i.setdefault("trigger", None)
	i.setdefault("syntax", "")
	i.setdefault("callback", lambda message: glob.client.send_message(message.channel, "No callback function set for this command."))

@glob.client.event
async def on_ready():
	# Logged in successfully!
	console.done()
	console.colored("Discord bot logged in as {} ({})".format(glob.client.user.name, glob.client.user.id), bcolors.GREEN)

@glob.client.event
async def on_message(message):
	# The bot has received a message
	for i in COMMANDS:
		if message.content.startswith(i["trigger"]):
			# This message has triggered the 'i' command
			if i["syntax"] != "":
				# Split 'passed' and 'syntax' arguments
				args = message.content.split(" ")[1:]
				requiredArgs = i["syntax"].split(" ")

				# Syntax check
				if len(args) < len(requiredArgs):
					# Invalid syntax
					await glob.client.send_message(message.channel, "Wrong syntax: {} {}".format(i["trigger"], i["syntax"]))
					return

			# Syntax is valid. Run the callback
			# We pass the message split by spaces if this command has syntax
			# Otherwise, we pass the message content
			await i["callback"](message)