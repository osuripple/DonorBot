import time

class RateLimiterClient:
	def __init__(self, client_id, rate, per):
		"""
		Initialise a rate limiter for a single client

		:param rate: rate limit
		:param per: check rate
		"""
		self.rate = rate
		self.per = per
		self.allowance = self.rate  # requests
		self.lastCheck = time.time()

	def check(self, increase=True):
		"""
		Checks if this client is above the rate limit

		:param increase: if True, increase the requests number
		:return: True if the client is allowed,
				 False if the client has surpassed the rate limit
		"""
		current = time.time()
		time_passed = current - self.lastCheck
		if increase:
			self.lastCheck = current
		self.allowance += time_passed * (self.rate / self.per)
		if self.allowance > self.rate:
			self.allowance = self.rate # throttle
		if self.allowance < 1.0:
			return False
		else:
			if increase:
				self.allowance -= 1.0
			return True

class RateLimiter:
	def __init__(self, rate, per):
		"""
		Initialise a group of RateLimiterClient

		:param rate: rate limit
		:param per: check rate
		"""
		self.rate = rate
		self.per = per
		self.clients = {}

	def check(self, client_id, increase=True):
		"""
		Checks if a client is above the rate limit.
		If the client doesn't exist, a new RateLimiterClient object
		is created and added to clients dictionary.

		:param client_id: client identifier
		:param increase: if True, increase the requests number
		:return: True if the client is allowed,
				 False if the client has surpassed the rate limit
		"""
		if client_id not in self.clients:
			self.clients[client_id] = RateLimiterClient(client_id, self.rate, self.per)
		return self.clients[client_id].check(increase)