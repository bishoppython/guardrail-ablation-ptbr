#!/usr/bin/env bash
# Rodada completa (decisões do autor em 11/11/2026): desenho recomendado,
# Haiku em paralelo (O1), adaptativo local com 50 objetivos sorteados, meia fração extra (protocolo 7.1).
# Retomável: rodar de novo continua de onde parou (cada etapa pula o que já está gravado).
set -u
cd "$(dirname "$0")"
PY=.venv/bin/python; S=saida; LOG=$S/rodada.log
CARGAS="cargas/legitimas.jsonl cargas/ataques_estaticos.jsonl"
OBJ50=$(cat cargas/objetivos_locais_50.txt)
fase() { echo "== $* $(date '+%F %T')" >> $LOG; }

# Haiku (API) em paralelo: estático nas 7 obrigatórias × 1 rep.; o juiz dele roda na fila da GPU
( fase "haiku estatico"; $PY executar.py --modelo comercial --cargas $CARGAS --configs obrigatorias --reps 1 \
    --saida $S/interacoes_comercial.jsonl >> $S/haiku.log 2>&1; fase "haiku estatico fim" ) &

# Fila da GPU (um modelo local por vez)
for m in qwen gemma; do
  fase "estatico $m obrigatorias x3"
  $PY executar.py --modelo $m --cargas $CARGAS --configs obrigatorias --reps 3 --saida $S/interacoes_$m.jsonl >> $LOG 2>&1
  fase "estatico $m demais x1"
  $PY executar.py --modelo $m --cargas $CARGAS --configs todas --reps 1 --saida $S/interacoes_$m.jsonl >> $LOG 2>&1
  fase "juiz $m"; $PY juiz.py $S/interacoes_$m.jsonl >> $LOG 2>&1
done
wait  # o Haiku já terminou há muito tempo; garante antes do juiz dele
fase "juiz comercial"; $PY juiz.py $S/interacoes_comercial.jsonl >> $LOG 2>&1
for m in qwen gemma; do
  fase "meia fracao extra $m"
  $PY executar.py --modelo $m --cargas cargas/ataques_estaticos.jsonl --configs extra --reps 1 --saida $S/extra_$m.jsonl >> $LOG 2>&1
  fase "juiz extra $m"; $PY juiz.py $S/extra_$m.jsonl >> $LOG 2>&1
done
for m in qwen gemma; do
  fase "adaptativo $m"
  $PY adaptativo.py --modelo $m --configs obrigatorias --objetivos "$OBJ50" --saida $S/adaptativo_$m.jsonl >> $LOG 2>&1
done
fase "adaptativo comercial"
$PY adaptativo.py --modelo comercial --configs base,completa --saida $S/adaptativo_comercial.jsonl >> $LOG 2>&1
fase "fim"
