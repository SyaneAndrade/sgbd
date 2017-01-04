from data_base import *


class Table(object):
    """docstring for table"""
    def __init__(self, data_base, nome):
        self.data_base = data_base
        self.name = nome
        self.key1 = None
        self.field = {}
        self.rows = []

    def create_field(self, name, type_field, primary_key=False):
        if (primary_key):
            if(self.key1 is None):
                self.key1 = name
            else:
                print("Error! Primary key already exist!!!")
        self.field[name] = type_field
