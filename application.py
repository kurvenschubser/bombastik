from bombastik import routes
from bombastik import caches
from bombastik import responses
from bombastik import utils


class Application:
	router = routes.get_router()


	def __call__(self, environ, start_response):
		response = self.process(environ)			
		status, headers, data = response.for_wsgi()
		start_response(status, headers)
		return data

	def process(self, environ):
		url = utils.reconstruct_url(environ)
		
		pathinfo = environ["PATH_INFO"]
		querystring = environ["QUERY_STRING"]
		protocol = environ["wsgi.url_scheme"]
		host = environ["HTTP_HOST"]
		agent = environ["HTTP_USER_AGENT"]
		cookie = environ.get("HTTP_COOKIE")
		request_method = environ["REQUEST_METHOD"]

		try:
			route = self.router.match(url)
			fn = route.get_response_fn(request_method.lower())
			response = fn(environ, *args, **kwargs)
		except routes.RouteNotFoundError as e:
			print(environ)
			response = responses.Response(404, {}, 
						{"error": str(e)})

		return response

