import sys
import unittest
from pathlib import Path
from types import SimpleNamespace as NS

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from answer import SEM_BASE, responder
from search import Indice

EXCERTOS = [
    {"documento": "a.pdf", "pagina": 1, "texto": "As propinas são pagas em prestações até ao final do mês."},
    {"documento": "a.pdf", "pagina": 2, "texto": "A época de recurso destina-se aos estudantes reprovados."},
    {"documento": "b.pdf", "pagina": 7, "texto": "O estudante trabalhador tem regime especial de faltas."},
]


class ClienteFalso:
    def __init__(self, texto):
        self.texto, self.pedidos = texto, []
        self.messages = self

    def create(self, **pedido):
        self.pedidos.append(pedido)
        return NS(content=[NS(type="text", text=self.texto)], usage=NS(input_tokens=10, output_tokens=5))


class Testes(unittest.TestCase):
    def test_cita_a_fonte(self):
        cliente = ClienteFalso("Em prestações [1].")
        r = responder("Como se pagam as propinas?", Indice(EXCERTOS), cliente, minima=0)
        self.assertEqual([(f["documento"], f["pagina"]) for f in r["fontes"]], [("a.pdf", 1)])
        self.assertIn("propinas", cliente.pedidos[0]["messages"][0]["content"])

    def test_sem_excertos_nao_gasta_tokens(self):
        cliente = ClienteFalso("nunca usado")
        r = responder("xilofone azul", Indice(EXCERTOS), cliente)
        self.assertEqual(r["resposta"], SEM_BASE)
        self.assertEqual(cliente.pedidos, [])

    def test_fonte_nao_citada_fica_de_fora(self):
        r = responder("Como se pagam as propinas?", Indice(EXCERTOS), ClienteFalso(SEM_BASE), minima=0)
        self.assertEqual(r["fontes"], [])


if __name__ == "__main__":
    unittest.main()
