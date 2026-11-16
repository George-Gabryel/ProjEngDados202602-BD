import pandas as pd

class Transform:
    def __init__(self):
        pass

    def transform_pnadc(self, data):
        serie = data[0]['resultados'][0]['series'][0]['serie']
        df = pd.DataFrame.from_dict(serie, orient='index', columns=['valor'])
        df.index.name= 'periodo'
        df = df.reset_index()

        # O IBGE usa "..." (dado não disponível), "-" e "X" como marcadores.
        # Eles viram NaN (ausente), não 0, para não registrar uma taxa falsa de 0%.
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
        df['ano'] = df['periodo'].str[:4]
        df['tri'] = df['periodo'].str[-2:].astype(int)
        df['periodo'] = pd.PeriodIndex(df['ano']+'Q'+df['tri'].astype(str), freq='Q')
        df['periodo'] = df['periodo'].dt.to_timestamp()
        return df
