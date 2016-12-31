from gevent import monkey as brit_monkey
brit_monkey.patch_all()
import os
import sys
import threading

import discord
import bottle
import MySQLdb

from helpers import console
from objects import glob
from objects import config
from constants import bcolors
from helpers import database
from objects import rate_limit
from web import give_donor
from web import clear_donor

def bottleWorker(host, port):
	bottle.run(host=host, port=port, server="gevent")

if __name__ == "__main__":
	# Create folders if needed
	console.printn("> Checking folders...")
	paths = [".data"]
	for i in paths:
		if not os.path.exists(i):
			os.makedirs(i, 0o770)
	console.done()

	# Load and check config.json
	console.printn("> Loading config file...")
	glob.config = config.Config()
	# TODO: Use exceptions
	if glob.config.status != config.ConfigStatus.VALID:
		console.warning()

		if glob.config.status == config.ConfigStatus.DOESNT_EXIST:
			console.colored("> The config file doesn't exist", bcolors.YELLOW)
		elif glob.config.status == config.ConfigStatus.INVALID:
			console.colored("> The config file has an invalid structure", bcolors.YELLOW)
		elif glob.config.status == config.ConfigStatus.INVALID_SYNTAX:
			console.colored("> Couldn't parse config.json", bcolors.YELLOW)
		else:
			console.colored("> Unknown error", bcolors.YELLOW)

		yn = input("> Do you want to generate a default config.json? (y/n): ")
		if yn == "y":
			console.printn("> Generating default config.json...")
			glob.config.write_default()
			console.done()
		sys.exit(0)
	console.done()

	# Connect to ripple database
	try:
		console.printn("> Connecting to ripple database")
		db_config = glob.config.config["database"]
		glob.db = database.Db(
			db_config["host"],
			db_config["username"],
			db_config["password"],
			db_config["database"],
		)
		console.done()
	except (ValueError, MySQLdb.Error):
		console.error()
		raise

	# Create rate limiters
	glob.rate_limiters["!role"] = rate_limit.RateLimiter(1, 300)

	# Start tornado
	console.printn("> Starting Bottle...")

	# Read port and secret
	try:
		serverPort = int(glob.config.config["web_server"]["port"])
		serverHost = glob.config.config["web_server"]["host"]
		glob.secret = glob.config.config["web_server"]["secret"]
	except (KeyError, ValueError):
		console.error()
		raise

	# Start Bottle in a separate thread
	threading.Thread(target=bottleWorker, args=(serverHost, serverPort,)).start()
	console.done()
	console.colored("Bottle listening for HTTP clients on :{}".format(serverPort), bcolors.GREEN)

	# Start discord bot in main thread
	console.printn("> Starting Discord Bot...")
	glob.client = discord.Client()
	from bot import main 
	glob.client.run(glob.config.config["discord"]["token"])
	