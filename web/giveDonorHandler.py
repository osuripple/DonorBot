import bottle
import json
from objects import glob
from constants import exceptions
from helpers import coroutineHelper

@bottle.route("/api/v1/give_donor", method="POST")
def POSTGiveDonor():
		data = {
			"status": 200,
			"message": "ok"
		}
		try:
			# Check arguments
			args = ["secret", "discord_id"]
			for i in args:
				if i not in bottle.request.params:
					raise exceptions.invalidArguments()

			# Check secret
			if glob.secret != bottle.request.forms.get("secret"):
				raise exceptions.invalidSecretKey()

			# Check if the user if in the server
			discordServer = glob.client.get_server(glob.config.config["discord"]["server_id"])
			if discordServer == None:
				raise exceptions.botNotInServer()
			discordUser = discordServer.get_member(bottle.request.forms.get("discord_id"))
			if discordUser == None:
				raise exceptions.notInServer()

			# Get donators role
			donorRole = None
			for i in discordServer.roles:
				if i.name.lower() == "donators":
					donorRole = i

			# Make sure the donators role exists
			if donorRole == None:
				raise exceptions.noRole()

			# Give donators role to the user
			coroutineHelper.syncCoroutine(glob.client.add_roles(discordUser, donorRole))
		except exceptions.invalidArguments:
			data["status"] = 400
			data["message"] = "Missing/invalid arguments"
		except exceptions.invalidSecretKey:
			data["status"] = 403
			data["message"] = "Invalid secret key"
		except exceptions.notInServer:
			data["status"] = 404
			data["message"] = "User not in server"
		except exceptions.botNotInServer:
			data["status"] = 403
			data["message"] = "Bot not in server"
		except exceptions.noRole:
			data["status"] = 500
			data["message"] = "No donators role found in server"
		except:
			data["status"] = 500
			data["message"] = "Unhandled exception"
		finally:
			jsonData = json.dumps(data)
			yield jsonData