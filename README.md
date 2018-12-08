# easydata
A simple and lightweight database and graph library in python.

## Code

A schema is a type of object defined within a database. We will now create a schema for defining points in space.
    
    db = Database()
    db.create_schema('point', ['x', 'y'])

As you can see, a point is defined by 'x' and 'y' coordinates. Now we will create an object representing an instance of a point.

    db.create_object('point', 'p1', None, [5, 6])
    
The database now contains an object 'p1' equal to None, with 'x' and 'y' attributes equal to 5 and 6 respectively.

We can access the value of a particular object using the database like a dictionary.

    db['p1']
    >>> None

The individual attributes of an object are also accessible.

    db.get_attr('p1', 'x)
    >>> 5
    db.get_attr('p1', 'y')
    >>> 6

Alternatively, attributes may be accessed in the following way:

    db['p1', 'x']   # equivalent to db.get_attr('p1', 'x')
    >>> 5
    db['p1', 'y']   # equivalent to db.get_attr('p1', 'y')
    >>> 6

Every attribute of an object can be accessed together as well.
    
    db.get_attrs('p1')
    >>> {'x':5, 'y':6}
    
Objects may be extracted from a database, wherein the total set of info regarding a particular object is placed within a dictionary.

    db.extract_object('p1')
    >>> {'key': 'p1', 'value': None, 'type': 'point', 'attributes': {'x': 5, 'y':6}}
