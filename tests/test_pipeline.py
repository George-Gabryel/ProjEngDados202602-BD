"""Testes do pipeline que não dependem de rede nem de banco.

Execute com:  python -m unittest discover -v
"""
import unittest

import pandas as pd

from src.load import normalizar_url_postgres
from src.transform import Transform


def _resposta_ibge(serie):
    """Monta um documento no formato retornado pela API do IBGE."""
    return [{
        "id": "4099",
        "resultados": [
            {
                "classificacoes": [{"id": "2", "nome": "Sexo", "categoria": {"6794": "Total"}}],
                "series": [{"localidade": {"id": "26", "nome": "Pernambuco"}, "serie": serie}],
            }
        ],
    }]


class TestTransformPnadc(unittest.TestCase):
    def setUp(self):
        self.df = Transform().transform_pnadc(
            _resposta_ibge({"201201": "9.6", "201202": "8.3", "202504": "...", "202602": "8.3"})
        )

    def test_colunas_e_tamanho(self):
        self.assertEqual(list(self.df.columns), ["periodo", "valor", "ano", "tri"])
        self.assertEqual(len(self.df), 4)

    def test_periodo_convertido_para_inicio_do_trimestre(self):
        self.assertEqual(
            list(self.df["periodo"]),
            [pd.Timestamp("2012-01-01"), pd.Timestamp("2012-04-01"),
             pd.Timestamp("2025-10-01"), pd.Timestamp("2026-04-01")],
        )
        self.assertEqual(list(self.df["tri"]), [1, 2, 4, 2])

    def test_valores_numericos_e_ausentes(self):
        self.assertTrue(pd.api.types.is_float_dtype(self.df["valor"]))
        self.assertEqual(list(self.df["valor"]), [9.6, 8.3, 0.0, 8.3])


class TestNormalizarUrlPostgres(unittest.TestCase):
    def test_postgresql_usa_psycopg2(self):
        url = normalizar_url_postgres("postgresql://u:p@host/db?sslmode=require")
        self.assertEqual(url, "postgresql+psycopg2://u:p@host/db?sslmode=require")

    def test_esquema_postgres_e_aceito(self):
        url = normalizar_url_postgres("postgres://u:p@host/db")
        self.assertEqual(url, "postgresql+psycopg2://u:p@host/db")

    def test_driver_explicito_e_mantido(self):
        url = normalizar_url_postgres("postgresql+psycopg://u:p@host/db")
        self.assertEqual(url, "postgresql+psycopg://u:p@host/db")

    def test_url_ausente_gera_erro_claro(self):
        with self.assertRaises(ValueError):
            normalizar_url_postgres(None)


if __name__ == "__main__":
    unittest.main()
