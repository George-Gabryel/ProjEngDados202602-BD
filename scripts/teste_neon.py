import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, make_url

load_dotenv()

ACCESS_NEON = os.getenv("DATABASE_URL")
os.environ["DISABLE_SQLALCHEMY_CEXT"] = "1"

# SQLAlchemy 2.1 usa psycopg (v3) por padrão; o projeto instala psycopg2-binary
url = make_url(ACCESS_NEON)
if url.drivername in ("postgres", "postgresql"):
    url = url.set(drivername="postgresql+psycopg2")

engine = create_engine(url)

df = pd.DataFrame(
    {
        "periodo": ["2024Q1", "2024Q2"],
        "valor":[10.5,11.2],
    }
)

df.to_sql("teste_neon", engine, if_exists="replace")
print("Dados Salvos na tabela 'teste_neon'!")