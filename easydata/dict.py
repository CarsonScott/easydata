class Reference(str):pass
class Object(dict):pass

class Dict(dict):
	def keys(self):
		return list(super().keys())	
	def values(self):
		return list(super().values())
