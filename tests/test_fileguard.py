import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import main as fileguard


class FileGuardTests(unittest.TestCase):
    def test_calcular_hash_conteudo_conhecido(self):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / 'vazio.txt'
            arquivo.write_bytes(b'')
            self.assertEqual(fileguard.calcular_hash(arquivo),
                             'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')

    def test_cadastrar_e_verificar_alteracoes(self):
        with tempfile.TemporaryDirectory() as temp:
            raiz = Path(temp)
            monitorada = raiz / 'arquivos_monitorados'
            monitorada.mkdir()
            (monitorada / 'a.txt').write_text('original', encoding='utf-8')
            (monitorada / 'removido.txt').write_text('x', encoding='utf-8')
            with patch.object(fileguard, 'PASTA', monitorada), \
                 patch.object(fileguard, 'REFERENCIA', raiz / 'hashes.json'), \
                 patch.object(fileguard, 'RELATORIO', raiz / 'relatorio.json'):
                self.assertEqual(fileguard.cadastrar(), 0)
                self.assertEqual(fileguard.verificar(), 0)
                (monitorada / 'a.txt').write_text('alterado', encoding='utf-8')
                (monitorada / 'removido.txt').unlink()
                (monitorada / 'novo.txt').write_text('novo', encoding='utf-8')
                self.assertEqual(fileguard.verificar(), 1)
                import json
                dados = json.loads((raiz / 'relatorio.json').read_text(encoding='utf-8'))
                self.assertEqual(dados['modificados'], ['a.txt'])
                self.assertEqual(dados['adicionados'], ['novo.txt'])
                self.assertEqual(dados['removidos'], ['removido.txt'])
                self.assertEqual(fileguard.cadastrar(), 2)


if __name__ == '__main__':
    unittest.main()
