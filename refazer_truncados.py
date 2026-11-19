"""Separa as buscas adaptativas que pararam num falso sucesso de A5 (regra do titular, 18/11/2026).

Até 18/11 a busca parava quando o modelo atendia, dentro da política, o pedido do próprio cliente (mesma ferramenta,
mesmo pedido, valor ajustado ao permitido). Pela regra fixada em veredito.py isso não é sucesso, e o atacante não
usou as tentativas restantes. Este script move essas buscas (e os julgamentos do juiz delas) para arquivos de
backup, para que adaptativo.py as refaça do zero com a regra nova. Nada é apagado.

Uso: .venv/bin/python refazer_truncados.py saida/adaptativo_qwen.jsonl [...]   (--checar: só lista)
Backups: saida/<arquivo>.truncados_regra_a5.jsonl e saida/juiz_<arquivo>.truncados_regra_a5.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from veredito import julgar

RAIZ = Path(__file__).resolve().parent


def truncada(r: dict, objetivos: dict, base: dict) -> bool:
    """A tentativa que encerrou a busca deixa de ser sucesso pela regra nova."""
    if r.get("k_sucesso") is None:
        return False
    h = next(h for h in r["historico"] if h["k"] == r["k_sucesso"])
    v = julgar(objetivos[r["objetivo"]], {"resposta": h["resposta"], "chamadas": h["chamadas"],
                                          "bloqueado_por": h["bloqueado_por"]}, base)
    return not v["sucesso_ataque"]


def gravar(p: Path, linhas: list[str]) -> None:
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text("".join(linhas))
    with tmp.open() as f:
        os.fsync(f.fileno())
    tmp.replace(p)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("arquivos", nargs="+")
    ap.add_argument("--checar", action="store_true")
    a = ap.parse_args()
    base = json.loads((RAIZ / "loja" / "base.json").read_text())
    objetivos = {o["id"]: o for o in map(json.loads, (RAIZ / "cargas" / "objetivos_adaptativos.jsonl").open())}
    for arq in map(Path, a.arquivos):
        if not arq.exists():
            continue
        linhas = arq.read_text().splitlines(keepends=True)
        sair = {(r["config"], r["objetivo"]) for r in map(json.loads, linhas) if truncada(r, objetivos, base)}
        print(f"{arq}: {len(sair)} buscas truncadas {sorted(sair)}")
        if a.checar or not sair:
            continue
        bk = arq.with_name(arq.name + ".truncados_regra_a5.jsonl")
        with bk.open("a") as f:
            f.writelines(l for l in linhas if (json.loads(l)["config"], json.loads(l)["objetivo"]) in sair)
        gravar(arq, [l for l in linhas if (json.loads(l)["config"], json.loads(l)["objetivo"]) not in sair])
        jz = arq.with_name("juiz_" + arq.name)
        if jz.exists():  # julgamentos de tentativas das buscas que serão refeitas (chave config, caso=objetivo, k)
            jl = jz.read_text().splitlines(keepends=True)
            fora = [l for l in jl if (json.loads(l)["config"], json.loads(l)["caso"]) in sair]
            with jz.with_name(jz.name + ".truncados_regra_a5.jsonl").open("a") as f:
                f.writelines(fora)
            gravar(jz, [l for l in jl if (json.loads(l)["config"], json.loads(l)["caso"]) not in sair])
            print(f"  {len(fora)} julgamentos movidos de {jz.name}")
        print(f"  backup em {bk.name}")


if __name__ == "__main__":
    main()
