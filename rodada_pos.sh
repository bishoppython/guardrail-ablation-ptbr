#!/usr/bin/env bash
# Depois do rodada.sh: juiz post hoc das tentativas adaptativas pendentes (decisão de 11/11/2026). Retomável.
set -u
cd "$(dirname "$0")"
PY=.venv/bin/python; S=saida; LOG=$S/rodada.log
until grep -q "^== fim" $LOG; do sleep 300; done
for m in qwen gemma comercial; do
  echo "== juiz adaptativo $m $(date '+%F %T')" >> $LOG
  $PY juiz.py $S/adaptativo_$m.jsonl >> $LOG 2>&1
done
echo "== fim pos $(date '+%F %T')" >> $LOG
