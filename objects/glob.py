from objects import fileLocks

client = None
db = None
fLocks = fileLocks.fileLocks()
debug = False
secret = ""
rate_limiters = {}