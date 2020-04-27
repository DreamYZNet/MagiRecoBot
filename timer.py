import time

time.perf_counter()


def time_function(func):
	def wrapper(*args, **kwargs):
		start = time.perf_counter()
		ret = func(*args, **kwargs)
		end = time.perf_counter()
		print('Function time: ' + str(end - start) + f' for \'{func.__name__}\'')
		return ret
	return wrapper


class Timer:
	def __enter__(self):
		self.start = time.perf_counter()

	def __exit__(self, *exc_info):
		end = time.perf_counter()
		print('Block time: ' + str(end - self.start))
