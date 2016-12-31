import re
import discord

from objects import glob

def is_hex_color(col):
	hex_regex = re.compile("^(?:[0-9a-fA-F]{3}){1,2}$")
	return True if hex_regex.match(col) is not None else False

async def handle(message):
	# Make sure the user who has triggered the command is a donor
	discord_id = message.author.id
	user_info = glob.db.fetch("SELECT users.privileges, discord_roles.roleid FROM users LEFT JOIN discord_roles ON users.id = discord_roles.userid WHERE discordid = %s LIMIT 1", [discord_id])
	if user_info is None or user_info["privileges"] & 4 == 0:
		await glob.client.send_message(message.channel, "**You're not allowed to use this command**, only donors can use it.")
		return

	# Make sure the user is not abusing the command
	if not glob.rate_limiters["!role"].check(discord_id):
		await glob.client.send_message(message.channel, "**You can use the !role command only once every 5 minutes.** Please try again later.")
		return

	# Get arguments
	args = message.content.split(" ")[1:]
	role_color = args[0]
	role_name = " ".join(args[1:])

	# Remove # from HEX color
	if role_color.startswith("#"):
		role_color = role_color[1:]

	# Make sure the color is valid
	if not is_hex_color(role_color):
		await glob.client.send_message(message.channel, "**Invalid HEX color.** Use this tool to choose your color: http://www.colorpicker.com/. The HEX color is the one that starts with '#'.")
		return

	# Convert the color from HEX to int
	role_color = int(role_color, 16)

	async def create_custom_role():
		# Set right permissions
		role_permissions = message.server.default_role
		role_permissions = role_permissions.permissions
		role_permissions.change_nickname = True

		# Get donators role (to set right position)
		donor_role = None
		for i in message.server.roles:
			if i.name.lower() == "donators":
				donor_role = i
		if donor_role == None:
			await glob.client.send_message(message.channel, "**Error while creating your role!** Missing 'donators' role. Please contact a developer.")
			return

		# Create the role, set the position and add it
		role = await glob.client.create_role(message.server, name=role_name, permissions=role_permissions, colour=discord.Colour(role_color), hoist=False, mentionable=False)
		await glob.client.move_role(message.server, role, donor_role.position)
		await glob.client.add_roles(message.author, role)
		glob.db.execute("UPDATE discord_roles SET roleid = %s WHERE discordid = %s LIMIT 1", [role.id, message.author.id])
		await glob.client.send_message(message.channel, "**Your role has been created successfully! Welcome to the donors club!**")
		return

	async def edit_custom_role(roleID):
		# Get role object
		role = None
		for i in message.author.roles:
			if i.id == roleID:
				role = i

		if role is None:
			# Role not found, reset role in db and create a new one
			glob.db.execute("UPDATE discord_roles SET roleid = 0 WHERE discordid = %s LIMIT 1", [message.author.id])
			return await create_custom_role()

		# Role object found, update it
		await glob.client.edit_role(message.server, role, name=role_name, colour=discord.Colour(role_color))
		await glob.client.send_message(message.channel, "**Your custom role has been edited successfully!**")
		return

	# Determine if this user has already a custom role
	if user_info["roleid"] != 0:
		await edit_custom_role(str(user_info["roleid"]))
	else:
		await create_custom_role()