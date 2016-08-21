import asyncio
from objects import glob

def syncCoroutine(coro):
	fut = asyncio.run_coroutine_threadsafe(coro, glob.client.loop)
	try:
		fut.result()
	except:
		pass
	return