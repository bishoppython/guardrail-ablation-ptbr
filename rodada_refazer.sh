#!/usr/bin/env bash
# Depois de rodada.sh e rodada_pos.sh: refaz as buscas adaptativas locais que pararam num falso sucesso de A5
# (regra do titular, 18/11/2026; ver refazer_truncados.py) e julga as tentativas novas. Retomável e idempotente:
# rodar de novo só refaz o que faltar. O Haiku não precisa: o adaptativo dele já roda com a regra nova.
set -u
cd "$(dirname "$0")"
PY=.venv/bin/python; S=saida; LOG=$S/rodada.log
OBJ50=$(cat cargas/objetivos_locais_50.txt)
until grep -q "^== fim pos" $LOG && ! pgrep -f "bash ./rodada(_pos)?\.sh" > /dev/null; do sleep 300; done
echo "== refazer truncados (regra A5) $(date '+%F %T')" >> $LOG
for m in qwen gemma; do
  $PY refazer_truncados.py $S/adaptativo_$m.jsonl >> $LOG 2>&1
  $PY adaptativo.py --modelo $m --configs obrigatorias --objetivos "$OBJ50" --saida $S/adaptativo_$m.jsonl >> $LOG 2>&1
  echo "== juiz adaptativo $m (refeitos) $(date '+%F %T')" >> $LOG
  $PY juiz.py $S/adaptativo_$m.jsonl >> $LOG 2>&1
done
echo "== fim refazer $(date '+%F %T')" >> $LOG
