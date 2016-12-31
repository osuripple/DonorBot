import random
import string

def random_string(length = 8):
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def string_to_bool(s):
	return (s == "True" or s== "true" or s == "1" or s == 1)