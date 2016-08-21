import json
import os

class configStatus:
	DOESNT_EXIST = -1
	INVALID = -2
	INVALID_SYNTAX = -3
	VALID = 1

class config:
	def __init__(self):
		"""
		Initializes and loads a config file object
		"""
		self.config = {}
		self.status = configStatus.INVALID_SYNTAX
		self.structure = {
			"database": {
				"host": "",
				"username": "",
				"password": "",
				"database": "",
			}, "web_server": {
				"host": "127.0.0.1",
				"port": 8888,
				"debug": False,
				"secret": "changeme",
			}, "discord": {
				"token": "",
				"server_id": "",
			}
		}

		self.load()

	def load(self):
		try:
			# Make sure the file exists
			if os.path.isfile("config.json") == False:
				self.status = configStatus.DOESNT_EXIST
				return

			# Read and parse the file
			try:
				with open("config.json", "r") as f:
					self.config = json.loads(f.read())
			except ValueError:
				self.status = configStatus.INVALID_SYNTAX
				return

			# Check config file structure
			if self.check() == False:
				self.status = configStatus.INVALID
				return

			# Loaded successfully
			self.status = configStatus.VALID
		except:
			# Error while loading the file
			return


	def check(self):
		"""
		Check self.config structure

		return -- True if valid, False if invalid
		"""
		def shape(d):
			"""Get database structure"""
			if isinstance(d, dict):
				return {k:shape(d[k]) for k in d}
			else:
				return None

		return shape(self.config) == shape(self.structure)


	def writeDefault(self):
		"""
		Overwrites config.json with a default one
		"""
		with open("config.json", "w") as f:
			f.write(json.dumps(self.structure, sort_keys=True, indent=4))
