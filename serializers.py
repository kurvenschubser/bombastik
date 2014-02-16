from http import server
import json

from bombastik import templates
from bombastik import settings

MIMETYPE_TO_CONTENTTYPE_MAP = server.SimpleHTTPRequestHandler.extensions_map

DATATYPE_TO_MIMETYPE_MAP = {
	dict: ".json",
	str: ".txt",
	list: ".json"
}

json_serializer = lambda d: (bytes(ln, settings.ENCODING) for ln in 
					json.dumps(d).split(settings.NEWLINE))
str_serializer = lambda d: (bytes(ln, settings.ENCODING) for ln in 
					str(d).split(settings.NEWLINE))
template_serializer = lambda t: (bytes(ln, settings.ENCODING) for ln in 
					t.render())
DATATYPE_TO_SERIALIZER_MAP = { 
	dict: json_serializer,
	list: json_serializer,
	tuple: json_serializer,
	set: json_serializer,
	str: str_serializer,
	templates.Template: template_serializer
}


def get_serializer_for_type(type_):
	return DATATYPE_TO_SERIALIZER_MAP[type_]


