from objects import glob
import re
import discord

def isHexColor(col):
	hexRegex = re.compile("^(?:[0-9a-fA-F]{3}){1,2}$")
	return True if hexRegex.match(col) != None else False

async def handle(message):
	# Make sure the user who has triggered the command is a donor
	discordID = message.author.id
	userInfo = glob.db.fetch("SELECT users.privileges, discord_roles.roleid FROM users LEFT JOIN discord_roles ON users.id = discord_roles.userid WHERE discordid = %s LIMIT 1", [discordID])
	if userInfo == None or userInfo["privileges"] & 4 == 0:
		await glob.client.send_message(message.channel, "You're not allowed to use this command, only donors can use it.")
		return

	# Get arguments
	args = message.content.split(" ")[1:]
	roleColor = args[0]
	roleName = " ".join(args[1:])

	# Remove # from HEX color
	if roleColor.startswith("#") == True:
		roleColor = roleColor[1:]

	# Make sure the color is valid
	if isHexColor(roleColor) == False:
		await glob.client.send_message(message.channel, "Invalid HEX color. Use this tool to choose your color: http://www.colorpicker.com/. The HEX color is the one that starts with '#'.")
		return

	# Convert the color from HEX to int
	roleColor = int(roleColor, 16)

	async def createCustomRole():
		# Set right permissions
		rolePermissions = message.server.default_role
		rolePermissions = rolePermissions.permissions
		rolePermissions.change_nickname = True

		# Get donators role (to set right position)
		donorRole = None
		for i in message.server.roles:
			if i.name.lower() == "donators":
				donorRole = i
		if donorRole == None:
			await glob.client.send_message(message.channel, "Error while creating your role! Missing 'donators' role. Please contact a developer.")
			return

		# Create the role, set the position and add it
		role = await glob.client.create_role(message.server, name=roleName, permissions=rolePermissions, colour=discord.Colour(roleColor), hoist=False, mentionable=False)
		await glob.client.move_role(message.server, role, donorRole.position)
		await glob.client.add_roles(message.author, role)
		glob.db.execute("UPDATE discord_roles SET roleid = %s WHERE discordid = %s", [role.id, message.author.id])
		await glob.client.send_message(message.channel, "Your role has been created successfully! Welcome to the donors club!")
		return

	async def editCustomRole(roleID):
		# Get role object
		role = None
		for i in message.author.roles:
			if i.id == roleID:
				role = i

		if role == None:
			# Role not found, reset role in db and create a new one
			glob.db.execute("UPDATE discord_roles SET roleid = 0 WHERE discordid = %s", [message.author.id])
			return await createCustomRole()

		# Role object found, update it
		await glob.client.edit_role(message.server, role, name=roleName, colour=discord.Colour(roleColor))
		await glob.client.send_message(message.channel, "Your custom role has been edited successfully!")
		return

	# Determine if this user has already a custom role
	if userInfo["roleid"] != 0:
		await editCustomRole(str(userInfo["roleid"]))
	else:
		await createCustomRole()