from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
import requests

load_dotenv()

class Extract():
    def __init__(self):
        pass

    def extract_pnadc(self):
        url = "https://servicodados.ibge.gov.br/api/v3/agregados/4093/periodos/201201%7C201202-202602/variaveis/4099?localidades=N3[26]&classificacao=2[all]"

        resp = requests.get(url, timeout=60)
        if resp.status_code != 200 or "json" not in resp.headers.get("content-type", ""):
            raise RuntimeError(
                f"API do IBGE não retornou JSON (HTTP {resp.status_code}, "
                f"content-type={resp.headers.get('content-type')}). "
                "A API pode estar indisponível ou bloqueando requisições; tente novamente mais tarde."
            )
        data = resp.json()

        return data

    
    def extract_collection_from_mongo(self, db_name, collection_name):
            mongo_uri = os.getenv("MONGO_URI")
            client = MongoClient(mongo_uri, server_api=ServerApi('1'))

            db = client[db_name]
            data = db[collection_name]

            # Mais recente primeiro: cada execução do pipeline insere um novo
            # documento na camada bronze e o Transform usa data[0].
            data = list(data.find().sort("_id", -1))
            return data


