# EasyData

EasyData is a lightweight database library for handling complex graphical data seemlessly in python.

## Databases

__I. Schemas__

Databases are dictionaries with additional structure built on top. 

A database consists of schemas, objects, and attributes, which are all related symbolically. 

A schema defines a label and a set of attributes, and is used to create new objects. 

![Schema diagram](https://github.com/CarsonScott/easydata/blob/master/img/4927232E-8D0E-4211-9546-594CF7557A5B.jpeg)

We can define a schema to represent positions in 2D space:
    
    db = Database()
    db.create_schema('point', ['x', 'y'])
    
It's useful to have some control over the acceptible values that can be assigned to the attributes of a schema.
 
Constraints are proposition functions that are assigned with respect to a particular attribute of a given schema.

We can define constraints on the x and y attributes of the point schema defined above.

These constraints ensure that any value assigned to either x or y will be a non-negative integer.

    db.create_constraint('point', 'x', lambda val: isinstance(val, int) and val >= 0)
    db.create_constraint('point', 'y', lambda val: isinstance(val, int) and val >= 0)
    
If a value is given for a particular attribute while creating an object, which fails to satisfy the corresponding constraints of that attribute, then the object is never created. 

In other words, all constraints must be satisfied by a set of values in order to create an object from a given schema. 

__II. Objects__

As you can see the schema labeled 'point' defines two attributes: 'x' and 'y'.

Objects created using the point schema are automatically assigned those attributes, and therefore require the same number of values to be defined when they are created. 

![Object diagram](https://github.com/CarsonScott/easydata/blob/master/img/D5C8A2F0-94B4-46C2-A9D7-BE7A3FE94563.jpeg)

We can create a new object using the point schema:

    db.create_object('point', 'p1', 0, [5, 6])
    
The database now contains an object called 'p1', equal to 0, which has attributes 'x' and 'y', equal to 5 and 6 respectively. 

The value of an object is stored in a database as a typical dictionary element:

    db['p1']
    >>> 0
    
__III. Attributes__

The individual attributes of an object are accessible through methods:

    db.get_attr('p1', 'x)
    >>> 5
    
    db.get_attr('p1', 'y')
    >>> 6

The following shorthand is equivalent to the method above:

    db['p1', 'x']
    >>> 5
    
    db['p1', 'y']   
    >>> 6

Collectively, the attributes of an object are accessible as a dictionary:
    
    db.get_attrs('p1')
    >>> {'x':5, 'y':6}

Total information of a particular object is accessible by extracting a dictionary:

    db.extract_object('p1')
    >>> {'key': 'p1', 'value': 0, 'type': 'point', 'attributes': {'x': 5, 'y':6}}

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
    graph.create_object('point', 'p1', 0, [5, 6])
    graph.create_object('point', 'p2', 0, [3, 9])

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
