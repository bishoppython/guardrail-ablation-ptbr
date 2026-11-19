"""C1 — detector de prompt injection na entrada do usuário.

`DetectorHeuristico` existe só para testes e para o modo simulado: NÃO é o C1 do artigo.
O C1 do artigo é um classificador pronto (`DetectorHF`), com limiar fixado na calibração.
"""
from __future__ import annotations

import re

RECUSA_C1 = ("Não consigo seguir com essa solicitação. Posso ajudar com pedidos, trocas, "
             "reembolsos e dúvidas sobre a loja.")

_GATILHOS = [r"ignor\w* (as |todas as )?(instru|regras|orienta)", r"prompt (de|do) sistema",
             r"system prompt", r"modo (desenvolvedor|dev|deus)", r"a partir de agora (você|vc) (é|será)",
             r"finja que (você|vc) (é|não)", r"esque[cç]a (suas|as) (regras|instru)", r"jailbreak"]


class DetectorHeuristico:
    nome = "heuristico-teste"

    def pontuar(self, texto: str) -> float:
        t = texto.lower()
        return 1.0 if any(re.search(p, t) for p in _GATILHOS) else 0.0


class DetectorHF:
    """Classificador da Hugging Face (padrão: meta-llama/Llama-Prompt-Guard-2-86M, mDeBERTa, multilíngue).

    Janela de 512 tokens: textos maiores são divididos em janelas e vale a MAIOR pontuação
    (recomendação do model card). O rótulo de ataque é lido de model.config.id2label.
    """

    def __init__(self, modelo: str, rotulo_ataque: str | None = None, dispositivo: str | None = None):
        import torch  # import tardio: só quem usa precisa instalar
        from transformers import AutoModelForSequenceClassification, AutoTokenizer
        self.nome, self.torch = modelo, torch
        self.tok = AutoTokenizer.from_pretrained(modelo)
        self.mod = AutoModelForSequenceClassification.from_pretrained(modelo).eval()
        self.disp = dispositivo or ("cuda" if torch.cuda.is_available() else "cpu")
        self.mod.to(self.disp)
        rotulos = {v.lower(): int(k) for k, v in self.mod.config.id2label.items()}
        self.idx = rotulos.get((rotulo_ataque or "").lower(),
                               rotulos.get("malicious", rotulos.get("label_1", max(rotulos.values()))))

    def pontuar(self, texto: str) -> float:
        ids = self.tok(texto, add_special_tokens=False)["input_ids"]
        janelas = [ids[i:i + 510] for i in range(0, max(len(ids), 1), 510)] or [[]]
        maior = 0.0
        with self.torch.no_grad():
            for j in janelas:
                ids_j = self.torch.tensor([[self.tok.cls_token_id, *j, self.tok.sep_token_id]], device=self.disp)
                ent = {"input_ids": ids_j, "attention_mask": self.torch.ones_like(ids_j)}
                prob = self.torch.softmax(self.mod(**ent).logits, dim=-1)[0, self.idx].item()
                maior = max(maior, prob)
        return maior


def bloqueia(detector, texto: str, limiar: float) -> tuple[bool, float]:
    p = detector.pontuar(texto)
    return p >= limiar, p
