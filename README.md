# EasyData
A simple and lightweight database/graph library in python.

## Databases

__I. Schemas__

Databases are dictionaries with additional structure built on top. 

A database consists of schemas, objects, and attributes, which are all related symbolically. 

A schema defines a label and a set of attributes, and are used to create new objects. 

![Schema diagram](https://github.com/CarsonScott/easydata/blob/master/4927232E-8D0E-4211-9546-594CF7557A5B.jpeg)

We can define a schema to represent positions in 2D space:
    
    db = Database()
    db.create_schema('point', ['x', 'y'])
    
__II. Objects__

As you can see the schema labeled 'point' defines two attributes: 'x' and 'y'.

Objects created using the point schema are automatically assigned those attributes, and therefore require the same number of values to be defined when they are created. 

![Object diagram](https://github.com/CarsonScott/easydata/blob/master/D5C8A2F0-94B4-46C2-A9D7-BE7A3FE94563.jpeg)

We can create a new object using the point schema:

    db.create_object('point', 'p1', None, [5, 6])
    
The database now contains an object called 'p1', equal to None, which has attributes 'x' and 'y', equal to 5 and 6 respectively. 

The value of an object is stored in a database as a typical dictionary element:

    db['p1']
    >>> None
    
__III. Attributes__

The individual attributes of an object are accessible through methods:

    db.get_attr('p1', 'x)
    >>> 5
    
    db.get_attr('p1', 'y')
    >>> 6

Attributes are accessible using an alternative strategy:

    db['p1', 'x']   # equivalent to db.get_attr('p1', 'x')
    >>> 5
    
    db['p1', 'y']   # equivalent to db.get_attr('p1', 'y')
    >>> 6

Every attribute of an object is accessible as a dictionary:
    
    db.get_attrs('p1')
    >>> {'x':5, 'y':6}

Total information about a particular object is accessible by extracting a dictionary:

    db.extract_object('p1')
    >>> {'key': 'p1', 'value': None, 'type': 'point', 'attributes': {'x': 5, 'y':6}}

An extracted dictionary may be used to create a new object:

    p2 = db.extract_object('p1')
    p2['key'] = 'p2'
    p2['attributes']['x']=3
    p2['attributes']['y']=9
    db.insert_object(p2)

    db.get_attrs('p2')
    >>> {'x':3, 'y':9}

*** 

## Graphs

__I. Nodes__

Graphs are databases with a preset schema for defining links between objects. 

Graphs also come with a few additional methods for dealing with the link objects.

    graph = Graph()
    graph.create_schema('point', ['x', 'y'])
    graph.create_object('point', 'p1', None, [5, 6])
    graph.create_object('point', 'p2', None, [3, 9])

Every object in a graph is assigned two additional attributes:
    
    graph.get_attrs('p1')
    >>> {'x': 5, 'y': 6, 'sources': [], 'targets': [])

__II. Links__

Links are created using a 'source' and 'target' key, each pointing to an existing object:

    >>> graph.create_link('p1', 'p2')
    
Every link is assigned a generated key based on the source and target keys used to define it:
    
    graph.get_key('p1', 'p2')
    >>> '(p1 p2)'

The source and target objects' attributes are updated when a new link is created:

    graph.get_attrs('p1')
    >>> {'x': 5, 'y': 6, 'sources': [], 'targets': ['p2'])
   
    graph.get_attrs('p2')
    >>> {'x': 3, 'y': 9, 'sources': ['p1'], 'targets': [])
    
__III. Hierarchies__

Every link is an object that may be the source or target of another link. 

Links between links may be defined in an infinite hierarchy.

    graph.get_attrs(graph.get_key('p1', 'p2')) 
    >>> {'source': 'p1', 'target': 'p2', 'sources': [], 'targets': [])

***
