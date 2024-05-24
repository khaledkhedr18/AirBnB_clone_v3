#!/usr/bin/python3
"""
FileStorage class for handling I/O, writing, and reading of JSON data.
"""

import json
from models import base_model, amenity, city, place, review, state, user
from datetime import datetime

strptime = datetime.strptime
to_json = base_model.BaseModel.to_json


class FileStorage:
    """
    Handles long-term storage of all class instances using JSON format.
    """

    CNC = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }
    """CNC - Dictionary mapping class names to their corresponding classes."""

    __file_path = './dev/file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns the private attribute __objects.
        If a class is specified, filters objects by that class.
        """
        if cls is not None:
            filtered_objs = {}
            for clsid, obj in FileStorage.__objects.items():
                if type(obj).__name__ == cls:
                    filtered_objs[clsid] = obj
            return filtered_objs
        else:
            return FileStorage.__objects

    def new(self, obj):
        """
        Sets or updates the object in __objects with key <obj class name>.id.
        """
        bm_id = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[bm_id] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path).
        """
        fname = FileStorage.__file_path
        storage_d = {}
        for bm_id, bm_obj in FileStorage.__objects.items():
            storage_d[bm_id] = bm_obj.to_json(saving_file_storage=True)
        with open(fname, mode='w', encoding='utf-8') as f_io:
            json.dump(storage_d, f_io)

    def reload(self):
        """
        Deserializes the JSON file to __objects (if file exists).
        """
        fname = FileStorage.__file_path
        FileStorage.__objects = {}
        try:
            with open(fname, mode='r', encoding='utf-8') as f_io:
                new_objs = json.load(f_io)
        except:
            return
        for o_id, d in new_objs.items():
            k_cls = d['__class__']
            FileStorage.__objects[o_id] = FileStorage.CNCk_cls

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it's inside.
        """
        if obj:
            obj_ref = "{}.{}".format(type(obj).__name__, obj.id)
            all_class_objs = self.all(obj.__class__.__name__)
            if all_class_objs.get(obj_ref):
                del FileStorage.__objects[obj_ref]
            self.save()

    def delete_all(self):
        """
        Deletes all stored objects (for testing purposes).
        """
        try:
            with open(FileStorage.__file_path, mode='w') as f_io:
                pass
        except:
            pass
        del FileStorage.__objects
        FileStorage.__objects = {}
        self.save()

    def close(self):
        """
        Calls the reload() method for deserialization from JSON to objects.
        """
        self.reload()

    def get(self, cls, id):
        """
        Retrieves one object based on class name and ID.
        Returns None if not found.
        """
        if cls and id:
            fetch_obj = "{}.{}".format(cls, id)
            all_obj = self.all(cls)
            return all_obj.get(fetch_obj)
        return None

    def count(self, cls=None):
        """
        Returns the count of all objects in storage.
        If a class name is passed, returns the count of objects of that class.
        """
        return len(self.all(cls))
