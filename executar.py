"""Roda configurações × casos × repetições e grava uma linha JSONL por interação (retomável).

Ex.: python executar.py --modelo simulado --cargas cargas/exemplos.jsonl --configs obrigatorias --reps 1
"""
from __future__ import annotations

import argparse
import json
import random
from dataclasses import asdict
from pathlib import Path

from assistente import Assistente
from controles.c1_detector import DetectorHeuristico, DetectorHF
from llm import OrcamentoEsgotado, criar
from veredito import julgar

RAIZ = Path(__file__).resolve().parent


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelo", required=True)
    ap.add_argument("--cargas", nargs="+", required=True)
    ap.add_argument("--configs", default="obrigatorias", help="obrigatorias | todas | extra | nomes separados por vírgula")
    ap.add_argument("--reps", type=int)
    ap.add_argument("--saida")
    a = ap.parse_args()

    cfg = json.loads((RAIZ / "config.json").read_text())
    base = json.loads((RAIZ / "loja" / "base.json").read_text())
    configs = json.loads((RAIZ / "configuracoes.json").read_text())
    if a.configs == "obrigatorias":
        configs = [c for c in configs if c["obrigatoria"]]
    elif a.configs == "extra":  # outra meia fração, só nas classes com separação (protocolo 7.1)
        configs = json.loads((RAIZ / "configuracoes_extra.json").read_text())
    elif a.configs != "todas":
        nomes = set(a.configs.split(","))
        configs = [c for c in configs if c["nome"] in nomes]
    casos = [json.loads(l) for f in a.cargas for l in Path(f).read_text().splitlines() if l.strip()]
    reps = a.reps or cfg["repeticoes"]
    c1 = cfg["c1"]
    detector = DetectorHF(c1["modelo_hf"], c1.get("rotulo_ataque"), c1.get("dispositivo")) if c1["tipo"] == "hf" else DetectorHeuristico()
    modelo = criar(cfg["modelos"][a.modelo])

    saida = Path(a.saida or RAIZ / "saida" / f"interacoes_{a.modelo}.jsonl")
    saida.parent.mkdir(exist_ok=True)
    feitos = set()
    if saida.exists():
        feitos = {(r["config"], r["caso"], r["rep"]) for r in map(json.loads, saida.read_text().splitlines())}

    ordem = [(c, k, r) for c in configs for k in casos for r in range(reps)
             if "classes" not in c or k.get("classe") in c["classes"]]
    random.Random(2027).shuffle(ordem)  # ordem aleatorizada e reprodutível
    with saida.open("a") as f:
        for i, (c, caso, rep) in enumerate(ordem, 1):
            if (c["nome"], caso["id"], rep) in feitos:
                continue
            ass = Assistente(base, modelo, c, detector, c1["limiar"], cfg["top_k"])
            try:
                res = asdict(ass.atender(caso["cliente_id"], caso["mensagem"], caso.get("docs_injetados")))
                erro = None
            except OrcamentoEsgotado as e:  # para limpo: nada é gravado para a interação incompleta
                print("PARADO POR ORÇAMENTO:", e)
                break
            except Exception as e:  # registra e segue; erro não é sucesso nem falha de ataque
                res, erro = None, f"{type(e).__name__}: {e}"
            ver = None
            if res:
                try:
                    ver = julgar(caso, res, base)
                except Exception as e:  # veredito quebrado não derruba a execução; a interação fica marcada
                    erro = f"veredito: {type(e).__name__}: {e}"
            linha = {"config": c["nome"], "controles": {k: c[k] for k in ("C1", "C2", "C3", "C4", "C5")},
                     "modelo": modelo.nome, "detector_c1": detector.nome, "caso": caso["id"], "rep": rep,
                     "carga": caso["carga"], "classe": caso.get("classe"), "gatilho": caso.get("gatilho"),
                     "erro": erro, "resultado": res, "veredito": ver}
            f.write(json.dumps(linha, ensure_ascii=False) + "\n")
            f.flush()
            if i % 50 == 0:
                print(f"{i}/{len(ordem)}")
    print("gravado em", saida)


if __name__ == "__main__":
    main()
