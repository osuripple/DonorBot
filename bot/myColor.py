from objects import glob
import discord

async def handle(message):
	# Make sure the user who has triggered the command is a donor
	discordID = message.author.id
	userInfo = glob.db.fetch("SELECT users.privileges, discord_roles.roleid FROM users LEFT JOIN discord_roles ON users.id = discord_roles.userid WHERE discordid = %s LIMIT 1", [discordID])
	if userInfo == None or userInfo["privileges"] & 4 == 0:
		await glob.client.send_message(message.channel, "**You're not allowed to use this command**, only donors can use it.")
		return

	# Get role object
	roleID = userInfo["roleid"]
	role = None
	for i in message.author.roles:
		if i.id == str(roleID):
			role = i

	# Make sure role is valid
	if role is None:
		await glob.client.send_message(message.channel, "**You don't have a custom role yet.** Please set it using !role command.")
		return

	# Send role color
	await glob.client.send_message(message.channel, "Your custom role color is: **#{}**".format(format(role.colour.value, "x").upper()))