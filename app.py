'Distribua sermões em datas semanais e pule dias reservados para outras atividades.'


def texto(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Use texto não vazio.")
    return value.strip()


def textos(items):
    if not isinstance(items, list):
        raise ValueError("Use uma lista de textos.")
    return [texto(item) for item in items]


def inteiro(value, minimo=0):
    if type(value) is not int or value < minimo:
        raise ValueError(f"Use um número inteiro a partir de {minimo}.")
    return value


from datetime import date, timedelta


def run(data):
    if not isinstance(data, dict):
        raise ValueError("A entrada deve ser um objeto JSON.")
    if not isinstance(data["mensagens"], list) or any(not isinstance(item, dict) for item in data["mensagens"]):
        raise ValueError("O campo mensagens deve ser uma lista de objetos.")
    atual = date.fromisoformat(texto(data["inicio"]))
    try:
        intervalo = timedelta(weeks=inteiro(data["intervalo_semanas"], 1))
    except OverflowError as exc:
        raise ValueError("O intervalo excede o limite do calendário.") from exc
    bloqueios = {date.fromisoformat(dia) for dia in textos(data["bloqueios"])}
    agenda = []
    def proxima(dia):
        try:
            return dia + intervalo
        except OverflowError as exc:
            raise ValueError("A agenda ultrapassa o limite de datas suportado.") from exc

    for indice, item in enumerate(data["mensagens"]):
        if indice:
            atual = proxima(atual)
        while atual in bloqueios:
            atual = proxima(atual)
        agenda.append({"data": atual.isoformat(), "titulo": texto(item["titulo"]),
                       "referencia": texto(item["referencia"])})
    return {"agenda": agenda, "ultima_data": agenda[-1]["data"] if agenda else None}


import argparse
import json
from pathlib import Path


def objeto_sem_campos_repetidos(pares):
    objeto = {}
    for chave, valor in pares:
        if chave in objeto:
            raise ValueError(f"Campo JSON repetido: {chave!r}.")
        objeto[chave] = valor
    return objeto


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", type=Path, help="Arquivo JSON com os dados")
    args = parser.parse_args()

    try:
        with args.entrada.open(encoding="utf-8-sig") as source:
            data = json.load(source, object_pairs_hook=objeto_sem_campos_repetidos)
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()

