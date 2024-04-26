import re
from typing import Union, Any
import json
import pyodbc
import requests
from datetime import datetime
from requests_html import HTMLSession


class DatabaseConnection:
    def __init__(self, server, database):
        self.server = server
        self.database = database

    def connect(self):
        connection_string = f"DRIVER={{SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes; "
        conn = pyodbc.connect(connection_string)
        return conn


class DataParser:
    def __init__(self, connection):
        self.connection = connection

    def extract_data(self, url):
        session = HTMLSession()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        match = re.search("originalData = (.*);", response.text)
        session.close()
        return json.loads(match.group(1))

    def create_database(self, data_base_name):
        cursor = self.connection.cursor()
        cursor.execute(
            f"IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = {data_base_name})CREATE DATABASE {data_base_name}")
        cursor.commit()

    def create_table(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = ?) 
        CREATE TABLE {} (
            ID_Empresa NVARCHAR(255) NOT NULL,
            Data NVARCHAR(255) NOT NULL,
            PRIMARY KEY(ID_Empresa, Data)
        )
        """.format(table_name), (table_name,))
        cursor.commit()

    def add_column(self, table_name, column_name, column_type):
        cursor = self.connection.cursor()
        cursor.execute("""
        IF NOT EXISTS (
            SELECT * FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = ? AND COLUMN_NAME = ?
        ) 
        BEGIN
            ALTER TABLE {} ADD {} {}
        END
        """.format(table_name, column_name, column_type), (table_name, column_name))
        cursor.commit()

    def clean_column_name(self, column_name):
        return re.sub(r"[^\w]+", "_", column_name)

    def upsert_record(self, table_name, empresa_ticker, date, column_name, value):
        cursor = self.connection.cursor()

        check_sql = f"SELECT COUNT(*) FROM {table_name} WHERE ID_Empresa = ? AND Data = ?"
        cursor.execute(check_sql, (empresa_ticker, date))
        record_count = cursor.fetchone()[0]

        if record_count > 0:
            update_sql = f"UPDATE {table_name} SET {column_name} = ? WHERE ID_Empresa = ? AND Data = ?"
            cursor.execute(update_sql, (value, empresa_ticker, date))
        else:
            insert_sql = f"INSERT INTO {table_name} (ID_Empresa, Data, {column_name}) VALUES (?, ?, ?)"
            cursor.execute(insert_sql, (empresa_ticker, date, value))

        cursor.commit()

    def parse_data(self, data, empresa_ticker, table_name):
        for n, x in enumerate(data):
            des_match = re.search(">(.*?)<", x['field_name'])
            descricao = des_match.group(1)
            nome_coluna = self.clean_column_name(descricao)
            self.add_column(table_name, nome_coluna, "NVARCHAR(255)")
            del x['field_name']
            del x['popup_icon']

            for key, valor in x.items():
                try:
                    valor = float(valor)
                except ValueError:
                    pass

                date = datetime.strptime(key, "%Y-%m-%d").strftime("%Y-%m-%d")

                # Chame a função upsert_record
                self.upsert_record(table_name, empresa_ticker, date, nome_coluna, valor)
