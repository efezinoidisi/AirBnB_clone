#!/usr/bin/python3
"""
This is the file_storage module which contains the FileStorage class
"""
from json import load, dump
from importlib import import_module


class FileStorage:
    """
    This serializes instances to a JSON file and deserializes
    JSON file to instances

    Attributes:
          file_path (str): path to the JSON file
          objects (dict): stores all objects
    """

    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """
        returns the dictionary __objects which contains all objects
        with the key as <class name>.id
        """
        return self.__objects

    def new(self, obj):
        """
        sets in __objects the object with key:
        <obj class name>.id
        """
        key = f'{obj.__class__.__name__}.{obj.id}'
        self.__objects.update({key: obj})

    def save(self):
        """
        serializes __objects to the JSON file specified in __file_path
        """
        format_obj = {key: value.to_dict()
                      for key, value in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            dump(format_obj, f)

    def reload(self):
        """
        deserializes the JSON file to __objects only if the JSON
        file exists otherwise do nothing
        """
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                data = load(f)
                s = {'BaseModel': "base_model", 'User': "user",
                     'State': "state", 'City': "city",
                     'Amenity': "amenity", 'Place': "place",
                     'Review': "review"}
                for value in data.values():
                    cls_name = value['__class__']
                    mod = import_module(f'models.{s[cls_name]}')
                    Class = getattr(mod, cls_name)
                    self.new(Class(**value))

        except FileNotFoundError:
            pass
