#!/usr/bin/python3
"""
FileStorage class for interacting with the JSON file storage.
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Dictionary mapping class names to their corresponding classes
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """Interacts with the JSON file storage."""

    # Path to the JSON file
    __file_path = "file.json"
    # Dictionary to store objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of all objects in the storage.
        If a class is specified, filters objects by that class.
        """
        if cls is not None:
            filtered_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    filtered_dict[key] = value
            return filtered_dict
        return self.__objects

    def new(self, obj):
        """
        Sets an object in the __objects dictionary
        with a key composed of the object's class name and its id.
        """
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict(True)
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def get(self, cls, id):
        """
        Retrieves an object based on the class name and its ID.
        Returns None if not found.
        """
        if type(cls) is str:
            cls = classes.get(cls)
        if cls is None:
            return None
        for item in self.__objects.values():
            if item.__class__ == cls and item.id == id:
                return item

    def count(self, cls=None):
        """
        Counts the number of objects in storage matching the given class name.
        If no name is passed, returns the count of all objects in storage.
        """
        if type(cls) is str:
            cls = classes.get(cls)
        if cls is None:
            return len(self.all())
        return len(self.all(cls))

    def reload(self):
        """Deserializes the JSON file to __objects."""
        try:
            with open(self.__file_path, 'r') as f:
                json_data = json.load(f)
            for key in json_data:
                self.__objects[key] = classes[json_data[key]["__class__"]](**json_data[key])
        except:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects if it's inside."""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """Calls reload() method for deserializing the JSON file to objects."""
        self.reload()
