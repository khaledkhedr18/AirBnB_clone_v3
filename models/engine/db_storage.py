#!/usr/bin/python3
"""
DBStorage class for interacting with the MySQL database.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models import amenity, city, place, review, state, user

# Dictionary mapping class names to their corresponding classes
CNC = {
    'Amenity': amenity.Amenity,
    'City': city.City,
    'Place': place.Place,
    'Review': review.Review,
    'State': state.State,
    'User': user.User
}


class DBStorage:
    """Interacts with the MySQL database."""

    def __init__(self):
        """Instantiate a DBStorage object."""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.environ.get('HBNB_MYSQL_USER'),
                os.environ.get('HBNB_MYSQL_PWD'),
                os.environ.get('HBNB_MYSQL_HOST'),
                os.environ.get('HBNB_MYSQL_DB')))
        if os.environ.get("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query the current database session.
        If a class is specified, filter objects by that class.
        """
        obj_dict = {}
        if cls is not None:
            a_query = self.__session.query(CNC[cls])
            for obj in a_query:
                obj_ref = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[obj_ref] = obj
            return obj_dict

        for c in CNC.values():
            a_query = self.__session.query(c)
            for obj in a_query:
                obj_ref = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[obj_ref] = obj
        return obj_dict

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def rollback_session(self):
        """Rollback a session in the event of an exception."""
        self.__session.rollback()

    def delete(self, obj=None):
        """Delete from the current database session if obj is not None."""
        if obj:
            self.__session.delete(obj)
            self.save()

    def delete_all(self):
        """Delete all stored objects (for testing purposes)."""
        for c in CNC.values():
            a_query = self.__session.query(c)
            all_objs = [obj for obj in a_query]
            while all_objs:
                to_delete = all_objs.pop(0)
                to_delete.delete()
        self.save()

    def reload(self):
        """Create all tables in the database & session from the engine."""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))

    def close(self):
        """Call remove() on the private session attribute."""
        self.__session.remove()

    def get(self, cls, id):
        """
        Retrieve one object based on class name and ID.
        Returns None if not found.
        """
        if cls and id:
            fetch = "{}.{}".format(cls, id)
            all_obj = self.all(cls)
            return all_obj.get(fetch)
        return None

    def count(self, cls=None):
        """
        Return the count of all objects in storage.
        If a class name is passed, return the count of objects of that class.
        """
        return len(self.all(cls))
