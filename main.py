from src.extract import Extract
from src.load import Load
from src.transform import Transform

extrator = Extract()
loader = Load()
transformer = Transform()

pnadc = extrator.extract_pnadc()
print("Dados extraídos da API do IBGE")

loader.load_mongo(pnadc, "IBGE", "PNADC")
print("Dados salvos na camada Bronze!")

pnadc = extrator.extract_collection_from_mongo("IBGE", "PNADC")
print("Extração da camada bronze efetuada com sucesso!")

df = transformer.transform_pnadc(pnadc)
print("Dados transformados com Sucesso!")

loader.load_sqlite(df)
print("Dados salvos na camada Silver Local!")

loader.load_neon(df, "pnadc")
print("Dados salvos na camada Silver Núvem!")