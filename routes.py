import re
import functools


class RouteNotFoundError(Exception):
	pass


class Router:
	def __init__(self):
		self.routes = []
		self._cache = {}

	def match(self, url):
		try:
			return self._cache[url]
		except KeyError:
			for route in self.routes:
				if route.match(url):
					self._cache[url] = handler
					break
			else:
				raise RouteNotFoundError(url)

		return self._cache[url]

	def register(self, route_re, route_re_flags=0):
		route = re.compile(route_re, route_re_flags)			
		self.routes.append((route, callable_object()))


def get_router():
	global __ROUTER
	try:
		return __ROUTER
	except NameError:
		__ROUTER = Router()
	return __ROUTER

