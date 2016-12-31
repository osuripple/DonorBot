import bottle
import json

from objects import glob
from constants import exceptions
from helpers import coro

@bottle.route("/api/v1/give_donor", method="POST")
def give_donor_post():
		data = {
			"status": 200,
			"message": "ok"
		}
		try:
			# Check arguments
			args = ["secret", "discord_id"]
			for i in args:
				if i not in bottle.request.params:
					raise exceptions.InvalidArgumentsError()

			# Check secret
			if glob.secret != bottle.request.forms.get("secret"):
				raise exceptions.InvalidSecretKeyError()

			# Check if the user if in the server
			discord_server = glob.client.get_server(glob.config.config["discord"]["server_id"])
			if discord_server is None:
				raise exceptions.BotNotInServerError()
			discord_user = discord_server.get_member(bottle.request.forms.get("discord_id"))
			if discord_user is None:
				raise exceptions.NotInServerError()

			# Get donators role
			donor_role = None
			for i in discord_server.roles:
				if i.name.lower() == "donators":
					donor_role = i

			# Make sure the donators role exists
			if donor_role is None:
				raise exceptions.NoRoleError()

			# Give donators role to the user
			coro.sync_coroutine(glob.client.add_roles(discord_user, donor_role))
		except exceptions.InvalidArgumentsError:
			data["status"] = 400
			data["message"] = "Missing/invalid arguments"
		except exceptions.InvalidSecretKeyError:
			data["status"] = 403
			data["message"] = "Invalid secret key"
		except exceptions.NotInServerError:
			data["status"] = 404
			data["message"] = "User not in server"
		except exceptions.BotNotInServerError:
			data["status"] = 403
			data["message"] = "Bot not in server"
		except exceptions.NoRoleError:
			data["status"] = 500
			data["message"] = "No donators role found in server"
		except:
			data["status"] = 500
			data["message"] = "Unhandled exception"
		finally:
			json_data = json.dumps(data)
			yield json_data