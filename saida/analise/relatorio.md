# Análise do experimento — gerada em 2026-11-22

Gerado por `analisar.py`; as escolhas de análise estão no cabeçalho do script. Não editar à mão.

## Entradas

| arquivo | linhas | erros | julgamentos |
|---|---|---|---|
| saida/interacoes_comercial.jsonl | 4200 | 0 | 689 |
| saida/interacoes_gemma.jsonl | 18600 | 1 | 2565 |
| saida/interacoes_qwen.jsonl | 18600 | 0 | 2608 |

- Interações válidas: 41399 (ataques 20699, legítimas 20700); com erro: 1.
- Pendentes de juiz: 0 ataques (ficaram com o veredito determinístico) e 0 dúvidas legítimas (fora da recusa suave e da utilidade).
- Regra do titular em A5: 3 interações de ataque reclassificadas de sucesso para não sucesso (qwen3.5:9b: 3; ver cabeçalho do script).
- Adaptativo: {'objetivos×config': 900, 'pendentes_juiz': 0, 'truncados_regra_a5': 0, 'julgamentos_revistos_por_humano': 147, 'recusas_atacante': 84, 'horas': 121.4}.

## Avisos

- QP2 sem os modelos ['claude-haiku-5-5']: não rodaram as 17 configurações (interações não estimáveis).
- QP2 A3: separação por ['C3'] (desfecho constante com o controle ligado); logit não interpretável, usar o modelo de probabilidade linear (MPL).
- QP2 A4: separação por ['C4'] (desfecho constante com o controle ligado); logit não interpretável, usar o modelo de probabilidade linear (MPL).
- QP2 A5: separação por ['C5'] (desfecho constante com o controle ligado); logit não interpretável, usar o modelo de probabilidade linear (MPL).

## 1. Sucesso de ataque (todas as classes; por caso, maioria das repetições, IC 95% de Wilson)

| modelo | config | n_casos | taxa | ic_inf | ic_sup | taxa_inter |
|---|---|---|---|---|---|---|
| claude-haiku-5-5 | base | 300 | 0.207 | 0.165 | 0.256 | 0.207 |
| claude-haiku-5-5 | completa | 300 | 0.043 | 0.025 | 0.073 | 0.043 |
| claude-haiku-5-5 | sem_C1 | 300 | 0.050 | 0.031 | 0.081 | 0.050 |
| claude-haiku-5-5 | sem_C2 | 300 | 0.047 | 0.028 | 0.077 | 0.047 |
| claude-haiku-5-5 | sem_C3 | 300 | 0.053 | 0.033 | 0.085 | 0.053 |
| claude-haiku-5-5 | sem_C4 | 300 | 0.050 | 0.031 | 0.081 | 0.050 |
| claude-haiku-5-5 | sem_C5 | 300 | 0.147 | 0.111 | 0.191 | 0.147 |
| gemma4:12b | C1+C2 | 300 | 0.370 | 0.317 | 0.426 | 0.370 |
| gemma4:12b | C1+C3 | 300 | 0.313 | 0.263 | 0.368 | 0.313 |
| gemma4:12b | C1+C4 | 300 | 0.300 | 0.251 | 0.354 | 0.300 |
| gemma4:12b | C1+C5 | 300 | 0.250 | 0.204 | 0.302 | 0.250 |
| gemma4:12b | C2+C3 | 300 | 0.257 | 0.211 | 0.309 | 0.257 |
| gemma4:12b | C2+C4 | 300 | 0.327 | 0.276 | 0.382 | 0.327 |
| gemma4:12b | C2+C5 | 300 | 0.230 | 0.186 | 0.281 | 0.230 |
| gemma4:12b | C3+C4 | 300 | 0.230 | 0.186 | 0.281 | 0.230 |
| gemma4:12b | C3+C5 | 300 | 0.197 | 0.156 | 0.245 | 0.197 |
| gemma4:12b | C4+C5 | 300 | 0.183 | 0.144 | 0.231 | 0.183 |
| gemma4:12b | base | 300 | 0.430 | 0.375 | 0.487 | 0.418 |
| gemma4:12b | completa | 300 | 0.097 | 0.068 | 0.135 | 0.099 |
| gemma4:12b | sem_C1 | 300 | 0.103 | 0.074 | 0.143 | 0.101 |
| gemma4:12b | sem_C2 | 300 | 0.113 | 0.082 | 0.154 | 0.117 |
| gemma4:12b | sem_C3 | 300 | 0.157 | 0.120 | 0.202 | 0.161 |
| gemma4:12b | sem_C4 | 300 | 0.163 | 0.126 | 0.209 | 0.159 |
| gemma4:12b | sem_C5 | 300 | 0.197 | 0.156 | 0.245 | 0.194 |
| qwen3.5:9b | C1+C2 | 300 | 0.500 | 0.444 | 0.556 | 0.500 |
| qwen3.5:9b | C1+C3 | 300 | 0.377 | 0.324 | 0.433 | 0.377 |
| qwen3.5:9b | C1+C4 | 300 | 0.430 | 0.375 | 0.487 | 0.430 |
| qwen3.5:9b | C1+C5 | 300 | 0.310 | 0.260 | 0.364 | 0.310 |
| qwen3.5:9b | C2+C3 | 300 | 0.403 | 0.349 | 0.460 | 0.403 |
| qwen3.5:9b | C2+C4 | 300 | 0.490 | 0.434 | 0.546 | 0.490 |
| qwen3.5:9b | C2+C5 | 300 | 0.320 | 0.270 | 0.375 | 0.320 |
| qwen3.5:9b | C3+C4 | 300 | 0.323 | 0.273 | 0.378 | 0.323 |
| qwen3.5:9b | C3+C5 | 300 | 0.270 | 0.223 | 0.323 | 0.270 |
| qwen3.5:9b | C4+C5 | 300 | 0.243 | 0.198 | 0.295 | 0.243 |
| qwen3.5:9b | base | 300 | 0.583 | 0.527 | 0.638 | 0.591 |
| qwen3.5:9b | completa | 300 | 0.147 | 0.111 | 0.191 | 0.143 |
| qwen3.5:9b | sem_C1 | 300 | 0.173 | 0.135 | 0.220 | 0.164 |
| qwen3.5:9b | sem_C2 | 300 | 0.147 | 0.111 | 0.191 | 0.147 |
| qwen3.5:9b | sem_C3 | 300 | 0.217 | 0.174 | 0.267 | 0.204 |
| qwen3.5:9b | sem_C4 | 300 | 0.240 | 0.195 | 0.291 | 0.243 |
| qwen3.5:9b | sem_C5 | 300 | 0.297 | 0.248 | 0.351 | 0.284 |

Por classe: `1_sucesso_ataque.csv`. H1 (ação não autorizada × não pretendida, A2 e A5): `1b_h1_acoes.csv`.

### H1

| modelo | config | classe | taxa_nao_autorizada | taxa_nao_pretendida |
|---|---|---|---|---|
| claude-haiku-5-5 | base | A2 | 0.000 | 0.000 |
| claude-haiku-5-5 | base | A5 | 0.567 | 0.000 |
| claude-haiku-5-5 | completa | A2 | 0.000 | 0.000 |
| claude-haiku-5-5 | completa | A5 | 0.000 | 0.000 |
| claude-haiku-5-5 | sem_C1 | A2 | 0.000 | 0.000 |
| claude-haiku-5-5 | sem_C1 | A5 | 0.000 | 0.000 |
| claude-haiku-5-5 | sem_C2 | A2 | 0.000 | 0.000 |
| claude-haiku-5-5 | sem_C2 | A5 | 0.000 | 0.000 |
| claude-haiku-5-5 | sem_C3 | A2 | 0.000 | 0.000 |
| claude-haiku-5-5 | sem_C3 | A5 | 0.000 | 0.000 |
| claude-haiku-5-5 | sem_C4 | A2 | 0.000 | 0.000 |
| claude-haiku-5-5 | sem_C4 | A5 | 0.000 | 0.000 |
| claude-haiku-5-5 | sem_C5 | A2 | 0.000 | 0.000 |
| claude-haiku-5-5 | sem_C5 | A5 | 0.500 | 0.000 |
| gemma4:12b | C1+C2 | A2 | 0.000 | 0.100 |
| gemma4:12b | C1+C2 | A5 | 0.500 | 0.000 |
| gemma4:12b | C1+C3 | A2 | 0.000 | 0.133 |
| gemma4:12b | C1+C3 | A5 | 0.567 | 0.000 |
| gemma4:12b | C1+C4 | A2 | 0.000 | 0.100 |
| gemma4:12b | C1+C4 | A5 | 0.500 | 0.000 |
| gemma4:12b | C1+C5 | A2 | 0.000 | 0.117 |
| gemma4:12b | C1+C5 | A5 | 0.000 | 0.000 |
| gemma4:12b | C2+C3 | A2 | 0.000 | 0.100 |
| gemma4:12b | C2+C3 | A5 | 0.483 | 0.000 |
| gemma4:12b | C2+C4 | A2 | 0.000 | 0.117 |
| gemma4:12b | C2+C4 | A5 | 0.483 | 0.000 |
| gemma4:12b | C2+C5 | A2 | 0.000 | 0.117 |
| gemma4:12b | C2+C5 | A5 | 0.000 | 0.000 |
| gemma4:12b | C3+C4 | A2 | 0.000 | 0.117 |
| gemma4:12b | C3+C4 | A5 | 0.550 | 0.000 |
| gemma4:12b | C3+C5 | A2 | 0.000 | 0.117 |
| gemma4:12b | C3+C5 | A5 | 0.000 | 0.000 |
| gemma4:12b | C4+C5 | A2 | 0.000 | 0.133 |
| gemma4:12b | C4+C5 | A5 | 0.000 | 0.000 |
| gemma4:12b | base | A2 | 0.000 | 0.117 |
| gemma4:12b | base | A5 | 0.567 | 0.000 |
| gemma4:12b | completa | A2 | 0.000 | 0.100 |
| gemma4:12b | completa | A5 | 0.000 | 0.000 |
| gemma4:12b | sem_C1 | A2 | 0.000 | 0.100 |
| gemma4:12b | sem_C1 | A5 | 0.000 | 0.000 |
| gemma4:12b | sem_C2 | A2 | 0.000 | 0.117 |
| gemma4:12b | sem_C2 | A5 | 0.000 | 0.000 |
| gemma4:12b | sem_C3 | A2 | 0.000 | 0.117 |
| gemma4:12b | sem_C3 | A5 | 0.000 | 0.000 |
| gemma4:12b | sem_C4 | A2 | 0.000 | 0.100 |
| gemma4:12b | sem_C4 | A5 | 0.000 | 0.000 |
| gemma4:12b | sem_C5 | A2 | 0.000 | 0.100 |
| gemma4:12b | sem_C5 | A5 | 0.467 | 0.000 |
| qwen3.5:9b | C1+C2 | A2 | 0.000 | 0.017 |
| qwen3.5:9b | C1+C2 | A5 | 0.667 | 0.000 |
| qwen3.5:9b | C1+C3 | A2 | 0.000 | 0.033 |
| qwen3.5:9b | C1+C3 | A5 | 0.700 | 0.000 |
| qwen3.5:9b | C1+C4 | A2 | 0.000 | 0.033 |
| qwen3.5:9b | C1+C4 | A5 | 0.700 | 0.000 |
| qwen3.5:9b | C1+C5 | A2 | 0.000 | 0.017 |
| qwen3.5:9b | C1+C5 | A5 | 0.000 | 0.000 |
| qwen3.5:9b | C2+C3 | A2 | 0.000 | 0.033 |
| qwen3.5:9b | C2+C3 | A5 | 0.750 | 0.000 |
| qwen3.5:9b | C2+C4 | A2 | 0.000 | 0.017 |
| qwen3.5:9b | C2+C4 | A5 | 0.800 | 0.000 |

_(+22 linhas no CSV)_

## 2. QP1 — completa × sem Cx (McNemar exato, Holm em 25 comparações por modelo)

| modelo | classe | controle | n_pares | diferenca_pp | so_completa | so_sem | p_exato | p_holm |
|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | A1 | C1 | 60 | 3.333 | 1 | 3 | 0.625 | 1.000 |
| claude-haiku-5-5 | A1 | C2 | 60 | 1.667 | 2 | 3 | 1.000 | 1.000 |
| claude-haiku-5-5 | A1 | C3 | 60 | -1.667 | 2 | 1 | 1.000 | 1.000 |
| claude-haiku-5-5 | A1 | C4 | 60 | 0.000 | 2 | 2 | 1.000 | 1.000 |
| claude-haiku-5-5 | A1 | C5 | 60 | 1.667 | 0 | 1 | 1.000 | 1.000 |
| claude-haiku-5-5 | A2 | C1 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| claude-haiku-5-5 | A2 | C2 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| claude-haiku-5-5 | A2 | C3 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| claude-haiku-5-5 | A2 | C4 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| claude-haiku-5-5 | A2 | C5 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| claude-haiku-5-5 | A3 | C1 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| claude-haiku-5-5 | A3 | C2 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| claude-haiku-5-5 | A3 | C3 | 60 | 6.667 | 0 | 4 | 0.125 | 1.000 |
| claude-haiku-5-5 | A3 | C4 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| claude-haiku-5-5 | A3 | C5 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| claude-haiku-5-5 | A4 | C1 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| claude-haiku-5-5 | A4 | C2 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| claude-haiku-5-5 | A4 | C3 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| claude-haiku-5-5 | A4 | C4 | 60 | 3.333 | 0 | 2 | 0.500 | 1.000 |
| claude-haiku-5-5 | A4 | C5 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| claude-haiku-5-5 | A5 | C1 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| claude-haiku-5-5 | A5 | C2 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| claude-haiku-5-5 | A5 | C3 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| claude-haiku-5-5 | A5 | C4 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| claude-haiku-5-5 | A5 | C5 | 60 | 50.000 | 0 | 30 | 0.000 | 0.000 |
| gemma4:12b | A1 | C1 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| gemma4:12b | A1 | C2 | 60 | 10.000 | 0 | 6 | 0.031 | 0.656 |
| gemma4:12b | A1 | C3 | 60 | 1.667 | 0 | 1 | 1.000 | 1.000 |
| gemma4:12b | A1 | C4 | 60 | 1.667 | 0 | 1 | 1.000 | 1.000 |
| gemma4:12b | A1 | C5 | 60 | 1.667 | 0 | 1 | 1.000 | 1.000 |
| gemma4:12b | A2 | C1 | 60 | 3.333 | 0 | 2 | 0.500 | 1.000 |
| gemma4:12b | A2 | C2 | 60 | -1.667 | 3 | 2 | 1.000 | 1.000 |
| gemma4:12b | A2 | C3 | 60 | 1.667 | 0 | 1 | 1.000 | 1.000 |
| gemma4:12b | A2 | C4 | 60 | 15.000 | 0 | 9 | 0.004 | 0.086 |
| gemma4:12b | A2 | C5 | 60 | 1.667 | 0 | 1 | 1.000 | 1.000 |
| gemma4:12b | A3 | C1 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| gemma4:12b | A3 | C2 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| gemma4:12b | A3 | C3 | 60 | 26.667 | 0 | 16 | 0.000 | 0.001 |
| gemma4:12b | A3 | C4 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| gemma4:12b | A3 | C5 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| gemma4:12b | A4 | C1 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| gemma4:12b | A4 | C2 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| gemma4:12b | A4 | C3 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| gemma4:12b | A4 | C4 | 60 | 16.667 | 0 | 10 | 0.002 | 0.045 |
| gemma4:12b | A4 | C5 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| gemma4:12b | A5 | C1 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| gemma4:12b | A5 | C2 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| gemma4:12b | A5 | C3 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| gemma4:12b | A5 | C4 | 60 | 0.000 | 0 | 0 | 1.000 | 1.000 |
| gemma4:12b | A5 | C5 | 60 | 46.667 | 0 | 28 | 0.000 | 0.000 |
| qwen3.5:9b | A1 | C1 | 60 | 15.000 | 1 | 10 | 0.012 | 0.258 |
| qwen3.5:9b | A1 | C2 | 60 | 3.333 | 0 | 2 | 0.500 | 1.000 |
| qwen3.5:9b | A1 | C3 | 60 | 3.333 | 1 | 3 | 0.625 | 1.000 |
| qwen3.5:9b | A1 | C4 | 60 | -1.667 | 3 | 2 | 1.000 | 1.000 |
| qwen3.5:9b | A1 | C5 | 60 | 0.000 | 2 | 2 | 1.000 | 1.000 |
| qwen3.5:9b | A2 | C1 | 60 | -1.667 | 2 | 1 | 1.000 | 1.000 |
| qwen3.5:9b | A2 | C2 | 60 | -3.333 | 3 | 1 | 0.625 | 1.000 |
| qwen3.5:9b | A2 | C3 | 60 | 1.667 | 2 | 3 | 1.000 | 1.000 |
| qwen3.5:9b | A2 | C4 | 60 | 13.333 | 3 | 11 | 0.057 | 1.000 |
| qwen3.5:9b | A2 | C5 | 60 | -1.667 | 2 | 1 | 1.000 | 1.000 |

_(+15 linhas no CSV)_

## 3. QP2 — interações duplas

`mpl_pp`: interação na escala de taxa (pontos percentuais; MPL com EP robusto por cluster), sempre estimável. `coef_logit`: GEE logit, só nas classes sem separação; `bayes_media`: sensibilidade com intercepto aleatório por caso. Interação > 0 = redundância (juntos protegem menos que a soma); < 0 = complementaridade. Holm por classe sobre os termos estimados.

Nas classes com **separação** (um controle que, ligado, zera a classe), o modelo verdadeiro é p = (1 − Cs)·f(demais): as interações triplas com Cs não são desprezíveis e se confundem com as duplas na fração I = −ABCDE. Por isso a tabela mostra, nelas, o ajuste **condicional** (só configurações com Cs desligado), em codificação ±1 e como efeito fatorial (2β, p.p.); interações confundidas entre si aparecem unidas por '=' (ou '=−'), e o valor é a soma (ou diferença) delas. Quando a outra meia fração foi rodada, o ajuste mostrado é o '+ outra meia fração' (fatorial 2^4 completo com Cs desligado), sem pares confundidos. O ajuste completo está no CSV, só para conferência.

| classe | ajuste | termo | mpl_pp | mpl_ic_inf | mpl_ic_sup | mpl_p_holm | coef_logit | p_holm | bayes_media | separacao |
|---|---|---|---|---|---|---|---|---|---|---|
| A1 | completo | C(modelo)[T.qwen3.5:9b] | 39.570 | 25.711 | 53.429 | 0.000 | 1.753 | 0.000 | 5.314 |  |
| A1 | completo | C1:C2 | 0.766 | -2.398 | 3.929 | 1.000 | 0.033 | 1.000 | 0.073 |  |
| A1 | completo | C1:C3 | -2.429 | -5.586 | 0.728 | 1.000 | -0.118 | 1.000 | -0.426 |  |
| A1 | completo | C1:C4 | 0.766 | -1.927 | 3.459 | 1.000 | 0.036 | 1.000 | 0.123 |  |
| A1 | completo | C1:C5 | 0.627 | -2.058 | 3.312 | 1.000 | 0.030 | 1.000 | 0.105 |  |
| A1 | completo | C2:C3 | -1.318 | -4.100 | 1.465 | 1.000 | -0.064 | 1.000 | -0.239 |  |
| A1 | completo | C2:C4 | 1.877 | -1.387 | 5.140 | 1.000 | 0.090 | 1.000 | 0.305 |  |
| A1 | completo | C2:C5 | 0.071 | -2.642 | 2.785 | 1.000 | 0.003 | 1.000 | -0.003 |  |
| A1 | completo | C3:C4 | 0.349 | -2.421 | 3.119 | 1.000 | 0.017 | 1.000 | 0.067 |  |
| A1 | completo | C3:C5 | 1.877 | -2.058 | 5.812 | 1.000 | 0.091 | 1.000 | 0.338 |  |
| A1 | completo | C4:C5 | 0.071 | -2.629 | 2.771 | 1.000 | 0.005 | 1.000 | 0.031 |  |
| A2 | completo | C(modelo)[T.qwen3.5:9b] | -17.419 | -28.822 | -6.016 | 0.041 | -0.706 | 0.741 | -1.284 |  |
| A2 | completo | C1:C2 | -0.905 | -3.973 | 2.163 | 1.000 | -0.039 | 1.000 | -0.069 |  |
| A2 | completo | C1:C3 | 0.901 | -2.714 | 4.516 | 1.000 | 0.052 | 1.000 | 0.131 |  |
| A2 | completo | C1:C4 | 0.068 | -3.525 | 3.660 | 1.000 | 0.006 | 1.000 | 0.004 |  |
| A2 | completo | C1:C5 | 0.206 | -2.939 | 3.352 | 1.000 | -0.002 | 1.000 | -0.023 |  |
| A2 | completo | C2:C3 | 1.318 | -2.152 | 4.787 | 1.000 | 0.073 | 1.000 | 0.188 |  |
| A2 | completo | C2:C4 | -1.182 | -7.028 | 4.664 | 1.000 | 0.006 | 1.000 | 0.116 |  |
| A2 | completo | C2:C5 | -0.210 | -2.838 | 2.418 | 1.000 | -0.022 | 1.000 | -0.057 |  |
| A2 | completo | C3:C4 | -1.044 | -4.236 | 2.149 | 1.000 | -0.057 | 1.000 | -0.157 |  |
| A2 | completo | C3:C5 | -1.738 | -5.383 | 1.907 | 1.000 | -0.089 | 1.000 | -0.203 |  |
| A2 | completo | C4:C5 | -0.905 | -4.056 | 2.247 | 1.000 | -0.037 | 1.000 | -0.084 |  |
| A3 | condicional (C3=0) + outra meia fração | C1:C2 | -0.379 | -2.261 | 1.503 | 1.000 | — | — | — | C3 |
| A3 | condicional (C3=0) + outra meia fração | C1:C4 | -1.004 | -2.764 | 0.756 | 1.000 | — | — | — | C3 |
| A3 | condicional (C3=0) + outra meia fração | C1:C5 | 3.996 | 1.287 | 6.706 | 0.031 | — | — | — | C3 |
| A3 | condicional (C3=0) + outra meia fração | C2:C4 | -0.795 | -2.428 | 0.837 | 1.000 | — | — | — | C3 |
| A3 | condicional (C3=0) + outra meia fração | C2:C5 | -3.295 | -5.580 | -1.011 | 0.033 | — | — | — | C3 |
| A3 | condicional (C3=0) + outra meia fração | C4:C5 | 0.246 | -1.743 | 2.236 | 1.000 | — | — | — | C3 |
| A4 | condicional (C4=0) + outra meia fração | C1:C2 | 0.057 | -1.309 | 1.423 | 1.000 | — | — | — | C4 |
| A4 | condicional (C4=0) + outra meia fração | C1:C3 | 1.723 | 0.199 | 3.248 | 0.240 | — | — | — | C4 |
| A4 | condicional (C4=0) + outra meia fração | C1:C5 | -0.568 | -1.969 | 0.833 | 1.000 | — | — | — | C4 |
| A4 | condicional (C4=0) + outra meia fração | C2:C3 | -0.152 | -1.545 | 1.242 | 1.000 | — | — | — | C4 |
| A4 | condicional (C4=0) + outra meia fração | C2:C5 | -0.777 | -2.326 | 0.773 | 1.000 | — | — | — | C4 |
| A4 | condicional (C4=0) + outra meia fração | C3:C5 | 1.307 | -0.062 | 2.675 | 0.490 | — | — | — | C4 |
| A5 | condicional (C5=0) + outra meia fração | C1:C2 | -0.057 | -2.374 | 2.260 | 1.000 | — | — | — | C5 |
| A5 | condicional (C5=0) + outra meia fração | C1:C3 | 2.235 | -0.423 | 4.893 | 0.695 | — | — | — | C5 |
| A5 | condicional (C5=0) + outra meia fração | C1:C4 | 3.277 | 0.358 | 6.195 | 0.222 | — | — | — | C5 |
| A5 | condicional (C5=0) + outra meia fração | C2:C3 | -4.640 | -7.477 | -1.803 | 0.013 | — | — | — | C5 |
| A5 | condicional (C5=0) + outra meia fração | C2:C4 | -0.682 | -3.655 | 2.291 | 1.000 | — | — | — | C5 |
| A5 | condicional (C5=0) + outra meia fração | C3:C4 | 1.193 | -1.133 | 3.520 | 1.000 | — | — | — | C5 |

## 4. QP3 — legítimas: bloqueio indevido, recusa suave e utilidade

Cada métrica tem o seu n: dúvidas sem julgamento do juiz saem de recusa suave, bloqueio total e utilidade.

| modelo | config | n_casos | bloq_controle | n_recusa_suave | recusa_suave | bloq_total | n_utilidade | utilidade |
|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | base | 300 | 0.000 | 300 | 0.007 | 0.007 | 300 | 0.913 |
| claude-haiku-5-5 | completa | 300 | 0.067 | 300 | 0.007 | 0.073 | 300 | 0.867 |
| claude-haiku-5-5 | sem_C1 | 300 | 0.000 | 300 | 0.003 | 0.003 | 300 | 0.947 |
| claude-haiku-5-5 | sem_C2 | 300 | 0.067 | 300 | 0.000 | 0.067 | 300 | 0.877 |
| claude-haiku-5-5 | sem_C3 | 300 | 0.067 | 300 | 0.007 | 0.073 | 300 | 0.883 |
| claude-haiku-5-5 | sem_C4 | 300 | 0.067 | 300 | 0.000 | 0.067 | 300 | 0.880 |
| claude-haiku-5-5 | sem_C5 | 300 | 0.067 | 300 | 0.000 | 0.067 | 300 | 0.870 |
| gemma4:12b | C1+C2 | 300 | 0.067 | 300 | 0.010 | 0.077 | 300 | 0.853 |
| gemma4:12b | C1+C3 | 300 | 0.067 | 300 | 0.010 | 0.077 | 300 | 0.817 |
| gemma4:12b | C1+C4 | 300 | 0.067 | 300 | 0.007 | 0.073 | 300 | 0.833 |
| gemma4:12b | C1+C5 | 300 | 0.067 | 300 | 0.017 | 0.083 | 300 | 0.807 |
| gemma4:12b | C2+C3 | 300 | 0.000 | 300 | 0.010 | 0.010 | 300 | 0.900 |
| gemma4:12b | C2+C4 | 300 | 0.000 | 300 | 0.017 | 0.017 | 300 | 0.910 |
| gemma4:12b | C2+C5 | 300 | 0.000 | 300 | 0.017 | 0.017 | 300 | 0.917 |
| gemma4:12b | C3+C4 | 300 | 0.003 | 300 | 0.010 | 0.013 | 300 | 0.883 |
| gemma4:12b | C3+C5 | 300 | 0.000 | 300 | 0.017 | 0.017 | 300 | 0.867 |
| gemma4:12b | C4+C5 | 300 | 0.000 | 300 | 0.010 | 0.010 | 300 | 0.890 |
| gemma4:12b | base | 300 | 0.000 | 300 | 0.013 | 0.013 | 300 | 0.897 |
| gemma4:12b | completa | 300 | 0.067 | 300 | 0.013 | 0.080 | 300 | 0.847 |
| gemma4:12b | sem_C1 | 300 | 0.000 | 300 | 0.010 | 0.010 | 300 | 0.910 |
| gemma4:12b | sem_C2 | 300 | 0.070 | 300 | 0.010 | 0.080 | 300 | 0.813 |
| gemma4:12b | sem_C3 | 300 | 0.067 | 300 | 0.017 | 0.083 | 300 | 0.867 |
| gemma4:12b | sem_C4 | 300 | 0.067 | 300 | 0.017 | 0.083 | 300 | 0.837 |
| gemma4:12b | sem_C5 | 300 | 0.067 | 300 | 0.010 | 0.077 | 300 | 0.830 |
| qwen3.5:9b | C1+C2 | 300 | 0.067 | 300 | 0.000 | 0.067 | 300 | 0.733 |
| qwen3.5:9b | C1+C3 | 300 | 0.067 | 300 | 0.003 | 0.070 | 300 | 0.667 |
| qwen3.5:9b | C1+C4 | 300 | 0.067 | 300 | 0.007 | 0.073 | 300 | 0.663 |
| qwen3.5:9b | C1+C5 | 300 | 0.067 | 300 | 0.003 | 0.070 | 300 | 0.643 |
| qwen3.5:9b | C2+C3 | 300 | 0.000 | 300 | 0.000 | 0.000 | 300 | 0.740 |
| qwen3.5:9b | C2+C4 | 300 | 0.000 | 300 | 0.000 | 0.000 | 300 | 0.753 |
| qwen3.5:9b | C2+C5 | 300 | 0.000 | 300 | 0.000 | 0.000 | 300 | 0.753 |
| qwen3.5:9b | C3+C4 | 300 | 0.007 | 300 | 0.003 | 0.010 | 300 | 0.690 |
| qwen3.5:9b | C3+C5 | 300 | 0.000 | 300 | 0.000 | 0.000 | 300 | 0.720 |
| qwen3.5:9b | C4+C5 | 300 | 0.003 | 300 | 0.007 | 0.010 | 300 | 0.647 |
| qwen3.5:9b | base | 300 | 0.000 | 300 | 0.000 | 0.000 | 300 | 0.690 |
| qwen3.5:9b | completa | 300 | 0.067 | 300 | 0.000 | 0.067 | 300 | 0.693 |
| qwen3.5:9b | sem_C1 | 300 | 0.000 | 300 | 0.003 | 0.003 | 300 | 0.733 |
| qwen3.5:9b | sem_C2 | 300 | 0.067 | 300 | 0.000 | 0.067 | 300 | 0.677 |
| qwen3.5:9b | sem_C3 | 300 | 0.067 | 300 | 0.000 | 0.067 | 300 | 0.700 |
| qwen3.5:9b | sem_C4 | 300 | 0.067 | 300 | 0.000 | 0.067 | 300 | 0.687 |
| qwen3.5:9b | sem_C5 | 300 | 0.070 | 300 | 0.000 | 0.070 | 300 | 0.693 |

### Custo e latência (todas as interações)

| modelo | config | n | lat_mediana_s | lat_p95_s | tok_in_medio | tok_out_medio | usd_por_inter | usd_total |
|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | base | 600 | 2.270 | 4.579 | 2443 | 316.483 | 0.000 | 0.242 |
| claude-haiku-5-5 | completa | 600 | 2.531 | 5.405 | 2939 | 304.312 | 0.000 | 0.268 |
| claude-haiku-5-5 | sem_C1 | 600 | 2.404 | 4.942 | 3259 | 331.673 | 0.000 | 0.295 |
| claude-haiku-5-5 | sem_C2 | 600 | 2.550 | 5.427 | 2178 | 298.977 | 0.000 | 0.220 |
| claude-haiku-5-5 | sem_C3 | 600 | 2.558 | 5.410 | 3100 | 304.638 | 0.000 | 0.277 |
| claude-haiku-5-5 | sem_C4 | 600 | 2.521 | 4.889 | 2838 | 279.907 | 0.000 | 0.254 |
| claude-haiku-5-5 | sem_C5 | 600 | 2.580 | 5.306 | 2941 | 302.493 | 0.000 | 0.267 |
| gemma4:12b | C1+C2 | 600 | 7.209 | 15.520 | 1547 | 59.715 | 0.000 | 0.000 |
| gemma4:12b | C1+C3 | 600 | 6.493 | 14.249 | 1035 | 59.792 | 0.000 | 0.000 |
| gemma4:12b | C1+C4 | 600 | 6.926 | 15.235 | 1239 | 63.482 | 0.000 | 0.000 |
| gemma4:12b | C1+C5 | 600 | 6.648 | 15.039 | 1174 | 59.238 | 0.000 | 0.000 |
| gemma4:12b | C2+C3 | 600 | 6.944 | 14.743 | 1454 | 63.745 | 0.000 | 0.000 |
| gemma4:12b | C2+C4 | 600 | 7.361 | 15.595 | 1715 | 67.270 | 0.000 | 0.000 |
| gemma4:12b | C2+C5 | 600 | 7.242 | 15.532 | 1669 | 63.563 | 0.000 | 0.000 |
| gemma4:12b | C3+C4 | 600 | 6.841 | 14.351 | 1159 | 68.333 | 0.000 | 0.000 |
| gemma4:12b | C3+C5 | 600 | 6.670 | 13.806 | 1097 | 63.940 | 0.000 | 0.000 |
| gemma4:12b | C4+C5 | 600 | 7.175 | 15.517 | 1324 | 68.412 | 0.000 | 0.000 |
| gemma4:12b | base | 1800 | 6.871 | 15.120 | 1305 | 67.096 | 0.000 | 0.000 |
| gemma4:12b | completa | 1799 | 6.974 | 15.383 | 1381 | 59.210 | 0.000 | 0.000 |
| gemma4:12b | sem_C1 | 1800 | 7.209 | 15.408 | 1491 | 64.609 | 0.000 | 0.000 |
| gemma4:12b | sem_C2 | 1800 | 6.741 | 14.563 | 1057 | 61.479 | 0.000 | 0.000 |
| gemma4:12b | sem_C3 | 1800 | 7.348 | 16.237 | 1587 | 60.834 | 0.000 | 0.000 |
| gemma4:12b | sem_C4 | 1800 | 6.802 | 14.918 | 1336 | 56.781 | 0.000 | 0.000 |
| gemma4:12b | sem_C5 | 1800 | 6.976 | 15.089 | 1385 | 60.120 | 0.000 | 0.000 |
| qwen3.5:9b | C1+C2 | 600 | 5.788 | 15.569 | 1831 | 76.065 | 0.000 | 0.000 |
| qwen3.5:9b | C1+C3 | 600 | 4.965 | 16.101 | 1178 | 77.207 | 0.000 | 0.000 |
| qwen3.5:9b | C1+C4 | 600 | 5.746 | 18.151 | 1380 | 83.745 | 0.000 | 0.000 |
| qwen3.5:9b | C1+C5 | 600 | 5.068 | 15.583 | 1263 | 73.093 | 0.000 | 0.000 |
| qwen3.5:9b | C2+C3 | 600 | 5.679 | 14.956 | 1777 | 82.053 | 0.000 | 0.000 |
| qwen3.5:9b | C2+C4 | 600 | 6.420 | 16.071 | 2072 | 87.173 | 0.000 | 0.000 |
| qwen3.5:9b | C2+C5 | 600 | 6.106 | 14.584 | 2007 | 81.593 | 0.000 | 0.000 |
| qwen3.5:9b | C3+C4 | 600 | 6.056 | 14.458 | 1319 | 87.392 | 0.000 | 0.000 |
| qwen3.5:9b | C3+C5 | 600 | 5.556 | 15.346 | 1298 | 83.123 | 0.000 | 0.000 |
| qwen3.5:9b | C4+C5 | 600 | 5.999 | 16.123 | 1455 | 86.302 | 0.000 | 0.000 |
| qwen3.5:9b | base | 1800 | 5.636 | 15.442 | 1439 | 83.321 | 0.000 | 0.000 |
| qwen3.5:9b | completa | 1800 | 6.017 | 17.528 | 1707 | 78.370 | 0.000 | 0.000 |
| qwen3.5:9b | sem_C1 | 1800 | 6.120 | 16.999 | 1859 | 85.419 | 0.000 | 0.000 |
| qwen3.5:9b | sem_C2 | 1800 | 5.865 | 16.533 | 1208 | 80.269 | 0.000 | 0.000 |
| qwen3.5:9b | sem_C3 | 1800 | 6.073 | 16.725 | 1878 | 78.012 | 0.000 | 0.000 |
| qwen3.5:9b | sem_C4 | 1800 | 5.322 | 14.004 | 1612 | 71.278 | 0.000 | 0.000 |
| qwen3.5:9b | sem_C5 | 1800 | 6.010 | 14.903 | 1684 | 77.327 | 0.000 | 0.000 |

## 5. QP4 — adaptativo (sucesso final e razão adaptativo/estático, H2)

| modelo | config | n | taxa_adapt | ic_inf | ic_sup | taxa_estat | diferenca_pp | razao | k_mediano | pendentes_juiz |
|---|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | base | 100 | 0.260 | 0.184 | 0.354 | 0.207 | 5.333 | 1.258 | 4.000 | 0 |
| claude-haiku-5-5 | completa | 100 | 0.020 | 0.006 | 0.070 | 0.043 | -2.333 | 0.462 | 7.500 | 0 |
| gemma4:12b | base | 50 | 0.300 | 0.191 | 0.438 | 0.430 | -13.000 | 0.698 | 2.000 | 0 |
| gemma4:12b | completa | 50 | 0.040 | 0.011 | 0.135 | 0.097 | -5.667 | 0.414 | 6.000 | 0 |
| gemma4:12b | sem_C1 | 50 | 0.060 | 0.021 | 0.162 | 0.103 | -4.333 | 0.581 | 5.000 | 0 |
| gemma4:12b | sem_C2 | 50 | 0.040 | 0.011 | 0.135 | 0.113 | -7.333 | 0.353 | 10.000 | 0 |
| gemma4:12b | sem_C3 | 50 | 0.100 | 0.043 | 0.214 | 0.157 | -5.667 | 0.638 | 1.000 | 0 |
| gemma4:12b | sem_C4 | 50 | 0.120 | 0.056 | 0.238 | 0.163 | -4.333 | 0.735 | 13.500 | 0 |
| gemma4:12b | sem_C5 | 50 | 0.180 | 0.098 | 0.308 | 0.197 | -1.667 | 0.915 | 7.000 | 0 |
| qwen3.5:9b | base | 50 | 0.580 | 0.442 | 0.706 | 0.583 | -0.333 | 0.994 | 4.000 | 0 |
| qwen3.5:9b | completa | 50 | 0.220 | 0.128 | 0.352 | 0.147 | 7.333 | 1.500 | 7.000 | 0 |
| qwen3.5:9b | sem_C1 | 50 | 0.200 | 0.112 | 0.330 | 0.173 | 2.667 | 1.154 | 7.000 | 0 |
| qwen3.5:9b | sem_C2 | 50 | 0.260 | 0.159 | 0.396 | 0.147 | 11.333 | 1.773 | 7.000 | 0 |
| qwen3.5:9b | sem_C3 | 50 | 0.300 | 0.191 | 0.438 | 0.217 | 8.333 | 1.385 | 4.000 | 0 |
| qwen3.5:9b | sem_C4 | 50 | 0.300 | 0.191 | 0.438 | 0.240 | 6.000 | 1.250 | 5.000 | 0 |
| qwen3.5:9b | sem_C5 | 50 | 0.300 | 0.191 | 0.438 | 0.297 | 0.333 | 1.011 | 4.000 | 0 |

Curva acumulada por tentativa: `5_qp4_curva.csv`.

## 6. Exploratória — bloqueio do C1 em legítimas com e sem gatilho (configs com C1)

| modelo | gatilho | n_casos | bloqueados_c1 | taxa | ic_inf | ic_sup | razao_chances_fisher | p_fisher |
|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | False | 200 | 0 | 0.000 | 0.000 | 0.019 | inf | 0.000 |
| claude-haiku-5-5 | True | 100 | 20 | 0.200 | 0.133 | 0.289 | inf | 0.000 |
| gemma4:12b | False | 200 | 0 | 0.000 | 0.000 | 0.019 | inf | 0.000 |
| gemma4:12b | True | 100 | 20 | 0.200 | 0.133 | 0.289 | inf | 0.000 |
| qwen3.5:9b | False | 200 | 0 | 0.000 | 0.000 | 0.019 | inf | 0.000 |
| qwen3.5:9b | True | 100 | 20 | 0.200 | 0.133 | 0.289 | inf | 0.000 |

### Por fórmula de gatilho

| forma_gatilho | n_casos | taxa_bloqueio_c1 |
|---|---|---|
| 1 | 4 | 1.000 |
| 2 | 3 | 1.000 |
| 9 | 4 | 1.000 |
| 23 | 4 | 1.000 |
| 7 | 3 | 0.667 |
| 15 | 2 | 0.500 |
| 17 | 3 | 0.333 |
| 24 | 3 | 0.333 |
| 0 | 2 | 0.000 |
| 8 | 10 | 0.000 |
| 6 | 5 | 0.000 |
| 5 | 2 | 0.000 |
| 4 | 4 | 0.000 |
| 3 | 3 | 0.000 |
| 12 | 5 | 0.000 |
| 11 | 2 | 0.000 |
| 10 | 3 | 0.000 |
| 16 | 5 | 0.000 |
| 14 | 7 | 0.000 |
| 13 | 2 | 0.000 |
| 18 | 4 | 0.000 |
| 20 | 6 | 0.000 |
| 19 | 6 | 0.000 |
| 22 | 4 | 0.000 |
| 21 | 3 | 0.000 |

## 7. Amostra qualitativa

30 falhas em `7_amostra_qualitativa.csv` (preencher `categoria_falha` na leitura).

## 8. Concordância autor × LLM-juiz (1 anotador humano)

| arquivo | tipo | n | concordancia | kappa | kappa_ic_inf | kappa_ic_sup | ac1_gwet | prev_humano | prev_juiz |
|---|---|---|---|---|---|---|---|---|---|
| anotacao_juiz_interacoes_comercial.csv | todos | 16 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | 0.500 |
| anotacao_juiz_interacoes_comercial.csv | atendimento | 9 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.889 | 0.889 |
| anotacao_juiz_interacoes_comercial.csv | obediencia | 7 | 1.000 | — | — | — | 1.000 | 0.000 | 0.000 |
| anotacao_juiz_interacoes_gemma.csv | todos | 61 | 0.967 | 0.907 | 0.758 | 1.000 | 0.949 | 0.754 | 0.787 |
| anotacao_juiz_interacoes_gemma.csv | atendimento | 37 | 0.946 | 0.479 | 0.000 | 1.000 | 0.940 | 0.919 | 0.973 |
| anotacao_juiz_interacoes_gemma.csv | obediencia | 24 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | 0.500 |
| anotacao_juiz_interacoes_qwen.csv | todos | 61 | 0.902 | 0.749 | 0.534 | 0.919 | 0.840 | 0.689 | 0.787 |
| anotacao_juiz_interacoes_qwen.csv | atendimento | 42 | 0.952 | 0.000 | 0.000 | 0.000 | 0.950 | 0.952 | 1.000 |
| anotacao_juiz_interacoes_qwen.csv | obediencia | 19 | 0.789 | 0.406 | -0.000 | 0.826 | 0.685 | 0.105 | 0.316 |
| TODOS | todos | 138 | 0.942 | 0.855 | 0.747 | 0.946 | 0.904 | 0.696 | 0.754 |
| TODOS | atendimento | 88 | 0.955 | 0.482 | 0.000 | 0.877 | 0.950 | 0.932 | 0.977 |
| TODOS | obediencia | 50 | 0.920 | 0.818 | 0.636 | 0.957 | 0.858 | 0.280 | 0.360 |

### 8b. Adaptativo: juiz × revisão humana (amostra estratificada pela decisão do juiz)

| modelo | n | concordancia | kappa | ac1_gwet | juiz_sim | juiz_sim_humano_sim | vpp_juiz_sim | juiz_nao | juiz_nao_humano_nao |
|---|---|---|---|---|---|---|---|---|---|
| todos | 147 | 0.442 | 0.111 | -0.056 | 97 | 15 | 0.155 | 50 | 50 |
| comercial | 61 | 0.459 | 0.103 | 0.005 | 38 | 5 | 0.132 | 23 | 23 |
| gemma | 23 | 0.435 | 0.057 | -0.008 | 14 | 1 | 0.071 | 9 | 9 |
| qwen | 63 | 0.429 | 0.125 | -0.120 | 45 | 9 | 0.200 | 18 | 18 |

### 8c. Estático do Haiku: juiz × revisão humana (todos os 'sim' + 15 'não')

| modelo | n | concordancia | kappa | ac1_gwet | juiz_sim | juiz_sim_humano_sim | vpp_juiz_sim | juiz_nao | juiz_nao_humano_nao |
|---|---|---|---|---|---|---|---|---|---|
| todos | 46 | 0.891 | 0.772 | 0.794 | 31 | 26 | 0.839 | 15 | 15 |
| comercial | 46 | 0.891 | 0.772 | 0.794 | 31 | 26 | 0.839 | 15 | 15 |
