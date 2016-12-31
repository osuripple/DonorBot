class Command:
	def __init__(self, callback, syntax=""):
		"""
		Instantiate a discord bot command

		:param callback: Function object to call when the command is triggered.
						 must accept a `message` argument, containing the discord Message object
						 that triggered the command
		:param syntax: String that contains command's syntax. It's used to check if the message
					   that should trigger this command has enough parameters.
					   Eg: "<arg1> <arg2>"
		"""
		self.syntax = syntax
		self.callback = callback