import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from search import Indice, tokens


def dividir_sem_pdf():
    from importlib import import_module
    return import_module("ingest").dividir


EXCERTOS = [
    {"documento": "a.pdf", "pagina": 1, "texto": "As propinas são pagas em prestações até ao final do mês."},
    {"documento": "a.pdf", "pagina": 2, "texto": "A época de recurso destina-se aos estudantes reprovados."},
    {"documento": "b.pdf", "pagina": 7, "texto": "O estudante trabalhador pode faltar às aulas sem justificação."},
]


class Testes(unittest.TestCase):
    def test_acentos(self):
        self.assertEqual(tokens("Época de Recurso"), tokens("epoca recurso"))
        self.assertEqual(tokens("creditar"), tokens("creditação"))

    def test_encontra_excerto_e_fonte(self):
        _, melhor = Indice(EXCERTOS).pesquisar("Quando se pagam as propinas?")[0]
        self.assertEqual((melhor["documento"], melhor["pagina"]), ("a.pdf", 1))

    def test_sem_resultados(self):
        self.assertEqual(Indice(EXCERTOS).pesquisar("xilofone"), [])

    def test_dividir_sobrepoe(self):
        partes = dividir_sem_pdf()(" ".join(str(i) for i in range(200)), 120, 30)
        self.assertEqual(len(partes), 2)
        self.assertTrue(partes[1].startswith("90 "))


if __name__ == "__main__":
    unittest.main()
