from urllib.parse import quote


def reconstruct_url(environ):
	url = environ['wsgi.url_scheme']+'://'
	url += environ.get("HTTP_HOST", environ['SERVER_NAME'])
	
	if not environ.get("HTTP_HOST"):
		if environ['wsgi.url_scheme'] == 'https':	
			if environ['SERVER_PORT'] != '443':
				url += ':' + environ['SERVER_PORT']
		else:
			if environ['SERVER_PORT'] != '80':
				url += ':' + environ['SERVER_PORT']

	url += quote(environ.get('SCRIPT_NAME', ''))
	url += quote(environ.get('PATH_INFO', ''))
	
	if environ.get('QUERY_STRING'):
		url += '?' + environ['QUERY_STRING']

	return url

