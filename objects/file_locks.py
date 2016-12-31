import threading

class FileLocks:
	def __init__(self):
		# Dictionary containing threading.Lock s
		self.locks = {}

	def lock(self, file_name):
		if file_name in self.locks:
			# Acquire existing lock
			self.locks[file_name].acquire()
		else:
			# Create new lock and acquire it
			self.locks[file_name] = threading.Lock()
			self.locks[file_name].acquire()

	def unlock(self, file_name):
		if file_name in self.locks:
			# Release lock if it exists
			self.locks[file_name].release()
