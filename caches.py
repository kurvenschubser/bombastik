import abc
import functools


def default_cache(fn):
	return most_often_used()


class AbstractCache(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def get(self, key):
		return self.cache[key]
	
	@abc.abstractmethod
	def set(self, key, value):
		self.cache[key] = value


class MostOftenUsedCache(AbstractCache):
	def __init__(self, n_items=1024):
		self.cache = {}
		self.scores = {}
		self.n_items = n_items

	def get(self, key):
		values = self.cache[key]
		self.scores[key] = self.scores.get(key, 0) + 1

	def set(self, key, values):
		if len(self.cache) >= self.n_items:
			sorted_scores = sorted(self.scores.items(), 
						lambda o: o[1], True)
			popkey = sorted_scores[0][0]
			self.scores.pop(popkey)
			self.cache.pop(popkey)
		self.cache[key] = values

def most_often_used(n_items=1024):
	cache = MostOftenUsedCache(n_items)
	@functools.wraps(fn)
	def w(*args):
		try:
			return cache.get(args)
		except KeyError:
			cache.set(args, fn(*args))
		return cache.get(arg)
	return w


