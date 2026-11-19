import json, sys, time
sys.path.insert(0, ".")
from assistente import Assistente
from controles.c1_detector import DetectorHeuristico
from llm import ModeloOllama
from veredito import julgar
from dataclasses import asdict
base = json.load(open("loja/base.json"))
casos = [json.loads(l) for l in open("cargas/exemplos.jsonl")]
ctl_b = dict.fromkeys(["C1","C2","C3","C4","C5"], False)
for nome in sys.argv[1:]:
    m = ModeloOllama("http://localhost:11434", nome)
    t0 = time.time(); ok = 0; tc = 0
    linhas = []
    for caso in casos:
        a = Assistente(base, m, ctl_b, DetectorHeuristico(), 0.5)
        r = asdict(a.atender(caso["cliente_id"], caso["mensagem"], caso.get("docs_injetados")))
        v = julgar(caso, r, base)
        tc += len(r["chamadas"])
        linhas.append((caso["id"], round(r["latencia_s"],1), r["tokens_entrada"], len(r["chamadas"]),
                       v.get("sucesso_ataque", v.get("tarefa_concluida")), r["resposta"][:90].replace("\n"," ")))
    print(f"== {nome}: {time.time()-t0:.0f}s para {len(casos)} casos, {tc} chamadas de ferramenta")
    for l in linhas: print("  ", *l)
