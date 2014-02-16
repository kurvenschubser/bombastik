import importlib
from wsgiref import simple_server
import argparse


def run(host, port, app):
	httpd = simple_server.make_server(host, port, app)
	print("Starting server on {}:{}, running '{}'.".format(
						host, port, app))
	httpd.serve_forever()


if __name__ == "__main__":
	import sys
	sys.path.insert(0, "/home/malte/dev/")

	parser = argparse.ArgumentParser(\
		description="Run a simple wsgiref development server.")
	parser.add_argument("host")
	parser.add_argument("port", type=int)
	parser.add_argument("app")

	ns = parser.parse_args()

	try:
		apppath = ns.app.split(".")
		mod = importlib.__import__(".".join(apppath[:-1]), globals(), 
						locals(), apppath[-1:])
		app = getattr(mod, apppath[-1])()
	except ImportError as e:
		print(e)
		raise

	run(ns.host, ns.port, app)

