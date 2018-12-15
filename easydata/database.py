from .dict import *

class Database(Dict):

	def __init__(self):
		self.schemas=dict()
		self.attributes=dict()
		self.constraints=dict()
		self.instances=dict()
	
	def __setitem__(self, key, value):
		if isinstance(key, tuple):
			self.set_attr(*key, value)
		else:
			super().__setitem__(key,value)
			if key not in self.attributes:
				self.attributes[key]=dict()
	
	def __getitem__(self, key):
		if isinstance(key, tuple):
			return self.get_attr(*key)
		else:return super().__getitem__(key)

	def create_schema(self, schema, attrs=[]):
		self.schemas[schema]=attrs
		self.instances[schema]=list()
		self.constraints[schema]=dict()
		for i in attrs:self.constraints[schema][i]=[]
	
	def create_constraint(self, schema, key, proposition):
		self.constraints[schema][key].append(proposition)

	def create_object(self, schema, key, value=None, values=[], raise_exception=True):
		self[key]=value
		attrs=self.schemas[schema]
		for i in range(len(attrs)):
			self.set_attr(key,attrs[i],values[i])
		self.instances[schema].append(key)

		invalid_attrs=[]
		for attr in self.get_attrs(key):
			value=self.get_attr(key, attr)
			constraints=self.constraints[schema][attr]
			if not all(constraint(value) for constraint in constraints):
				invalid_attrs.append(attr)

		if len(invalid_attrs) > 0:
			self.remove_object(key)
			exception='Object "' + key + '" not created. '
			if len(invalid_attrs) == 1:
				exception += 'Attribute '
			else: exception += 'Attributes '

			for i in range(len(invalid_attrs)):
				attr=invalid_attrs[i]
				exception += '"' + attr + '"' 
				if i < len(invalid_attrs)-1:
					exception += ','
				exception += ' '
			exception += 'not satisfied.'
			raise Exception(exception)
	
	def remove_object(self, key):
		del self[key]
		del self.attributes[key]
		for i in self.schemas:
			if self.is_instance(key, i):
				index=self.instances[i].index(key)
				del self.instances[i][index]

	def set_attr(self, key, attr, value):self.attributes[key][attr]=value
	def get_attr(self, key, attr):return self.attributes[key][attr]
	def has_attr(self, key, attr):return attr in self.attributes[key]
	def get_attrs(self, key):return self.attributes[key]
	def get_instances(self, schema):return self.instances[schema]
	def is_instance(self, key, schema):return key in self.get_instances(schema)
	