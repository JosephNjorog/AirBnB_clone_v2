#!/usr/bin/python3
"""
This module instantiates an object of class FileStorage/DBStorage
"""
import os

st_type = os.getenv('HBNB_TYPE_STORAGE')
if st_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
