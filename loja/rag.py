"""Recuperação BM25 sem dependências (sem embedding, para não haver variável escondida)."""
from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter

PARADAS = set("a o as os de da do das dos e em no na nos nas um uma uns umas para por com que se meu minha "
              "eu voce você é ao à qual quais como ou".split())


def tokens(texto: str) -> list[str]:
    t = unicodedata.normalize("NFKD", texto.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return [w for w in re.findall(r"[a-z0-9]+", t) if w not in PARADAS]


class BM25:
    def __init__(self, documentos: list[dict], k1: float = 1.5, b: float = 0.75):
        self.docs = documentos
        self.k1, self.b = k1, b
        self.tf = [Counter(tokens(d["titulo"] + " " + d["texto"])) for d in documentos]
        self.len = [sum(c.values()) for c in self.tf]
        self.media = sum(self.len) / max(len(self.len), 1)
        df = Counter(w for c in self.tf for w in c)
        n = len(documentos)
        self.idf = {w: math.log(1 + (n - f + 0.5) / (f + 0.5)) for w, f in df.items()}

    def buscar(self, consulta: str, k: int = 4) -> list[dict]:
        q = tokens(consulta)
        notas = []
        for i, tf in enumerate(self.tf):
            s = 0.0
            for w in q:
                if w in tf:
                    f = tf[w]
                    s += self.idf[w] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.len[i] / self.media))
            notas.append((s, i))
        notas.sort(key=lambda x: (-x[0], x[1]))
        return [self.docs[i] for s, i in notas[:k] if s > 0]
