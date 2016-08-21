import random
import string

def randomString(length = 8):
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def stringToBool(s):
	return (s == "True" or s== "true" or s == "1" or s == 1)