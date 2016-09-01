import bottle
import time
import json
from objects import glob
from constants import exceptions
from helpers import coroutineHelper

@bottle.route("/api/v1/clear_donor", method="POST")
def POSTClearDonor():
	data = {
		"status": 200,
		"message": "ok"
	}
	try:
		# Get discord expired donors
		expired = glob.db.fetchAll("SELECT discord_roles.discordid, discord_roles.roleid, users.id FROM discord_roles RIGHT JOIN users ON users.id = discord_roles.userid WHERE users.privileges & 4 > 0 AND donor_expire <= %s", [int(time.time())])

		# Do all the work if the query has returned something
		if expired != None:
			# Get discord server object and make sure it's valid
			discordServer = glob.client.get_server(glob.config.config["discord"]["server_id"])
			if discordServer == None:
				raise exceptions.notInServer()

			# Get donators role object
			donorRole = None
			for i in discordServer.roles:
				if i.name.lower() == "donators":
					donorRole = i

			# Make sure the donorRole is valid
			if donorRole == None:
				coroutineHelper.syncCoroutine(glob.client.send_message(discordServer.get_default_channel(), "Error while cleaning expired donors! Looks like the donators role is gone! Nyo-sama where are you? :'("))
				raise exceptions.noRole()

			# Remove donators and custom roles to expired donors
			for i in expired:
				print("Removing donor for user {}".format(i["id"]))

				# First, remove donor badge
				glob.db.execute("DELETE FROM user_badges WHERE user = %s AND badge = '14'", [i["id"]])

				# Then, do discord stuff
				# Make sure the discord id is valid
				if i["discordid"] == None or i["discordid"] == 0:
					continue

				# Get the user and make sure he is still inside the server	
				discordUser = discordServer.get_member(str(i["discordid"]))
				if discordUser == None:
					continue

				# Remove donators role
				coroutineHelper.syncCoroutine(glob.client.remove_roles(discordUser, donorRole))

				# Update db
				glob.db.execute("UPDATE discord_roles SET roleid = 0 WHERE discordid = %s", [i["discordid"]])

				# Get the custom role
				customRole = None
				for j in discordServer.roles:
					if j.id == str(i["roleid"]):
						customRole = j

				# Make sure the custom role is valid
				if customRole == None:
					continue

				# Delete custom role from server
				coroutineHelper.syncCoroutine(glob.client.delete_role(discordServer, customRole))

		# Remove website and ingame expired donor privilege
		glob.db.execute("UPDATE users SET privileges = privileges & ~4 WHERE privileges & 4 > 0 AND donor_expire <= %s", [int(time.time())])
	except exceptions.invalidSecretKey:
		data["status"] = 403
		data["message"] = "Bot not in server"
	except exceptions.noRole:
		data["status"] = 500
		data["message"] = "Donators role not found"
	except:
		data["status"] = 500
		data["message"] = "Unhandled exception"
		raise
	finally:
		jsonData = json.dumps(data)
		yield jsonData