#!/usr/bin/env bash
# Retoma a rodada depois de uma parada (desligamento, queda de energia, travamento).
#   ./retomar.sh            confere os arquivos e relança rodada.sh + rodada_pos.sh em segundo plano
#   ./retomar.sh --checar   só confere, não relança
# Conferência: a última linha de cada JSONL em saida/ precisa ser JSON completo. Uma linha cortada (queda de
# energia no meio da gravação) quebraria a retomada; ela é guardada em saida/linhas_cortadas.txt (nada se perde)
# e retirada do arquivo, e a interação correspondente é refeita.
set -u
cd "$(dirname "$0")"
PY=.venv/bin/python; LOG=saida/rodada.log

if pgrep -f "bash ./rodada.sh" > /dev/null; then
  echo "A rodada já está rodando; nada a fazer."; exit 0
fi

$PY - <<'EOF'
import json, pathlib, datetime
cortadas = pathlib.Path("saida/linhas_cortadas.txt")
for p in sorted(pathlib.Path("saida").glob("*.jsonl")):
    linhas = p.read_text().splitlines(keepends=True)
    if not linhas:
        continue
    try:
        json.loads(linhas[-1])
        ok = linhas[-1].endswith("\n")
    except json.JSONDecodeError:
        ok = False
    if not ok:
        with cortadas.open("a") as f:
            f.write(f"# {p} {datetime.datetime.now():%F %T}\n{linhas[-1].rstrip()}\n")
        p.write_text("".join(linhas[:-1]))
        print(f"linha cortada removida de {p} (guardada em {cortadas})")
    # linhas inválidas no meio do arquivo não são corrigidas aqui: avisar
    for i, l in enumerate(linhas[:-1], 1):
        try:
            json.loads(l)
        except json.JSONDecodeError:
            print(f"ATENÇÃO: linha {i} inválida no meio de {p}; corrigir à mão antes de retomar")
print("arquivos conferidos")
EOF

if ! curl -s --max-time 5 http://localhost:11434/api/tags > /dev/null; then
  echo "ATENÇÃO: Ollama não responde em localhost:11434 (docker start ollama). Não relancei."; exit 1
fi
# GPU: sem ela o Ollama cai para CPU sem avisar e a rodada fica ~50x mais lenta (ex.: kernel novo sem módulo NVIDIA)
if ! nvidia-smi > /dev/null 2>&1; then
  echo "ATENÇÃO: nvidia-smi falhou (driver NVIDIA não carregado). Não relancei."; exit 1
fi
if ! docker exec ollama nvidia-smi > /dev/null 2>&1; then
  echo "ATENÇÃO: o contêiner do Ollama não enxerga a GPU (docker restart ollama e conferir). Não relancei."; exit 1
fi
echo "Ollama e GPU ok ($(nvidia-smi --query-gpu=name,driver_version --format=csv,noheader); kernel $(uname -r))"
[ "${1:-}" = "--checar" ] && exit 0

echo "== retomada $(date '+%F %T')" >> $LOG
setsid nohup ./rodada.sh > /dev/null 2>&1 < /dev/null &
setsid nohup ./rodada_pos.sh > /dev/null 2>&1 < /dev/null &
# refaz as buscas adaptativas truncadas pela regra antiga de A5 (18/11/2026); espera a rodada acabar
pgrep -f "bash ./rodada_refazer.sh" > /dev/null || setsid nohup ./rodada_refazer.sh > /dev/null 2>&1 < /dev/null &
# impede suspensão (inclusive ao fechar a tampa) enquanto a rodada roda; some sozinho quando ela termina
if ! systemd-inhibit --list 2>/dev/null | grep -q "rodada SBSeg"; then
  sleep 2
  setsid nohup systemd-inhibit --what=sleep:idle:handle-lid-switch --who="rodada SBSeg" --why="experimento em execução" \
    --mode=block bash -c 'while pgrep -f "bash ./rodada" >/dev/null; do sleep 600; done' > /dev/null 2>&1 < /dev/null &
fi
sleep 2
pgrep -af "bash ./rodada" | cut -c1-80
echo "Retomada. Acompanhe em saida/rodada.log"
