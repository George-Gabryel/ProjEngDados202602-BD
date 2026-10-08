import json
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from sqlalchemy import create_engine
import os
import certifi
import sqlite3
import pandas as pd

load_dotenv()


class Load():

    def __init__(self):
        self.mongo_uri = os.getenv('MONGO_URI')
        self.access_neon = os.getenv('DATABASE_URL')
        self.client = MongoClient(self.mongo_uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
        self.engine = create_engine(self.access_neon)
        
    def load_json(self, nome_doc, data):
        with open(f"{nome_doc}.json", "w", encoding="utf-8") as f:
            json.dump(data, f)

    def load_mongo(self, data: list[dict], db_name: str, collection_name: str) -> None:

        collection = self.client[db_name][collection_name]

        if data:
            collection.insert_many(data)

        print(f"Dados inseridos com sucesso na coleção '{collection_name}'!")

    def load_sqlite(self,df: pd.DataFrame):
        conn = sqlite3.connect("ibge.db")
        df.to_sql("pnadc", conn, if_exists="replace", index=False)
        conn.close()

    def load_neon(self, df, nome_tabela):
        df.to_sql(nome_tabela, self.engine, if_exists="replace")
        self.engine.dispose()
        print(f"Dados salvos no Neon com sucesso na tabela'{nome_tabela}'!")

