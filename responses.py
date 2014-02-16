import http.server
from bombastik import serializers

STATUS_CODES = http.server.BaseHTTPRequestHandler.responses


class Response:
	DEFAULT_MIMETYPE = ".txt"


	def __init__(self, status, headers, data, mimetype=None, 
						encoding="utf-8"):
		self._status = status
		self._headers = dict(headers)
		self._data = data
		self._mimetype = mimetype
		self._encoding = encoding
		self.serializer = None

	def __iter__(self):
		return iter((self._status, self._headers, self._data))

	def for_wsgi(self):
		self._headers["Content-Encoding"] = self._encoding
		content = self.serialize_data(self._data)
		return iter((
			"{} {}".format(self._status, 
					STATUS_CODES[self._status][0]),
			list(self._headers.items()),
			content))

	def serialize_data(self, data):
		if self.serializer is None:
			datatype = type(data)
			mimetype = self._mimetype
			if mimetype is None:
				mimetype = serializers \
					.DATATYPE_TO_MIMETYPE_MAP.get(
						datatype, 
						self.DEFAULT_MIMETYPE)
			self._headers["Content-Type"] = \
				serializers.MIMETYPE_TO_CONTENTTYPE_MAP[
							mimetype]
			self.serializer = serializers \
				.get_serializer_for_type(datatype)

		return self.serializer(data)

