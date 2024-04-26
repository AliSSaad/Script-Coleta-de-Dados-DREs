import DBAction
from dicionarioEmpresas import dicionarioEmpresas
import pyodbc
import json
import re
from requests_html import HTMLSession
import logging
import time

# Configura o nível de log para ERROR (ou superior) para exibir apenas mensagens de erro
logging.basicConfig(level=logging.ERROR)

# Informacoes do banco de dados
server = "ALI-DESKTOP\SQLEXPRESS"
database = "DBFundamentos"
# Criando a conexão com o banco de dados e criando a tabela caso ela não exista
db_conn = DBAction.DatabaseConnection(server, database)
connection = db_conn.connect()
db_create = DBAction.DataParser(connection)
db_create.create_table("cashflowstatement")
dicionario = dicionarioEmpresas()

for x, empresaTicker in enumerate(dicionario.empresas):
    empresaNome = dicionario.get_nome_empresa(empresaTicker.upper())
    #url = f"https://www.macrotrends.net/stocks/charts/{empresaTicker.upper()}/{empresaNome.lower()}/income-statement?freq=Q"
    #url = f"https://www.macrotrends.net/stocks/charts/{empresaTicker.upper()}/{empresaNome.lower()}/balance-sheet?freq=Q"
    url = f"https://www.macrotrends.net/stocks/charts/{empresaTicker.upper()}/{empresaNome.lower()}/cash-flow-statement?freq=Q"

    # Extraindo, processando e salvando os dados
    data = db_create.extract_data(url)
    db_create.parse_data(data, empresaTicker, "cashflowstatement")
    print(empresaTicker + " Salva com sucesso")
    time.sleep(10)
    #input("Pressione qualquer tecla")

