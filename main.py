"""FileGuard: monitor de integridade de arquivos para laboratório local."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
PASTA = BASE / "arquivos_monitorados"
REFERENCIA = BASE / "hashes.json"
RELATORIO = BASE / "relatorio.json"


def calcular_hash(caminho):
    sha = hashlib.sha256()
    with caminho.open("rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(65536), b""):
            sha.update(bloco)
    return sha.hexdigest()


def examinar_pasta():
    if not PASTA.is_dir():
        raise FileNotFoundError(f"Pasta não encontrada: {PASTA}")

    hashes = {}
    for item in sorted(PASTA.rglob("*")):
        if item.is_file() and not item.is_symlink():
            caminho_relativo = item.relative_to(PASTA).as_posix()
            hashes[caminho_relativo] = calcular_hash(item)
    return hashes


def salvar_json(caminho, dados):
    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
        arquivo.write("\n")


def carregar_referencia():
    if not REFERENCIA.exists():
        raise FileNotFoundError("Referência ausente. Execute primeiro: python main.py cadastrar")
    with REFERENCIA.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    if not isinstance(dados, dict) or not all(
        isinstance(k, str) and isinstance(v, str) and len(v) == 64
        and all(c in "0123456789abcdef" for c in v)
        for k, v in dados.items()
    ):
        raise ValueError("O hashes.json não contém um mapa válido de hashes SHA-256.")
    return dados


def cadastrar():
    if REFERENCIA.exists():
        print("Referência já existe. Cadastro cancelado para evitar sobrescrita.")
        print("Guarde uma cópia segura e remova hashes.json manualmente apenas se desejar criar uma nova referência.")
        return 2

    hashes = examinar_pasta()
    # 'x' cria apenas se o arquivo ainda não existir.
    with REFERENCIA.open("x", encoding="utf-8") as arquivo:
        json.dump(hashes, arquivo, ensure_ascii=False, indent=2)
        arquivo.write("\n")
    print(f"Referência criada com {len(hashes)} arquivo(s): {REFERENCIA.name}")
    return 0


def verificar():
    original = carregar_referencia()
    atual = examinar_pasta()

    antigos = set(original)
    presentes = set(atual)
    adicionados = sorted(presentes - antigos)
    removidos = sorted(antigos - presentes)
    modificados = sorted(nome for nome in (antigos & presentes) if original[nome] != atual[nome])
    intactos = sorted(nome for nome in (antigos & presentes) if original[nome] == atual[nome])

    print(f"Arquivos intactos: {len(intactos)}")
    for titulo, nomes in (("NOVO", adicionados), ("REMOVIDO", removidos), ("MODIFICADO", modificados)):
        for nome in nomes:
            print(f"[{titulo}] {nome}")

    relatorio = {
        "verificado_em_utc": datetime.now(timezone.utc).isoformat(),
        "intactos": intactos,
        "adicionados": adicionados,
        "removidos": removidos,
        "modificados": modificados,
    }
    salvar_json(RELATORIO, relatorio)
    print(f"Relatório salvo em {RELATORIO.name}")
    if adicionados or removidos or modificados:
        print("ALERTA: foram detectadas diferenças em relação à referência!")
        return 1
    print("Integridade preservada: nenhuma diferença detectada.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="FileGuard: verificação local de integridade SHA-256")
    parser.add_argument("acao", choices=["cadastrar", "verificar"], help="Operação desejada")
    args = parser.parse_args()

    try:
        if args.acao == "cadastrar":
            return cadastrar()
        return verificar()
    except (OSError, ValueError, json.JSONDecodeError) as erro:
        print(f"ERRO: {erro}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
