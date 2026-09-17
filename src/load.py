import json
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import sqlite3
import pandas as pd


load_dotenv()


class Load():

    def __init__(self):
        self.mongo_uri = os.getenv('MONGO_URI')
        self.client = MongoClient(self.mongo_uri, server_api=ServerApi('1'),)

        
    def load_json(self, nome_doc, data):
        with open(f"{nome_doc}.json", "w", encoding="utf-8") as f:
            json.dump(data, f)

    def load_mongo(self, data: list[dict], db_name: str, collection_name: str) -> None:

        collection = self.client[db_name][collection_name]

        if data:
            collection.insert_many(data)

        print(f"Dados inseridos com sucesso na coleção '{collection_name}'!")

    def load_sqlite(self, data: pd.DataFrame, nome_tabela: str):
        df = pd.DataFrame(data)
        conn = sqlite3.connect("IBGE.db")
        df.to_sql(f"{nome_tabela}",con=conn, if_exists="replace", index=False)
        conn.close()

