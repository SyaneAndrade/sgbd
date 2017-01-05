from ged import GED
from data_base import Data_Base
from table import Table
import os
import sys


# Função que limpa a tela pra ficar bonitinho
def clear():
    os.system("cls")


# Validação de campo, do tipo da tabela
def verifytype(type_field):
    if type_field == "INT" or type_field == "TEXT" or type_field == "DECIMAL":
        return True
    else:
        print("Entrada incorreta!!! Tente novamente")
        return False


# Função chamada para cria uma nova tabela de um banco de dados
def cria_table(Table):
    aux2 = True
    while aux2 is True:
        field = input("Entre com o nome do campo: ")
        aux = False
        while aux is False:
            type_field = input("Entre com o tipo do campo (INT, DECIMAL, TEXT): ")
            aux = verifytype(type_field)
        primary = 'A'
        while primary != "S" or primary != "N":
            primary = input("É primary key (S) or (N): ")
            if primary == "S":
                flag = True
                break
            elif primary == "N":
                flag = False
                break
            else:
                print("Entrada invalida")
        Table.create_field(field, type_field, flag)
        aux1 = None
        while True:
            aux1 = input("Deseja adcionar um novo campo? (S) or (N): ")
            if aux1 == "N":
                aux2 = False
                break
            elif aux1 == "S":
                break
            else:
                print("Entrada invalida!!!")


# Validação de dados inseridos nas row da tabela.
def verify_type_field(data, type_field):
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


# Para salvar as informações das tabelas
def cria_row(table):
    row = {}
    for key in table.field:
        while True:
            data = input("Entre com o valor para " + key + ": ")
            row[key] = verify_type_field(data, table.field[key])
            if (row[key] is not False):
                break
    key1 = table.key1
    for row2 in table.rows:
        if row[key1] == row2[key1]:
            input("Duplicidade de key não permitida. Tente novamente!!!\nPressione qualquer tecla para continuar...")
            return 0
    print(row)
    table.rows.append(row)


# Função para criar novo banco de dados
def criar_banco(ged):
    field = None
    tipo = None
    flag = None
    name = input("Entre com o nome do banco(sem espaços): ")
    size = input("Entre com o tamanho do banco: ")
    new_base = Data_Base(name, size)
    aux1 = False
    while aux1 is False:
        clear()
        print("Criando tabelas para o banco de dados: " + name)
        name_table = input("Entre com o nome da tabelas: ")
        table = Table(new_base, name_table)
        new_base.table.append(table)
        cria_table(table)
        aux = None
        while True:
            aux = input("Deseja adcionar uma nova tabela? (S) or (N): ")
            if aux == "N":
                aux1 = True
                break
            elif aux == "S":
                break
            else:
                print("Entrada invalida!!!")
    clear()
    print("Banco criado: " + new_base.name)
    for table in new_base.table:
        print(table.name)
        for key in table.field:
            print(key + ": " + table.field[key])
    print("Salvando no Catalogo do Sitema")
    input("Pressione qualquer tecla pra continuar....")
    ged.save_ims(new_base)


# Procura o banco no disco
def SelecionaBD(ged):
    while True:
        nome = input("Entre com o nome do banco procurado: ")
        bds = ged.loking_db(nome)
        for i in bds:
            if i.name == nome:
                return i
        print("Banco de dados não encontrado!")
        aux = input("Deseja tentar novamente?(S) or (N): ")
        if aux == "N":
            return None
            input("Aperte qualquer tecla pra continuar...")
            break


def Selecionatable(bd, ged):
    while True:
        clear()
        print("Menu para o banco de dados: " + bd.name)
        print("----------------------------------------")
        count = 0
        for i in range(0, len(bd.table)):
            print("({0}) - Adcionar informações para {1}".format(i, bd.table[i].name))
        aux = int(input("Opção: "))
        if aux < len(bd.table) and aux >= 0:
            cria_row(bd.table[aux])
            input("Aperte qualquer tecla para continuar...")
            break
        else:
            aux1 = input("Entrada invalida!!!\n Deseja tentar novamente? (S) ou (N): ")
            if aux1 == "N":
                break

# Menu
if __name__ == '__main__':
    ged = GED()
    aux = 0
    while True:
        clear()
        print("SGBD Simples by Denise")
        print("-----------------------------------------")
        print("(1) Criar novo Banco de dados")
        print("(2) Selecionar Banco de Dados")
        print("(0) Sair")

        aux = input("Opção: ")

        if aux == '1':
            clear()
            print("Criando Banco de Dados")
            criar_banco(ged)
            input("Pressione qualquer tecla pra continuar ...")
            clear()
        elif aux == '2':
            clear()
            bd = SelecionaBD(ged)
            if bd is not None:
                while True:
                    clear()
                    print("Menu para o banco de dados: " + bd.name)
                    print("----------------------------------------")
                    print("(1) - Listar todos os dados do banco")
                    print("(2) - Adcionar informação ao banco ")
                    print("(3) - Fazer consulta")
                    print("(4) - DROP DATA BASE")
                    print("(5) - Sair")
                    aux1 = input("Opção: ")
                    if aux1 == "1":
                        print("Ainda não implementado")
                    if aux1 == "2":
                        clear()
                        Selecionatable(bd, ged)
                    if aux1 == "3":
                        print("")
                    if aux1 == "4":
                        flag = False
                        while True:
                            aux = input("\nCerteza que deseja excluir o banco " + bd.name + " (S) ou (N): ")
                            if aux == 'S':
                                ged.drop_data_base(bd.name)
                                input("Exclusão sendo feita, aperte qualquer tecla pra continuar...")
                                flag = True
                                break
                            elif aux == 'N':
                                break
                        if flag:
                            break
                    if aux1 == "5":
                        for table in bd.table:
                            ged.save_disc(bd)
                        input("Saindo ...\n Pressione qualquer tecla pra continuar")
                        break
        elif aux == '0':
            print("Saindo...")
            break
        else:
            clear()
            print("Entrada invalida!!!")
            clear()
