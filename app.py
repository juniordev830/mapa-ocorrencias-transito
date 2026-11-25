'Filtre registros locais de obras, alagamentos e bloqueios por data de validade.'


def texto(value, max_chars=300):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Use texto não vazio.")
    normalized = value.strip()
    if len(normalized) > max_chars:
        raise ValueError(f"Use texto com até {max_chars} caracteres.")
    if any(ord(char) < 32 or ord(char) == 127 for char in normalized):
        raise ValueError("O texto não pode conter caracteres de controle.")
    return normalized


def inteiro(value, minimo=0):
    if type(value) is not int or value < minimo:
        raise ValueError(f"Use um número inteiro a partir de {minimo}.")
    return value


from urllib.parse import urlencode


def _url(acao, parametros):
    url = "https://www.google.com/maps/" + acao + "?" + urlencode({"api": 1, **parametros})
    if len(url) > 2048:
        raise ValueError("O endereço gerado ultrapassa o limite do Google Maps.")
    return url


def busca(local):
    return _url("search/", {"query": texto(local)})


from datetime import date
import re


def data_iso(value):
    """Require a calendar-valid date in canonical YYYY-MM-DD form."""
    value = texto(value)
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        raise ValueError("Use datas no formato AAAA-MM-DD.")
    return date.fromisoformat(value)


def run(data):
    if not isinstance(data, dict):
        raise ValueError("A entrada deve ser um objeto JSON.")
    ocorrencias = data["ocorrencias"]
    if not isinstance(ocorrencias, list) or any(not isinstance(item, dict) for item in ocorrencias):
        raise ValueError("O campo ocorrencias deve ser uma lista de objetos.")
    dia = data_iso(data["data"])
    minima = inteiro(data.get("gravidade_minima", 1), 1)
    if minima > 3:
        raise ValueError("A gravidade mínima deve estar entre 1 e 3.")
    pesquisa = data.get("tipos")
    if pesquisa is not None and (not isinstance(pesquisa, list) or not pesquisa):
        raise ValueError("tipos deve ser uma lista não vazia de textos.")
    from unicodedata import normalize, combining
    def chave(value):
        return "".join(c for c in normalize("NFKD", texto(value).casefold()) if not combining(c))
    filtro = {chave(tipo) for tipo in pesquisa} if pesquisa is not None else None
    ativas = []
    for item in ocorrencias:
        inicio = data_iso(item["inicio"])
        fim = data_iso(item["fim"])
        gravidade = inteiro(item["gravidade"], 1)
        if inicio > fim or gravidade > 3:
            raise ValueError("Use um período crescente e gravidade de 1 a 3.")
        if inicio <= dia <= fim and gravidade >= minima:
            if filtro is not None and chave(item["tipo"]) not in filtro:
                continue
            local = texto(item["local"])
            ativas.append({"local": local, "tipo": texto(item["tipo"]), "gravidade": gravidade,
                           "google_maps": busca(local)})
    ativas.sort(key=lambda item: (-item["gravidade"], item["local"]))
    return {"ocorrencias": ativas, "ativas": len(ativas)}


import argparse
from contextlib import nullcontext
import sys
from relatorio_csv import escrever_csv
import json
from pathlib import Path

MAX_JSON_BYTES = 1_000_000


def objeto_sem_campos_repetidos(pares):
    objeto = {}
    for chave, valor in pares:
        if chave in objeto:
            raise ValueError(f"Campo JSON repetido: {chave!r}.")
        objeto[chave] = valor
    return objeto


def rejeitar_constante_json(constante):
    raise ValueError(f"Constante numérica inválida em JSON: {constante}.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", help="Arquivo JSON com os dados ou - para a entrada padrão")
    parser.add_argument("--csv", action="store_true", help="Exportar as ocorrências ativas por gravidade em CSV")
    args = parser.parse_args()

    try:
        entrada = nullcontext(sys.stdin.buffer) if args.entrada == "-" else Path(args.entrada).open("rb")
        with entrada as source:
            raw = source.read(MAX_JSON_BYTES + 1)
        if len(raw) > MAX_JSON_BYTES:
            raise ValueError("JSON excede o limite de 1 MB.")
        data = json.loads(
            raw,
            object_pairs_hook=objeto_sem_campos_repetidos,
            parse_constant=rejeitar_constante_json,
        )
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except RecursionError:
        parser.exit(2, "O JSON tem níveis de aninhamento demais.\n")
    except (KeyError, TypeError, ValueError, UnicodeError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    if args.csv:
        escrever_csv(result, sys.stdout)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
