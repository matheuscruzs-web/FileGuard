# FileGuard — Monitor de Integridade de Arquivos

Projeto educacional de segurança defensiva desenvolvido em Python. Registra hashes SHA-256 dos arquivos de uma pasta e depois compara com o estado atual para detectar arquivos modificados, novos e excluídos.

## Requisitos
- Python 3.9 ou superior
- Não precisa instalar bibliotecas externas

## Como usar
Abra um terminal na pasta `FileGuard`.

1. Prepare os arquivos na pasta `arquivos_monitorados/`.
2. **Cadastro inicial (uma vez):** `python main.py cadastrar`
3. **Verificação:** `python main.py verificar`
4. Altere, adicione ou exclua um arquivo dentro de `arquivos_monitorados/` e execute novamente `python main.py verificar`.
5. Consulte `relatorio.json`, gerado a cada verificação.

No Windows, caso `python` não seja reconhecido, experimente `py`.

## Arquivos
- `main.py`: programa principal.
- `arquivos_monitorados/`: pasta de testes, incluindo subpastas.
- `hashes.json`: referência dos hashes iniciais, **criada pelo programa** e não sobrescrita nas verificações.
- `relatorio.json`: resumo da última verificação.
- `tests/test_fileguard.py`: testes automatizados.

## Importante
- Caso exista um `hashes.json` de experiências anteriores, **guarde uma cópia** antes de usar este projeto. O novo programa usa chaves relativas à pasta monitorada, como `teste.txt`.
- O comando `cadastrar` se recusa a sobrescrever uma referência existente. Para um novo cadastro, após investigar as diferenças e guardar a referência antiga em um local seguro, exclua manualmente o `hashes.json` e execute `cadastrar` novamente.
- O hash detecta diferenças, mas não prova ataque ou identifica o autor.
- Em um ambiente real, um invasor com acesso de escrita poderia alterar também o arquivo de referência. Guarde uma cópia da referência fora da máquina monitorada ou use proteção de integridade e acesso apropriada.
- O programa é um protótipo de laboratório: não vigia continuamente em tempo real e não substitui uma solução corporativa de FIM.
- Links simbólicos são ignorados para evitar seguir arquivos fora da pasta monitorada.

## Testes
Na raiz do projeto: `python -m unittest discover -s tests -v`.

## Evoluções possíveis
- Interface CLI com opções adicionais.
- Registro histórico de eventos.
- Testes para erros de leitura e arquivos em alteração.
- Agendamento de verificações.

## Licença
Projeto de estudo; adicione uma licença antes de reutilização pública.
