"""C3 — mascaramento de dados pessoais de terceiros (antes do modelo e na saída).

Os dados do próprio titular da sessão não são mascarados; os de qualquer outro cliente sim.
"""
from __future__ import annotations

import re

PADROES = {
    "CPF": r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
    "EMAIL": r"\b[\w.+-]+@[\w-]+(\.[\w-]+)+\b",
    "TELEFONE": r"\(?\b\d{2}\)?\s?9?\d{4}-?\d{4}\b",
    "CEP": r"\b\d{5}-\d{3}\b",
    "CARTAO": r"\b(?:\d[ -]?){13,16}\b",
}


class Mascarador:
    def __init__(self, base: dict, cliente_id: str):
        titular = next(c for c in base["clientes"] if c["id"] == cliente_id)
        self.permitidos = {titular[k].lower() for k in ("cpf", "email", "telefone", "cep", "chave_pix", "nome", "endereco")}
        # nomes e endereços não têm padrão: usa a lista conhecida dos outros clientes
        self.literais = sorted({c[k] for c in base["clientes"] if c["id"] != cliente_id
                                for k in ("nome", "endereco")} - {titular["nome"], titular["endereco"]},
                               key=len, reverse=True)

    def mascarar(self, texto: str) -> tuple[str, int]:
        n = 0
        for lit in self.literais:
            if lit in texto:
                n += texto.count(lit)
                texto = texto.replace(lit, "[DADO_PESSOAL]")
        for rotulo, pad in PADROES.items():
            def troca(m, rotulo=rotulo):
                nonlocal n
                if m.group(0).lower() in self.permitidos:
                    return m.group(0)
                n += 1
                return f"[{rotulo}]"
            texto = re.sub(pad, troca, texto)
        return texto, n
