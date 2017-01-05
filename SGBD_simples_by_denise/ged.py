import os
import sys
from data_base import Data_Base
from table import Table


class GED(object):
    """Classe responsavel pelo gerenciamento de disco"""
    # http://187.7.106.14/marcelo/linguagemwebII/08_clienteservidor2/arquivosbinariosPython.pdf
    """docstring for GED"""
    def __init__(self):
        super(GED, self).__init__()
        self.count = 0
        self.full_size = 0
        self.list_size = []
        # Caminho do catalogo do sistema
        self.path_ims = 'arquivos/IMS.txt'
        # Caminho para disco
        self.path_disc = 'arquivos/disc.txt'

    # Metodo para abrir arquivos para leitura ou gravação
    def OpenFile(self, aux, path):
        try:
            if(aux == "read"):
                file = open(path, "rb")
            else:
                file = open(path, "wb")
        except IOError:
            print("Erro ao abrir arquivo " + path)
        return file

    # Salva dados informados pela criação de um novo  banco de dados como
    # suas tabelas, campos e tipos, inclusive a chave primaria
    """
        DATA_BASE_NAME banco_santander
        Size 1024
        |TABLE pessoa_fisica
        $nome TEXT
        $id INT
        $Primary_key id
        |TABLE conta
        $id_pessoa INT
        $digito_conta INT
        $numero_conta TEXT
        $Primary_key numero_conta
    """
    # modelo de dados salvos, considero splitar os bancos existentes pelos \n\n\n, as tabelas pelos |
    # e os campos das tabelas pelos $, isso no looking_db que retorna todos os bancos existentes
    def save_ims(self, data_base):
        # Salvando banco com suas tabelas no catalogo do sistema
        file = self.OpenFile("read", self.path_ims)
        file_disc = self.OpenFile("read", self.path_disc)
        mem = file.read()
        mem_disc = file_disc.read()
        file_disc.close()
        file.close()
        mem_disc = mem_disc.decode()
        file = self.OpenFile("write", self.path_ims)
        file_disc = self.OpenFile("write", self.path_disc)
        text_disc = mem_disc + "DATA_BASE_NAME " + data_base.name
        text = mem.decode() + "DATA_BASE_NAME " + data_base.name
        text = text + "\nSize " + data_base.size
        for table in data_base.table:
            text_disc = text_disc + "\n|TABLE " + table.name
            text = text + "\n" + "|TABLE " + table.name
            for key in table.field:
                text = text + "\n$" + key + " " + table.field[key]
            text = text + "\n$Primary_key" + " " + table.key1
        text = text + "\n\n\n"
        text_disc = text_disc + "\n\n\n"
        size_disc = file.tell()
        size = file.tell()
        file.seek(size, 2)
        file_disc.seek(size, 2)
        file.write(text.encode())
        file_disc.write(text_disc.encode())
        file.close()
        file_disc.close()
        file = self.OpenFile("read", self.path_ims)
        file_disc = self.OpenFile("read", self.path_disc)
        text_disc = file_disc.read()
        file.seek(0)
        text = file.read()
        print(text.decode())
    """
        Ideia para salvar no disco, assim que salvo no catalogo eu salvo o nome
        do banco e suas tabelas no disco
        banco separado por \n\n\n e tabelas separadas por |
        as rows serão separadas por $ e os campos por \n
        Sera do tipo
        DATA_BASE_NAME etc\n
        |TABLE etc1\n
        $field1 assas\n
        field2 heiehe\n
        $field1 asasa\n
        field2 heueheeu\n
        |TABLE etc2\n
        ...
        \n\n\n
    """
    def save_disc(self, bd):
        file = self.OpenFile("read", self.path_disc)
        text = file.read()
        file.close()
        text = text.decode().replace("\r", "")
        text = text.split("\n\n\n")
        mem = ""
        for i in text:
            if i != "":
                info = i.split("|")
                try:
                    name_db = info[0].split(" ")[1].replace("\n", "")
                except:
                    name_db = ""
                if bd.name != name_db:
                    mem = mem + "\n\n\n" + i
                    continue
                mem = mem + "\n\n\n" + info[0]
                temp_mem = ""
                for table in bd.table:
                    temp_mem = temp_mem + "|TABLE " + table.name + "\n"
                    for row in table.rows:
                        temp_mem = temp_mem +"$"
                        for key in row:
                            temp_mem = temp_mem + key + " " + str(row[key])+ "\n"
                mem = mem + temp_mem
        file = self.OpenFile("write", self.path_disc)
        file.write(mem.encode())
        file.close()

    def verify_type_field(self, data, type_field):
        if type_field == "INT":
            try:
                return int(data)
            except:
                return False
        elif type_field == "DECIMAL":
            try:
                return float(data.replace(",", "."))
            except:
                return False
        elif type_field == "TEXT":
            return data

    # Retorna as informações salvas no banco
    def loking_db_row(self, list_data_base):
        file = self.OpenFile("read", self.path_disc)
        text = file.read()
        file.close()
        text = text.decode()
        text = text.split("\n\n\n")
        for i in text:
            if i != "" and i != "\n":
                info = i.split("|")
                name_base = info[0].split(" ")[1].replace("\n", "")
                name_base = name_base.replace("\r", "")
                data_base = None
                for d in list_data_base:
                    if d.name == name_base:
                        data_base = d
                if data_base is None:
                    continue
                for a in range(1, len(info)):
                    b = info[a].split("$")
                    table_name = b[0].split(" ")[1].replace("\n", "")
                    table = None
                    for t in data_base.table:
                        if table_name == t.name:
                            table = t
                    if table is None:
                        continue
                    row = {}
                    for c in range(1, len(b)):
                        temp = b[c].split("\n")
                        for elem in temp:
                            if elem != "":
                                inf = elem.split(" ")
                                key = inf[0].replace("\n", "")
                                data = inf[1].replace("\n", " ")
                                row[key] = self.verify_type_field(data, table.field[key])
                                # inf = elem.split(" ")
                                # row[inf[0].replace("\n", "")] =  inf[1].replace("\n", " ")
                        table.rows.append(row.copy())

    def drop_disc(self, text, name_base):
        import pdb
        pdb.set_trace()
        temp = ""
        for i in text:
            if i != "":
                info = i.split("|")
                bd_name = info[0].split(" ")[1].replace("\n", "")
                bd_name = bd_name.replace("\r", "")
                if bd_name == name_base:
                    i = ""
                    temp = temp + i
                else:
                    temp = temp + "\n\n\n" + i
        return temp

    def drop_ims(self, text, name_base):
        temp = ""
        for i in text:
            if i != "" and i != "\n":
                info = i.split("|")
                mem = info[0].split("\n")
                dado = mem[0].split(" ")
                tam = mem[1].split(" ")
                if dado[1] == name_base:
                    i = ""
                    temp = temp
                else:
                    temp = temp + i +"\n\n\n"
        return temp

    def drop_data_base(self, name_base):
        file_disc = self.OpenFile("read", self.path_disc)
        file = self.OpenFile("read", self.path_ims)
        text = file_disc.read()
        text_ims = file.read()
        file.close()
        file_disc.close()
        text = text.decode()
        text_ims = text_ims.decode()
        text = text.replace("\r", "")
        text = text.split("\n\n\n")
        text_ims = text_ims.split("\n\n\n")
        text = self.drop_disc(text, name_base)
        text_ims = self.drop_ims(text_ims, name_base)
        file = self.OpenFile("write", self.path_ims)
        file_disc = self.OpenFile("write", self.path_disc)
        file.write(text_ims.encode())
        file_disc.write(text.encode())
        file.close()
        file_disc.close()


    # Retorna a lista de bancos existentes
    def loking_db(self, name):
        file = self.OpenFile("read", self.path_ims)
        text = file.read()
        text = text.decode()
        text = text.split("\n\n\n")
        data_bases = []
        for i in text:
            if i != "" and i != "\n":
                info = i.split("|")
                mem = info[0].split("\n")
                dado = mem[0].split(" ")
                tam = mem[1].split(" ")
                data_base = Data_Base(dado[1], tam[1])
            else:
                continue
            for j in range(1, len(info)):
                b = info[j].split("$")
                table = Table(data_base, b[0].split(" ")[1].replace("\n", ""))
                data_base.table.append(table)
                for a in range(1, len(b)):
                    if a != len(b)-1:
                        field = b[a].split(" ")
                        table.field[field[0]] = field[1].replace("\n", "")
                    else:
                        table.key1 = b[a].split(" ")[1].replace("\n", "")
            data_bases.append(data_base)
        file.close()
        self.loking_db_row(data_bases)
        return data_bases
