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


    #Pesquisa no banco
        #Recebe um dicionario que contem as seguintes coisas:
        '''
        query = {
            col: 'nome',
            operator: 'like',
            value: 'gui'
        }
        '''
    def search(self, query='All'):
        if (query == "All"):
            return self.rows
        else:
            results = []
            for row in self.rows:
                if (query['operator'] == '>'):
                    if(row[query['col']] > query['value']):
                        results.append(row)
                if (query['operator'] == '<'):
                    if(row[query['col']] < query['value']):
                        results.append(row)
                if (query['operator'] == '>='):
                    if(row[query['col']] >= query['value']):
                        results.append(row)
                if (query['operator'] == '<='):
                    if(row[query['col']] <= query['value']):
                        results.append(row)
                if (query['operator'] == '='):
                    if(row[query['col']] == query['value']):
                        results.append(row)
                if (query['operator'] == 'like'):
                    if(row[query['col']] == query['value']):
                        results.append(row)
                if (query['operator'] == 'percentLike'):
                    #substring
                    if(query['value'] in row[query['row']]):
                        results.append(row)
            return results
