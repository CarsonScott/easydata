from .database import *

class Graph(Database):

	def __init__(self):
		super().__init__()
		self.create_schema('link', ['source', 'target'])
	
	def create_object(self, schema, key, values=[], value=None):
		super().create_object(schema, key, values, value)
		self.set_attr(key, 'sources', [])
		self.set_attr(key, 'targets', [])
	
	def create_link(self, source, target, values=[], value=None):
		key=self.get_key(source, target)
		self[source, 'targets'].append(target)
		self[target, 'sources'].append(source)
		self.create_object('link', key, [Reference(source), Reference(target)]+values, value)
	
	def get_key(self, source, target):return '('+source+' '+target+')'
