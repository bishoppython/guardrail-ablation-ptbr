"""Backends de modelo. Todos expõem `conversar(mensagens, ferramentas) -> dict` no formato OpenAI
(content + tool_calls) e devolvem também tokens usados.

- "openai": qualquer endpoint compatível (Ollama em /v1, OmniRoute, API comercial). Chave lida de
  variável de ambiente (nunca de um .env versionado).
- "simulado": modelo de brinquedo, ingênuo de propósito (obedece instruções no contexto), para testar
  o encanamento e os vereditos sem gastar nada.
"""
from __future__ import annotations

import json
import os
import re
import urllib.request


class ModeloOpenAI:
    def __init__(self, url_base: str, modelo: str, chave_env: str | None = None, temperatura: float = 0.7,
                 timeout: int = 180):
        self.url = url_base.rstrip("/") + "/chat/completions"
        self.modelo, self.temperatura, self.timeout = modelo, temperatura, timeout
        self.chave = os.environ.get(chave_env, "") if chave_env else ""
        self.nome = modelo

    def conversar(self, mensagens: list[dict], ferramentas: list[dict]) -> dict:
        limpas = [{k: v for k, v in m.items() if not k.startswith("_")} for m in mensagens]
        corpo = {"model": self.modelo, "messages": limpas, "temperature": self.temperatura}
        if ferramentas:
            corpo["tools"] = ferramentas
        req = urllib.request.Request(self.url, data=json.dumps(corpo).encode(), method="POST",
                                     headers={"Content-Type": "application/json",
                                              **({"Authorization": f"Bearer {self.chave}"} if self.chave else {})})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            dados = json.loads(r.read())
        msg = dados["choices"][0]["message"]
        uso = dados.get("usage", {})
        return {"content": msg.get("content") or "", "tool_calls": msg.get("tool_calls") or [],
                "tokens_entrada": uso.get("prompt_tokens", 0), "tokens_saida": uso.get("completion_tokens", 0)}


class ModeloOllama:
    """API nativa do Ollama (/api/chat): permite desligar o raciocínio (think=False) e fixar a semente."""

    def __init__(self, url_base: str, modelo: str, temperatura: float = 0.7, think: bool = False,
                 num_ctx: int = 8192, timeout: int = 300, num_gpu: int | None = None,
                 num_predict: int | None = None):
        self.url = url_base.rstrip("/") + "/api/chat"
        self.num_gpu = num_gpu  # 0 = só CPU
        self.num_predict = num_predict  # teto de tokens gerados (o atacante, a temperatura 1,0, pode não parar)
        self.modelo, self.temperatura, self.think, self.num_ctx, self.timeout = modelo, temperatura, think, num_ctx, timeout
        self.nome = modelo

    @staticmethod
    def _nativo(m: dict) -> dict:
        if m.get("tool_calls"):
            return {"role": "assistant", "content": m.get("content", ""),
                    "tool_calls": [{"function": {"name": t["function"]["name"],
                                                 "arguments": json.loads(t["function"]["arguments"] or "{}")}}
                                   for t in m["tool_calls"]]}
        return {"role": m["role"], "content": m["content"]}

    def conversar(self, mensagens: list[dict], ferramentas: list[dict]) -> dict:
        corpo = {"model": self.modelo, "messages": [self._nativo(m) for m in mensagens], "stream": False,
                 "think": self.think, "options": {"temperature": self.temperatura, "num_ctx": self.num_ctx,
                             **({"num_gpu": self.num_gpu} if self.num_gpu is not None else {}),
                             **({"num_predict": self.num_predict} if self.num_predict else {})}}
        if ferramentas:
            corpo["tools"] = ferramentas
        req = urllib.request.Request(self.url, data=json.dumps(corpo).encode(), method="POST",
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            d = json.loads(r.read())
        msg = d["message"]
        chamadas = [{"id": f"t{i}", "type": "function",
                     "function": {"name": t["function"]["name"],
                                  "arguments": json.dumps(t["function"].get("arguments", {}), ensure_ascii=False)}}
                    for i, t in enumerate(msg.get("tool_calls") or [])]
        return {"content": msg.get("content") or "", "tool_calls": chamadas,
                "tokens_entrada": d.get("prompt_eval_count", 0), "tokens_saida": d.get("eval_count", 0)}


class OrcamentoEsgotado(RuntimeError):
    """Levantada ANTES de uma chamada que poderia ultrapassar o teto de gasto."""


class Livro:
    """Registro persistente do gasto na API (sobrevive a interrupções). Preços em US$ por milhão de tokens."""

    def __init__(self, caminho: str, teto_usd: float, preco_in: float, preco_out: float):
        self.caminho, self.teto, self.pin, self.pout = caminho, teto_usd, preco_in, preco_out
        self.dados = {"tokens_entrada": 0, "tokens_saida": 0, "chamadas": 0, "usd": 0.0}
        if os.path.exists(caminho):
            with open(caminho) as f:
                self.dados = json.load(f)

    def custo(self, tin: int, tout: int) -> float:
        return tin / 1e6 * self.pin + tout / 1e6 * self.pout

    def autorizar(self, tin_estimado: int, tout_maximo: int) -> None:
        pior = self.custo(tin_estimado, tout_maximo)
        if self.dados["usd"] + pior > self.teto:
            raise OrcamentoEsgotado(f"gasto US$ {self.dados['usd']:.4f} + pior caso US$ {pior:.4f} > teto US$ {self.teto}")

    def registrar(self, tin: int, tout: int) -> None:
        d = self.dados
        d["tokens_entrada"] += tin; d["tokens_saida"] += tout; d["chamadas"] += 1
        d["usd"] = round(self.custo(d["tokens_entrada"], d["tokens_saida"]), 6)
        tmp = self.caminho + ".tmp"
        with open(tmp, "w") as f:
            json.dump(d, f)
        os.replace(tmp, self.caminho)


class ModeloAnthropic:
    """Claude via SDK oficial (`anthropic`). Chave: ANTHROPIC_API_KEY ou um arquivo fora do repositório
    (padrão ~/.config/anthropic/sbseg.key, chmod 600). O conteúdo da chave nunca é impresso.

    Haiku 5.5 não aceita temperatura diferente da padrão: roda na amostragem do provedor, com
    raciocínio adaptativo (padrão do modelo) e esforço baixo; os blocos devolvidos (inclusive os de
    raciocínio) são reenviados sem alteração no laço de ferramentas, como a API exige.
    """

    def __init__(self, modelo: str, esforco: str = "low", max_tokens: int = 1500,
                 chave_arquivo: str = "~/.config/anthropic/sbseg.key", livro: "Livro | None" = None,
                 url_base: str | None = None):
        import anthropic  # import tardio: só quem usa precisa instalar
        # com url_base (ex.: OmniRoute, só para testar o código), a chave vem só do arquivo indicado
        chave = None if url_base else os.environ.get("ANTHROPIC_API_KEY")
        caminho = os.path.expanduser(chave_arquivo)
        if not chave and os.path.exists(caminho):
            with open(caminho) as f:
                chave = f.read().strip()
        kw = {"max_retries": 5, **({"base_url": url_base} if url_base else {})}
        self.cliente = anthropic.Anthropic(api_key=chave, **kw) if chave else anthropic.Anthropic(**kw)
        self.modelo, self.esforco, self.max_tokens, self.nome = modelo, esforco, max_tokens, modelo
        self._ferramentas: list[dict] = []
        self.livro = livro

    def _converter(self, mensagens: list[dict]):
        i, sistema = 0, []
        while i < len(mensagens) and mensagens[i]["role"] == "system":
            sistema.append(mensagens[i]["content"])
            i += 1
        saida: list[dict] = []
        for m in mensagens[i:]:
            if m["role"] == "tool":
                bloco = {"type": "tool_result", "tool_use_id": m["tool_call_id"], "content": m["content"]}
                if saida and saida[-1]["role"] == "user" and isinstance(saida[-1]["content"], list):
                    saida[-1]["content"].append(bloco)  # todos os resultados de um turno numa só mensagem
                else:
                    saida.append({"role": "user", "content": [bloco]})
            elif m["role"] == "assistant":
                saida.append({"role": "assistant", "content": m.get("_bruto") or m["content"]})
            else:  # user, ou system no meio da conversa (aceito pelo Haiku 5.5)
                saida.append({"role": m["role"], "content": m["content"]})
        return "\n\n".join(sistema), saida

    def conversar(self, mensagens: list[dict], ferramentas: list[dict]) -> dict:
        if ferramentas:
            self._ferramentas = [{"name": f["function"]["name"], "description": f["function"]["description"],
                                  "input_schema": f["function"]["parameters"]} for f in ferramentas]
        sistema, msgs = self._converter(mensagens)
        historico_com_ferramenta = any(m.get("tool_calls") for m in mensagens)
        extra = {"tools": self._ferramentas} if (ferramentas or historico_com_ferramenta) else {}
        if self.livro:  # pior caso: ~4 caracteres por token na entrada + max_tokens inteiro na saída
            tamanho = len(sistema) + len(json.dumps(self._ferramentas)) + sum(len(str(m.get("content"))) for m in msgs)
            self.livro.autorizar(tamanho // 3 + 500, self.max_tokens)
        r = self.cliente.messages.create(model=self.modelo, max_tokens=self.max_tokens, system=sistema,
                                         messages=msgs, **({"output_config": {"effort": self.esforco}} if self.esforco else {}), **extra)
        if self.livro:
            self.livro.registrar(r.usage.input_tokens, r.usage.output_tokens)
        texto = "".join(b.text for b in r.content if b.type == "text")
        chamadas = [{"id": b.id, "type": "function",
                     "function": {"name": b.name, "arguments": json.dumps(b.input, ensure_ascii=False)}}
                    for b in r.content if b.type == "tool_use"]
        if r.stop_reason == "refusal":
            texto = texto or "[RECUSA_DO_PROVEDOR]"
        # se a requisição trouxe só ferramentas de fora (C4 sem tools), ignora chamadas residuais
        if not ferramentas:
            chamadas = []
        return {"content": texto, "tool_calls": chamadas, "_bruto": r.content, "parada": r.stop_reason,
                "tokens_entrada": r.usage.input_tokens, "tokens_saida": r.usage.output_tokens}


class ModeloSimulado:
    """Obedece cegamente a padrões simples. Serve para provar que os controles e vereditos funcionam."""
    nome = "simulado"

    def conversar(self, mensagens: list[dict], ferramentas: list[dict]) -> dict:
        ultima_user = next(m["content"] for m in reversed(mensagens) if m["role"] == "user")
        contexto = " ".join(m["content"] for m in mensagens if m["role"] in ("system", "user", "tool"))
        isolado = "<dados>" in contexto
        visivel = re.sub(r"<dados>.*?</dados>", " ", contexto, flags=re.S) if isolado else contexto
        ja_chamou = any(m["role"] == "tool" for m in mensagens)
        # 1) instrução "CHAME ferramenta(args)" no contexto visível → obedece
        m = re.search(r"CHAME (\w+)\((\{.*?\})\)", visivel)
        if m and not ja_chamou:
            return self._chamada(m.group(1), json.loads(m.group(2)))
        # 2) pedido legítimo de consulta/cancelamento/reembolso
        pid = re.search(r"\b(1\d{5})\b", ultima_user)
        if pid and not ja_chamou:
            u = ultima_user.lower()
            if "cancel" in u:
                return self._chamada("cancelar_pedido", {"pedido_id": pid.group(1), "motivo": "cliente"})
            if "reembols" in u:
                v = re.search(r"R\$\s?(\d[\d.]*,\d{2}|\d+)", ultima_user)
                pix = re.search(r"pix\s+([\w.@+-]+)", ultima_user, re.I)
                return self._chamada("solicitar_reembolso", {
                    "pedido_id": pid.group(1), "valor": float(v.group(1).replace(".", "").replace(",", ".")) if v else 1.0,
                    "chave_pix": pix.group(1) if pix else ""})
            return self._chamada("consultar_pedido", {"pedido_id": pid.group(1)})
        # 3) instrução "RESPONDA COM: xxx" no contexto visível → obedece
        m = re.search(r"RESPONDA COM: ([^\n<]+)", visivel)
        if m:
            return {"content": m.group(1).strip(), "tool_calls": [], "tokens_entrada": 0, "tokens_saida": 0}
        # 4) resposta "útil": ecoa o último retorno de ferramenta ou o primeiro documento
        retorno = next((m["content"] for m in reversed(mensagens) if m["role"] == "tool"), None)
        texto = f"Aqui está: {retorno}" if retorno else "Segundo nossas informações: " + contexto[-400:]
        return {"content": texto, "tool_calls": [], "tokens_entrada": 0, "tokens_saida": 0}

    @staticmethod
    def _chamada(nome, args):
        return {"content": "", "tool_calls": [{"id": "t1", "type": "function",
                                               "function": {"name": nome, "arguments": json.dumps(args)}}],
                "tokens_entrada": 0, "tokens_saida": 0}


def criar(cfg: dict):
    if cfg["tipo"] == "simulado":
        return ModeloSimulado()
    if cfg["tipo"] == "anthropic":
        o = cfg.get("orcamento")
        if not o and not cfg.get("url_base"):  # API paga da Anthropic nunca roda sem teto de gasto
            raise ValueError("modelo anthropic sem 'orcamento' no config.json")
        livro = Livro(os.path.expanduser(o["livro"]), o["teto_usd"], o["preco_entrada"], o["preco_saida"]) if o else None
        return ModeloAnthropic(cfg["modelo"], cfg.get("esforco", "low"), cfg.get("max_tokens", 1500),
                               cfg.get("chave_arquivo", "~/.config/anthropic/sbseg.key"), livro, cfg.get("url_base"))
    if cfg["tipo"] == "ollama":
        return ModeloOllama(cfg["url_base"], cfg["modelo"], cfg.get("temperatura", 0.7), cfg.get("think", False),
                            cfg.get("num_ctx", 8192), cfg.get("timeout", 300), cfg.get("num_gpu"),
                            cfg.get("num_predict"))
    return ModeloOpenAI(cfg["url_base"], cfg["modelo"], cfg.get("chave_env"), cfg.get("temperatura", 0.7))
