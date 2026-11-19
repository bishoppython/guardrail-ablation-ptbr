"""C4 — validação determinística da resposta: preços, prazos e links contra as fontes."""
from __future__ import annotations

import re
from urllib.parse import urlparse

RESPOSTA_PADRAO_C4 = ("Não consegui confirmar essa informação com segurança. Vou encaminhar seu atendimento "
                      "para um atendente humano.")


def _num(brl: str) -> float:
    return round(float(brl.replace(".", "").replace(",", ".")), 2)


class Validador:
    def __init__(self, base: dict, cliente_id: str):
        self.dominio = base["dominio"]
        self.precos = {round(p["preco"], 2) for p in base["produtos"]}
        self.precos |= {round(p["valor_pago"], 2) for p in base["pedidos"] if p["cliente_id"] == cliente_id}
        self.precos |= {299.00}  # limite do frete grátis (POL-03)
        self.prazos = {5, 7, 10, 90}  # dias úteis, arrependimento, parcelas, garantia

    def falhas(self, resposta: str, valores_extra: set[float] = frozenset()) -> list[str]:
        f = []
        for m in re.finditer(r"R\$\s?(\d{1,3}(?:\.\d{3})*(?:,\d{2})?|\d+(?:,\d{2})?)", resposta):
            v = _num(m.group(1))
            if v not in self.precos and v not in valores_extra:
                f.append(f"preco_sem_fonte:{m.group(0)}")
        for m in re.finditer(r"\b(\d{1,3})\s+dias\b", resposta):
            if int(m.group(1)) not in self.prazos:
                f.append(f"prazo_sem_fonte:{m.group(0)}")
        # a URL termina em espaço, fecha-parêntese/colchete, "<", aspas, Markdown (* `) ou no "ˆ" do datamarking (C2)
        for m in re.finditer(r"https?://[^\s)>\]<ˆ*`\"'»]+|\bwww\.[^\s)>\]<ˆ*`\"'»]+", resposta):
            url = m.group(0).rstrip(".,;:!?")
            try:
                host = (urlparse(url if "://" in url else "http://" + url).hostname or "").rstrip(".")
            except ValueError:  # URL malformada (ex.: "[" no host): falha fechada, conta como não autorizada
                host = ""
            if not (host == self.dominio or host.endswith("." + self.dominio)):
                f.append(f"link_nao_autorizado:{url}")
        return f
