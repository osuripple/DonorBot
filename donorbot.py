import discord
import os
import sys
import threading

from helpers import consoleHelper as console
from objects import glob
from objects import config
from constants import bcolors
from helpers import databaseHelper
import bottle
from gevent import monkey as brit_monkey
brit_monkey.patch_all()

from web import giveDonorHandler
from web import clearDonorHandler

def bottleWorker(host, port):
	bottle.run(host=host, port=port, server="gevent")

if __name__ == "__main__":
	# Create folders if needed
	console.printN("> Checking folders...")
	paths = [".data"]
	for i in paths:
		if not os.path.exists(i):
			os.makedirs(i, 0o770)
	console.done()

	# Load and check config.json
	console.printN("> Loading config file...")
	glob.config = config.config()
	if glob.config.status != config.configStatus.VALID:
		console.warning()

		if glob.config.status == config.configStatus.DOESNT_EXIST:
			console.colored("> The config file doesn't exist", bcolors.YELLOW)
		elif glob.config.status == config.configStatus.INVALID:
			console.colored("> The config file has an invalid structure", bcolors.YELLOW)
		elif glob.config.status == config.configStatus.INVALID_SYNTAX:
			console.colored("> Couldn't parse config.json", bcolors.YELLOW)
		else:
			console.colored("> Unknown error", bcolors.YELLOW)

		yn = input("> Do you want to generate a default config.json? (y/n): ")
		if yn == "y":
			console.printN("> Generating default config.json...")
			glob.config.writeDefault()
			console.done()
		sys.exit(0)
	console.done()

	# Connect to ripple database
	try:
		console.printN("> Connecting to ripple database")
		dbConfig = glob.config.config["database"]
		glob.db = databaseHelper.db(
			dbConfig["host"],
			dbConfig["username"],
			dbConfig["password"],
			dbConfig["database"],
		)
		console.done()
	except:
		console.error()
		raise

	# Start tornado
	console.printN("> Starting Bottle...")

	# Read port and secret
	try:
		serverPort = int(glob.config.config["web_server"]["port"])
		serverHost = glob.config.config["web_server"]["host"]
		glob.secret = glob.config.config["web_server"]["secret"]
	except:
		console.error()
		raise

	# Start Bottle in a separate thread
	threading.Thread(target=bottleWorker, args=(serverHost, serverPort,)).start()
	console.done()
	console.colored("Bottle listening for HTTP clients on :{}".format(serverPort), bcolors.GREEN)

	# Start discord bot in main thread
	console.printN("> Starting Discord Bot...")
	glob.client = discord.Client()
	from bot import main 
	glob.client.run(glob.config.config["discord"]["token"])
	