'Filtre registros locais de obras, alagamentos e bloqueios por data de validade.'


def texto(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Use texto não vazio.")
    return value.strip()


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


def run(data):
    if not isinstance(data, dict):
        raise ValueError("A entrada deve ser um objeto JSON.")
    ocorrencias = data["ocorrencias"]
    if not isinstance(ocorrencias, list) or any(not isinstance(item, dict) for item in ocorrencias):
        raise ValueError("O campo ocorrencias deve ser uma lista de objetos.")
    dia = date.fromisoformat(texto(data["data"]))
    minima = inteiro(data.get("gravidade_minima", 1), 1)
    if minima > 3:
        raise ValueError("A gravidade mínima deve estar entre 1 e 3.")
    ativas = []
    for item in ocorrencias:
        inicio = date.fromisoformat(texto(item["inicio"]))
        fim = date.fromisoformat(texto(item["fim"]))
        gravidade = inteiro(item["gravidade"], 1)
        if inicio > fim or gravidade > 3:
            raise ValueError("Use um período crescente e gravidade de 1 a 3.")
        if inicio <= dia <= fim and gravidade >= minima:
            local = texto(item["local"])
            ativas.append({"local": local, "tipo": texto(item["tipo"]), "gravidade": gravidade,
                           "google_maps": busca(local)})
    ativas.sort(key=lambda item: (-item["gravidade"], item["local"]))
    return {"ocorrencias": ativas, "ativas": len(ativas)}


import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", type=Path, help="Arquivo JSON com os dados")
    args = parser.parse_args()

    try:
        with args.entrada.open(encoding="utf-8") as source:
            data = json.load(source)
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
