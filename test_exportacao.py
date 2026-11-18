import json
from pathlib import Path
import shutil
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parent


@unittest.skipUnless(shutil.which("node"), "requer Node.js")
class ExportacaoTest(unittest.TestCase):
    def exportar(self, dados):
        return subprocess.run(
            ["node", ROOT / "exportar-agenda.mjs"], input=dados, capture_output=True,
        )

    def test_agenda_real_com_bloqueio(self):
        dados = subprocess.check_output([sys.executable, ROOT / "app.py", ROOT / "exemplo.json"])
        resultado = self.exportar(dados)
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn(b"DTSTART;VALUE=DATE:20261206\r\n", resultado.stdout)
        self.assertIn(b"DTSTART;VALUE=DATE:20261220\r\n", resultado.stdout)
        self.assertNotIn(b"20261213", resultado.stdout)
        def ids(saida):
            return [linha for linha in saida.replace(b"\r\n ", b"").splitlines()
                    if linha.startswith(b"UID:")]
        self.assertEqual(len(set(ids(resultado.stdout))), 2)
        self.assertEqual(ids(resultado.stdout), ids(self.exportar(dados).stdout))

    def test_texto_longo_e_quebras_nao_criam_propriedades(self):
        titulo = "João " * 30 + "A,B;C\\D\r\nEND:VEVENT"
        dados = {"agenda": [{"data": "2028-02-29", "titulo": titulo, "referencia": "João 15"}]}
        resultado = self.exportar(json.dumps(dados).encode())
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        linhas = resultado.stdout.split(b"\r\n")
        self.assertTrue(all(len(linha) <= 75 for linha in linhas))
        texto = resultado.stdout.decode()
        self.assertIn(r"A\,B\;C\\D\nEND:VEVENT", texto.replace("\r\n ", ""))
        self.assertEqual(linhas.count(b"END:VEVENT"), 1)

    def test_agenda_vazia_e_data_invalida(self):
        vazio = self.exportar(b'{"agenda":[]}')
        self.assertEqual(vazio.returncode, 0)
        self.assertNotIn(b"BEGIN:VEVENT", vazio.stdout)
        erro = self.exportar(b'{"agenda":[{"data":"2026-02-30","titulo":"A","referencia":"B"}]}')
        self.assertEqual(erro.returncode, 2)
        self.assertEqual(erro.stdout, b"")
