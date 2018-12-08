from .database import *

class Graph(Database):

	def __init__(self):
		super().__init__()
		self.create_schema('link', ['source', 'target'])
	
	def create_object(self, schema, key, value=None, values=[]):
		super().create_object(schema, key, value, values)
		self.set_attr(key, 'sources', [])
		self.set_attr(key, 'targets', [])
	
	def create_link(self, source, target, value=None):
		key=self.get_key(source, target)
		self[source, 'targets'].append(target)
		self[target, 'sources'].append(source)
		self.create_object('link', key, value, [Reference(source), Reference(target)])
	
	def get_key(self, source, target):return '('+source+' '+target+')'
