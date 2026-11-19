"""Gera as 17 configurações: meia fração 2^(5-1) com I = -ABCDE (resolução V) + a completa.

A fração contém a base (nenhum controle) e as cinco "sem Cx". Ver protocolo, seção 1.2.
"""
import itertools
import json
from pathlib import Path

CTL = ["C1", "C2", "C3", "C4", "C5"]


def gerar() -> list[dict]:
    cfgs = []
    for niveis in itertools.product([-1, 1], repeat=5):
        prod = 1
        for x in niveis:
            prod *= x
        if prod == -1:  # I = -ABCDE
            cfgs.append(dict(zip(CTL, (x == 1 for x in niveis))))
    cfgs.append(dict.fromkeys(CTL, True))
    for c in cfgs:
        ativos = [k for k in CTL if c[k]]
        if len(ativos) == 0:
            c["nome"] = "base"
        elif len(ativos) == 5:
            c["nome"] = "completa"
        elif len(ativos) == 4:
            c["nome"] = "sem_" + next(k for k in CTL if not c[k])
        else:
            c["nome"] = "+".join(ativos)
        c["obrigatoria"] = len(ativos) in (0, 4, 5)
    return sorted(cfgs, key=lambda c: (not c["obrigatoria"], -sum(c[k] for k in CTL), c["nome"]))


# Classes com separação (piloto de 11/11/2026): o controle que, ligado, zera a classe.
SEPARACAO = {"A3": "C3", "A4": "C4", "A5": "C5"}


def gerar_extra() -> list[dict]:
    """Outra meia fração (protocolo 7.1): para cada classe com separação, as 8 configurações com Cs desligado e
    número ÍMPAR de controles ligados entre os outros 4 (1 ou 3). Junto com as 8 da fração principal (0, 2 ou 4),
    fecham o fatorial 2^4 completo nos outros controles, e as interações duplas deixam de ser confundidas.
    Cada configuração lista em "classes" as classes em que deve rodar (só os ataques dessas classes)."""
    por_nome = {}
    for classe, cs in SEPARACAO.items():
        outros = [k for k in CTL if k != cs]
        for n in (1, 3):
            for ativos in itertools.combinations(outros, n):
                nome = "+".join(ativos)
                c = por_nome.setdefault(nome, {**{k: k in ativos for k in CTL}, "nome": nome, "obrigatoria": False,
                                               "extra": True, "classes": []})
                c["classes"].append(classe)
    return sorted(por_nome.values(), key=lambda c: (sum(c[k] for k in CTL), c["nome"]))


if __name__ == "__main__":
    cfgs = gerar()
    Path(__file__).with_name("configuracoes.json").write_text(json.dumps(cfgs, indent=1, ensure_ascii=False))
    print(len(cfgs), "configurações;", sum(c["obrigatoria"] for c in cfgs), "obrigatórias")
    extra = gerar_extra()
    Path(__file__).with_name("configuracoes_extra.json").write_text(json.dumps(extra, indent=1, ensure_ascii=False))
    print(len(extra), "configurações extras;", sum(len(c["classes"]) for c in extra), "pares configuração×classe")
