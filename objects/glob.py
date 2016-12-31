from objects import file_locks

config = None
client = None
db = None
f_locks = file_locks.FileLocks()
debug = False
secret = ""
rate_limiters = {}