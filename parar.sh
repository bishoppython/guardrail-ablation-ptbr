#!/usr/bin/env bash
# Para a rodada com segurança antes de desligar o computador.
# Ordem: primeiro os orquestradores (para não dispararem a próxima etapa), depois os processos Python.
# Cada interação é gravada e sincronizada (flush) inteira; o que estava em andamento é refeito na retomada.
set -u
cd "$(dirname "$0")"
LOG=saida/rodada.log
pkill -f "bash ./rodada_pos.sh" && echo "rodada_pos.sh parado"
pkill -f "bash ./rodada_refazer.sh" && echo "rodada_refazer.sh parado"
pkill -f "bash ./rodada.sh" && echo "rodada.sh parado"
pkill -TERM -f ".venv/bin/python (executar|juiz|adaptativo).py" && echo "processos Python parados"
sleep 3
if pgrep -f ".venv/bin/python (executar|juiz|adaptativo).py" > /dev/null; then
  pkill -KILL -f ".venv/bin/python (executar|juiz|adaptativo).py"; echo "processos Python forçados"
fi
echo "== parada manual $(date '+%F %T')" >> $LOG
sync
echo "Pode desligar. Para retomar depois: ./retomar.sh"
