#!/usr/bin/python3
"""
DBStorage class for interacting with the MySQL database.
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Dictionary mapping class names to their corresponding classes
classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """Interacts with the MySQL database."""

    def __init__(self):
        """Instantiate a DBStorage object."""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query the current database session.
        If a class is specified, filter objects by that class.
        """
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session if obj is not None."""
        if obj is not None:
            self.__session.delete(obj)

    def get(self, cls, id):
        """
        Retrieve one object based on the class name and its ID.
        Returns None if not found.
        """
        if type(cls) == str:
            cls = classes.get(cls)
        if cls is None:
            return None
        return self.__session.query(cls).filter(cls.id == id).first()

    def count(self, cls=None):
        """
        Count the number of objects in storage matching the given class name.
        If no name is passed, return the count of all objects in storage.
        """
        if type(cls) is str:
            cls = classes.get(cls)
        if cls is None:
            return len(self.all())
        return len(self.all(cls))

    def reload(self):
        """Reload data from the database."""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """Call remove() method on the private session attribute."""
        self.__session.remove()
