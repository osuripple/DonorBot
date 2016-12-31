from constants import bcolors

def colored(string, color):
	print("{}{}{}".format(color, string, bcolors.ENDC))

def done(space=True):
	s = " " if space == True else ""
	s += "Done!"
	colored(s, bcolors.GREEN)

def error(space=True):
	s = " " if space == True else ""
	s += "Error!"
	colored(s, bcolors.RED)

def warning(space=True):
	s = " " if space == True else ""
	s += "Warning!"
	colored(s, bcolors.YELLOW)

def printn(s):
	print(s, end="")
