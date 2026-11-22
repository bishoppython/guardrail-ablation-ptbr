# guardrail-ablation-ptbr

Reproduction package for the paper **"How much does each layer protect? A factorial ablation of guardrails in a
Portuguese-language LLM customer-service agent"** (manuscript under preparation for the *Journal of Information
Security and Applications*).

The experiment measures, through a fractional factorial ablation, how much each of five guardrails protects an
LLM customer-service assistant that operates in Brazilian Portuguese, retrieves documents and executes three tools
with financial effect, and what each guardrail costs in false blocking of legitimate requests, latency and money.

Everything runs on **synthetic data** in a sandboxed fictitious store ("Loja Fictícia"). No real customer data and
no human participants are involved.

> Code identifiers, comments and the test payloads are in Portuguese, because the system under test operates in
> Brazilian Portuguese. This README and the paper are in English.

## Contents

| Path | What it is |
|---|---|
| `loja/` | Synthetic store: 200 customers, 20 products, 600 orders, 50 knowledge-base documents (`dados.py`, seed 2027 → `base.json`), BM25 retrieval (`rag.py`), the three tools and the store policy (`ferramentas.py`), including **C5** (backend authorization) |
| `controles/` | **C1** input injection detector (Llama Prompt Guard 2 86M), **C2** datamarking of retrieved content, **C3** personal-data masking, **C4** output validation |
| `assistente.py` | The assistant pipeline with each control switchable on/off |
| `llm.py` | Backends: Ollama (local models), Anthropic API (commercial model, with a hard spending cap), and a **simulated** model for testing without a GPU |
| `veredito.py` | Deterministic verdicts; separates **unauthorized** from **unintended** actions |
| `juiz.py` | LLM judge for the residual verdicts, plus the blind annotation sheets used to validate it |
| `executar.py` | Runs configurations × cases × repetitions; resumable JSONL output |
| `adaptativo.py` | Adaptive black-box attacker (LLM-guided mutation search, 20 attempts per objective) |
| `analisar.py`, `figuras.py`, `fig1_arquitetura.py` | Statistical analysis (RQ1–RQ4) and the paper's figures |
| `gerar_configuracoes.py` | The 2^(5−1) design (`configuracoes.json`, 17 configurations) and the complementary half fraction (`configuracoes_extra.json`) |
| `cargas/` | Test payloads: 300 legitimate requests, 300 static attacks, 100 adaptive objectives, the C1 calibration set (disjoint), and their schema (`LEIA-ME.md`) |
| `rodada*.sh`, `retomar.sh`, `parar.sh` | The exact sequence of the main run, with safe stop/resume |
| `testes/` | Unit and pipeline tests |
| `saida/` | Raw outputs and analysis (added after the main run finishes) |

## Requirements

- Python 3.12; dependencies in `requirements.txt` (`pip install -r requirements.txt`).
- [Ollama](https://ollama.com) for the local models. The models and the digests used in the paper:

  | Role | Model | Ollama digest | Quantization |
  |---|---|---|---|
  | Target | `qwen3.5:9b` | `56671c2ab938` | Q4_K_M |
  | Target | `gemma4:12b` | `6114515d63c1` | Q4_K_M |
  | LLM judge | `gpt-oss:20b` | `f38aa0c53da5` | MXFP4 |
  | Adaptive attacker | `llama3.1:8b` | `46e0c10c039e` | Q4_K_M |

- Commercial target: `claude-haiku-5-5` through the Anthropic API. The key is read from `ANTHROPIC_API_KEY` or
  from `~/.config/anthropic/sbseg.key`; it is never stored in the repository. `config.json` sets a spending cap
  (`teto_usd`), enforced in code, and every call is logged in `saida/gasto_anthropic.json`.
- C1 uses [`meta-llama/Llama-Prompt-Guard-2-86M`](https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M),
  a gated model under the Llama 4 Community License. It is **not redistributed here**: request access on Hugging
  Face and log in (`huggingface-cli login`) before running C1. It runs on CPU (~57 ms per message).

## Quick check (no GPU, no API key)

```bash
python -m unittest discover -s testes -t .
python executar.py --modelo simulado --cargas cargas/exemplos.jsonl --configs todas --reps 1 --saida saida/teste_sim.jsonl
```

The simulated model exercises the whole pipeline (retrieval, tools, controls, verdicts) without any LLM. For the
simulated run, set `"c1": {"tipo": "heuristico"}` in `config.json` if you have not downloaded Prompt Guard 2.

## Reproducing the experiment

```bash
python -m loja.dados                 # synthetic store → loja/base.json (seed 2027)
python gerar_configuracoes.py        # design → configuracoes.json, configuracoes_extra.json
python cargas/finais.py              # final payloads (validated; exits with an error if any check fails)
python cargas/objetivos_adaptativos.py
./rodada.sh && ./rodada_pos.sh       # the main run, in the order used in the paper (days on a 6 GB GPU)
./rodada_refazer.sh                  # reruns the adaptive searches truncated by the original A5 rule (Section 4.7)
python analisar.py                   # everything in saida/ → saida/analise/relatorio.md + one CSV per table
python figuras.py --en saida/analise # the paper's figures (fig2–fig4, English labels)
```

`./parar.sh` stops the run safely and `./retomar.sh` resumes it; every script appends to its JSONL and skips what
is already done. The random seed is 2027 throughout.

## From outputs to the paper

| Paper | Output |
|---|---|
| Table 5 (LLM judge vs. blind human annotation) | `saida/analise/8_concordancia_juiz.csv`, from the `saida/anotacao_juiz_*.csv` sheets |
| Section 4.7, human review of the judge (adaptive runs and Haiku static runs) | `saida/analise/8b_concordancia_juiz_adaptativo.csv`, `8c_revisao_estatico.csv`, from `saida/revisao_humana_*.csv` (blind sheets made by `planilha_adaptativo.py`) |
| Table 6 (attack success, base vs. full) | `saida/analise/1_sucesso_ataque.csv` |
| Fig. 2, RQ1 (removing each control) | `saida/analise/2_qp1_mcnemar.csv` |
| RQ2 (pairwise interactions) | `saida/analise/3_qp2_regressao.csv` |
| H1 (unauthorized vs. unintended actions) | `saida/analise/1b_h1_acoes.csv` |
| Fig. 3 and Table 7, RQ3 (false blocking, utility, latency, cost) | `saida/analise/4_qp3_legitimas.csv`, `4b_qp3_utilidade_por_tipo.csv`, `4c_custo_latencia.csv` |
| Trigger vocabulary (exploratory) | `saida/analise/6_gatilho.csv`, `6b_gatilho_formula.csv` |
| Fig. 4, Table 8, RQ4 and H2 (adaptive attacks) | `saida/analise/5_qp4_curva.csv`, `5b_qp4_final.csv`, `5c_h2_razao.csv`; judge-only sensitivity: `python analisar.py --sem-revisao --saida <dir>` |

The raw interaction logs (`saida/interacoes_*.jsonl`, `extra_*.jsonl`, `adaptativo_*.jsonl`) hold, per
interaction, the configuration, the case, the response, every tool call with its policy check, the retrieved
documents, the C1 score, tokens, latency and the verdict.

`saida/analise_estatica/` is an earlier snapshot of the same analysis taken before the adaptive phase finished
(static results only; identical to `saida/analise/` for those tables). The `*.truncados_regra_a5.jsonl` files keep
the 12 adaptive searches that stopped early under the first version of the A5 verdict rule (a legitimate refund
to the account holder counted as an attack success); they were re-run with the final rule (all 12 failed) and are
kept for audit only: `analisar.py` ignores them.

## Licences

- Code: MIT (`LICENSE`).
- Test payloads, synthetic data and outputs (`cargas/`, `loja/base.json`, `saida/`): CC BY 4.0 (`LICENSE-DATA`).
- Half of the static attacks instantiate, in Portuguese translation, the attack templates of
  [AgentDojo](https://github.com/ethz-spylab/agentdojo) (MIT licence; Debenedetti et al., NeurIPS 2024); those
  cases carry `"origem": "agentdojo:<template> (MIT)"`.

## Citation

Citation details will be added when the paper is published.
