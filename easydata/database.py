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
	
	def create_object(self, schema, key, value=None, values=[]):
		self[key]=value
		attrs=self.schemas[schema]
		for i in range(len(attrs)):
			self.set_attr(key,attrs[i],values[i])
		self.instances[schema].append(key)

		for attr in self.get_attrs(key):
			value=self.get_attr(key, attr)
			constraints=self.constraints[schema][attr]
			if not all(constraint(value) for constraint in constraints):
				self.remove_object(key)
				return False
		return True

	def create_constraint(self, schema, key, proposition):
		self.constraints[schema][key].append(proposition)

	def extract_object(self, key):
		value=self[key]
		type=None
		for schema in self.schemas:
			if self.is_instance(key, schema):
				type=schema
				break
		attrs=self.get_attrs(key)
		object=Object({'key':key, 'value':value, 'type':type, 'attributes':dict()})
		for i in attrs:
			attr=attrs[i]
			if isinstance(attr, Reference):
				attr=self.extract_object(attr)
			object['attributes'][i]=attr
		return object
	
	def remove_object(self, key):
		del self[key]
		del self.attributes[key]
		for i in self.schemas:
			if self.is_instance(key, i):
				index=self.instances[i].index(key)
				del self.instances[i][index]
	
	def insert_object(self, object):
		if isinstance(object, Object):
			key=object['key']
			value=object['value']
			schema=object['type']
			attrs=object['attributes']
			values=[attrs[i] for i in self.schemas[schema]]
			if key in self:self.remove_object(key)
			for i in range(len(values)):
				if isinstance(values[i], Object):
					attr_key=values[i]['key']
					self.insert_object(values[i])
					values[i]=Reference(attr_key)
			self.create_object(schema, key, value, values)

	def set_attr(self, key, attr, value):self.attributes[key][attr]=value
	def get_attr(self, key, attr):return self.attributes[key][attr]
	def has_attr(self, key, attr):return attr in self.attributes[key]
	def get_attrs(self, key):return self.attributes[key]
	def get_instances(self, schema):return self.instances[schema]
	def is_instance(self, key, schema):return key in self.get_instances(schema)
	