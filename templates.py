import re


TEST_FORMAT = "'uieauie{for x, y, z in (1,2,3,4)}\\n body \\n{x} + {y}content {endfor}'"


class Template:
	LOOP_RE = re.compile(r""".*?(?P<begin>\{for) (?P<vars>[a-zA-Z_][\w,\s]*?) in (?P<opensquarebrackets>[\[])?(?P<openroundbrackets>[\(])?\s?(?P<iterable>[a-zA-Z_][\w\s]*?,?)*?(?(opensquarebrackets)[\]])(?(openroundbrackets)[\)])}(?P<body>.*?)(?P<end>{endfor}).*""", re.MULTILINE)


	def __init__(self, fmt, context=None, encoding="utf-8"):
		self.fmt = fmt
		if context is None:
			self.context = {}
		else:
			self.context = context
		self.encoding = encoding

	def render(self, extra_context={}):
		ctx = self.context
		if extra_context != {}:
			ctx.update(extra_context)
		return self.fmt.format(**ctx)

	def for_wsgi(self):
		return (bytes(line, self.encoding) for line in self.render())
