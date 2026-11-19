"""Calibra o limiar do C1 no conjunto de calibração (separado das cargas de teste).

Critério (fixado ANTES de ver as notas): o limiar é o MENOR valor que mantém o bloqueio indevido
(FPR nas legítimas) <= 5%; entre os que cumprem, é o que maximiza a detecção. Reporta AUC, IC de Wilson
e a detecção por subtipo. Uso: .venv/bin/python calibrar_c1.py
"""
from __future__ import annotations

import csv
import json
import math
import sys
import time
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
FPR_MAX = 0.05


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - m), min(1.0, c + m))


def auc(pos: list[float], neg: list[float]) -> float:
    s = sum(1.0 if p > n else 0.5 if p == n else 0.0 for p in pos for n in neg)
    return s / (len(pos) * len(neg))


def _norm(t: str) -> str:
    t = unicodedata.normalize("NFKD", t.lower())
    return " ".join("".join(c for c in t if not unicodedata.combining(c)).split())


def verificar_disjuncao(cal: list[dict], arquivos_teste: list[Path]) -> list[str]:
    """Frases da calibração que aparecem (normalizadas) em alguma carga de teste."""
    calib = {_norm(c["texto"]) for c in cal}
    achados = []
    for arq in arquivos_teste:
        for linha in arq.read_text().splitlines():
            if linha.strip() and _norm(json.loads(linha)["mensagem"]) in calib:
                achados.append(f"{arq.name}: {json.loads(linha)['id']}")
    return achados


def main() -> None:
    sys.path.insert(0, str(RAIZ))
    from controles.c1_detector import DetectorHF
    cfg = json.loads((RAIZ / "config.json").read_text())["c1"]
    cal = [json.loads(l) for l in (RAIZ / "cargas" / "calibracao_c1.jsonl").read_text().splitlines() if l.strip()]
    testes = [p for p in (RAIZ / "cargas").glob("*.jsonl") if p.name != "calibracao_c1.jsonl"]
    sobrep = verificar_disjuncao(cal, testes)
    print("sobreposição com cargas de teste:", sobrep or "nenhuma")

    det = DetectorHF(cfg["modelo_hf"], cfg.get("rotulo_ataque"), cfg.get("dispositivo"))
    det.pontuar("aquecimento")
    tempos = []
    for c in cal:
        t = time.perf_counter()
        c["nota"] = det.pontuar(c["texto"])
        tempos.append((time.perf_counter() - t) * 1000)
    pos = [c["nota"] for c in cal if c["rotulo"] == 1]
    neg = [c["nota"] for c in cal if c["rotulo"] == 0]

    candidatos = sorted({0.5, *[c["nota"] for c in cal]})
    def taxa(lim):
        tp = sum(p >= lim for p in pos); fp = sum(n >= lim for n in neg)
        return tp, fp
    validos = [(lim, *taxa(lim)) for lim in candidatos if taxa(lim)[1] / len(neg) <= FPR_MAX]
    melhor = max(validos, key=lambda x: (x[1], -x[0]))  # maior detecção; empate → menor limiar
    # o limiar fica no meio do intervalo entre a nota escolhida e a nota imediatamente abaixo (evita colar num ponto)
    abaixo = max([n for n in candidatos if n < melhor[0]], default=0.0)
    limiar = round((melhor[0] + abaixo) / 2, 4)
    tp, fp = taxa(limiar)

    por_sub = {}
    for c in cal:
        s = por_sub.setdefault((c["rotulo"], c["subtipo"]), [0, 0])
        s[0] += c["nota"] >= limiar; s[1] += 1

    tempos.sort()
    rel = {
        "detector": det.nome, "dispositivo": det.disp, "criterio": f"menor limiar com FPR <= {FPR_MAX}",
        "limiar": limiar, "n_ataques": len(pos), "n_legitimas": len(neg),
        "deteccao": tp / len(pos), "deteccao_ic95": wilson(tp, len(pos)),
        "bloqueio_indevido": fp / len(neg), "bloqueio_indevido_ic95": wilson(fp, len(neg)),
        "auc": auc(pos, neg),
        "no_limiar_0_5": {"deteccao": taxa(0.5)[0] / len(pos), "bloqueio_indevido": taxa(0.5)[1] / len(neg)},
        "por_subtipo": {f"{'ataque' if r else 'legitima'}:{s}": f"{k}/{n}" for (r, s), (k, n) in sorted(por_sub.items())},
        "latencia_ms": {"mediana": tempos[len(tempos) // 2], "p95": tempos[int(len(tempos) * 0.95)]},
        "sobreposicao_com_testes": sobrep,
    }
    saida = RAIZ / "saida" / "calibracao_c1"
    saida.mkdir(parents=True, exist_ok=True)
    (saida / "resumo.json").write_text(json.dumps(rel, indent=1, ensure_ascii=False))
    with (saida / "notas.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "rotulo", "subtipo", "nota", "bloqueado", "texto"])
        for c in cal:
            w.writerow([c["id"], c["rotulo"], c["subtipo"], f"{c['nota']:.4f}", int(c["nota"] >= limiar), c["texto"]])
    print(json.dumps(rel, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
