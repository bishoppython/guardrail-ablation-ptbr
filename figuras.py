"""Figuras 2–4 do artigo a partir dos CSVs do analisar.py (rascunho, seção 5).

Uso: .venv/bin/python figuras.py [--en] [pasta da análise]   (padrão: saida/analise)
--en: rótulos em inglês, arquivos fig{2,3,4}_*_en.* (manuscrito da Elsevier).
Saída: <pasta>/figuras/fig{2,3,4}_*.pdf e .png (largura de texto do modelo SBC, ~16 cm).

- Fig. 2 (QP1): mapa de calor controle × classe, Δ da taxa de sucesso de ataque ao remover o controle da
  completa (p.p.), um painel por modelo; divergente azul ↔ cinza ↔ vermelho; * = significativo após Holm.
- Fig. 3 (QP3): proteção × custo por configuração (x = bloqueio indevido total das legítimas, y = sucesso de
  ataque em todas as classes); cor e forma por modelo (identidade nunca só pela cor); base e completa rotuladas.
- Fig. 4 (QP4): sucesso acumulado por tentativa no adaptativo, um painel por modelo, rótulo direto no fim.
Paleta: a de referência da skill de visualização (3 primeiras cores categóricas validadas em todos os pares).
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

RAIZ = Path(__file__).resolve().parent
TINTA, TINTA2, GRADE = "#0b0b0b", "#52514e", "#e4e3df"
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6"]
NEUTRO = "#8a8984"
MARCAS = ["o", "s", "^"]
DIVERGENTE = LinearSegmentedColormap.from_list("azul_cinza_vermelho", ["#1c5cab", "#f0efec", "#c23b3a"])
NOME = {"qwen3.5:9b": "Qwen 3.5 9B", "gemma4:12b": "Gemma 4 12B", "claude-haiku-5-5": "Claude Haiku 5.5"}
ORDEM_MODELOS = ["qwen3.5:9b", "gemma4:12b", "claude-haiku-5-5"]
IDIOMA = "pt"
EN = {"Colunas: classe de ameaça. Δ da taxa de sucesso de ataque ao remover o controle da completa (p.p.); "
      "* = significativo após Holm": "Columns: threat class. Δ in attack success rate when the control is removed "
      "from the full configuration (p.p.); * = significant after Holm correction",
      "Bloqueio indevido de legítimas (%)": "False blocking of legitimate requests (%)",
      "Sucesso de ataque, todas as classes (%)": "Attack success, all classes (%)",
      "Tentativa": "Attempt", "Objetivos atingidos (%)": "Objectives achieved (%)"}


def T(texto: str) -> str:
    return EN.get(texto, texto) if IDIOMA == "en" else texto


def conf_rot(conf: str) -> str:
    """Nome da configuração na figura: sem_C1 → "sem C1" (pt) ou "without C1" (en); completa → full."""
    if IDIOMA == "en":
        return {"completa": "full"}.get(conf, conf.replace("sem_", "without "))
    return conf.replace("_", " ")
CM = 1 / 2.54
LARGURA = 16 * CM

plt.rcParams.update({
    "font.size": 8, "axes.titlesize": 8.5, "axes.labelsize": 8, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "legend.fontsize": 7.5, "axes.edgecolor": TINTA2, "axes.labelcolor": TINTA, "xtick.color": TINTA2,
    "ytick.color": TINTA2, "text.color": TINTA, "axes.spines.top": False, "axes.spines.right": False,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6, "pdf.fonttype": 42,
    "figure.dpi": 150, "savefig.bbox": "tight", "savefig.pad_inches": 0.03,
})


def modelos_em(df: pd.DataFrame) -> list[str]:
    return [m for m in ORDEM_MODELOS if m in set(df["modelo"])] + \
        sorted(set(df["modelo"]) - set(ORDEM_MODELOS))


def salvar(fig, pasta: Path, nome: str) -> None:
    nome += "_en" if IDIOMA == "en" else ""
    for ext in ("pdf", "png"):
        fig.savefig(pasta / f"{nome}.{ext}")
    plt.close(fig)
    print("gravada", pasta / f"{nome}.pdf")


def fig2_qp1(a: Path, pasta: Path) -> None:
    q = pd.read_csv(a / "2_qp1_mcnemar.csv")
    mods = modelos_em(q)
    classes, ctls = sorted(q["classe"].unique()), sorted(q["controle"].unique())
    fig, axs = plt.subplots(1, len(mods), figsize=(LARGURA, 5.2 * CM), squeeze=False)
    for ax, m in zip(axs[0], mods):
        g = q[q["modelo"] == m].set_index(["controle", "classe"])
        z = np.array([[g.loc[(c, k), "diferenca_pp"] if (c, k) in g.index else np.nan for k in classes]
                      for c in ctls])
        ax.imshow(z, cmap=DIVERGENTE, vmin=-100, vmax=100, aspect="auto")
        for i, c in enumerate(ctls):
            for j, k in enumerate(classes):
                if np.isnan(z[i, j]):
                    continue
                sig = (c, k) in g.index and g.loc[(c, k), "p_holm"] < 0.05
                cor = "white" if abs(z[i, j]) > 55 else TINTA
                rot = "0" if round(z[i, j]) == 0 else f"{z[i, j]:+.0f}"
                ax.text(j, i, rot + ("*" if sig else ""), ha="center", va="center", fontsize=7,
                        color=cor)
        ax.set_xticks(range(len(classes)), classes)
        ax.set_yticks(range(len(ctls)), [conf_rot(f"sem_{c}") for c in ctls])
        ax.set_title(NOME.get(m, m))
        ax.tick_params(length=0)
        for s in ax.spines.values():
            s.set_visible(False)
        ax.set_xticks(np.arange(-.5, len(classes)), minor=True)
        ax.set_yticks(np.arange(-.5, len(ctls)), minor=True)
        ax.grid(which="minor", color="white", linewidth=1.5)
        ax.tick_params(which="minor", length=0)
        if ax is not axs[0][0]:
            ax.set_yticklabels([])
    fig.text(0.5, -0.04, T("Colunas: classe de ameaça. Δ da taxa de sucesso de ataque ao remover o controle da completa (p.p.); "
                           "* = significativo após Holm"), ha="center", fontsize=7, color=TINTA2)
    salvar(fig, pasta, "fig2_qp1_mapa")


def fig3_qp3(a: Path, pasta: Path) -> None:
    s = pd.read_csv(a / "1_sucesso_ataque.csv")
    s = s[s["classe"] == "todas"][["modelo", "config", "taxa"]]
    le = pd.read_csv(a / "4_qp3_legitimas.csv")[["modelo", "config", "bloq_total"]]
    d = s.merge(le, on=["modelo", "config"])
    fig, ax = plt.subplots(figsize=(LARGURA * 0.62, 6.2 * CM))
    for i, m in enumerate(modelos_em(d)):
        g = d[d["modelo"] == m]
        ax.scatter(100 * g["bloq_total"], 100 * g["taxa"], s=26, marker=MARCAS[i % 3], color=CAT[i % 3],
                   edgecolor="white", linewidth=0.8, zorder=3, label=NOME.get(m, m))
        for _, r in g[g["config"].isin(["base", "completa"])].iterrows():
            # o "base" do Haiku cai junto de um ponto do Qwen (configs sem C1): rótulo à esquerda
            esq = "haiku" in m and r["config"] == "base"
            ax.annotate(conf_rot(r["config"]), (100 * r["bloq_total"], 100 * r["taxa"]),
                        xytext=(-3, 3) if esq else (4, 3), ha="right" if esq else "left",
                        textcoords="offset points", fontsize=6.5, color=TINTA2)
    ax.set_xlabel(T("Bloqueio indevido de legítimas (%)"))
    ax.set_ylabel(T("Sucesso de ataque, todas as classes (%)"))
    ax.set_xlim(left=-1)
    ax.set_ylim(bottom=-1)
    ax.spines["left"].set_position(("data", -1))
    ax.grid(color=GRADE, linewidth=0.5)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="upper right")
    salvar(fig, pasta, "fig3_qp3_protecao_custo")


def fig4_qp4(a: Path, pasta: Path) -> None:
    p = a / "5_qp4_curva.csv"
    if not p.exists():
        print("sem adaptativo; fig. 4 pulada")
        return
    c = pd.read_csv(p)
    c = c[c["classe"] == "todas"]
    mods = modelos_em(c)
    fig, axs = plt.subplots(1, len(mods), figsize=(LARGURA, 5.4 * CM), squeeze=False, sharey=True)
    ordem = ["completa"] + [f"sem_C{i}" for i in range(1, 6)] + ["base"]
    for ax, m in zip(axs[0], mods):
        g = c[c["modelo"] == m]
        confs = [x for x in ordem if x in set(g["config"])]
        fim = []
        for j, conf in enumerate(confs):
            h = g[g["config"] == conf].sort_values("k")
            base = conf == "base"
            cor = NEUTRO if base else CAT[ordem.index(conf) % len(CAT)]
            ax.step(h["k"], 100 * h["acumulado"], where="post", color=cor, linewidth=1.6 if conf == "completa"
                    else 1.1, linestyle="--" if base else "-", zorder=3 if conf == "completa" else 2)
            fim.append((100 * h["acumulado"].iloc[-1], conf_rot(conf), cor))
        # rótulos diretos no fim, afastados para não colidir
        fim.sort()
        ys, ult = [], -99
        for y, _, _ in fim:
            ult = max(y, ult + 7)
            ys.append(ult)
        kmax = g["k"].max()
        # cotovelo: a curva segue reta (o valor final não muda) e só o fio pontilhado, cinza, sobe ao rótulo;
        # um fio da cor da curva e quase vertical parecia um salto do sucesso na última tentativa
        for (y, nome, cor), yl in zip(fim, ys):
            ax.plot([kmax, kmax + 1.2], [y, y], color=cor, linewidth=1.1, solid_capstyle="butt")
            ax.plot([kmax + 1.2, kmax + 2.6], [y, yl], color=GRADE, linewidth=0.6, linestyle=":")
            ax.plot([kmax + 2.6, kmax + 3.0], [yl, yl], color=cor, linewidth=1.6)
            ax.text(kmax + 3.3, yl, nome, fontsize=6.5, color=TINTA2, va="center")
        ax.set_title(NOME.get(m, m))
        ax.set_xlim(1, kmax + 11)
        ax.spines["bottom"].set_bounds(1, kmax)
        ax.set_xticks([1, 5, 10, 15, 20])
        ax.set_ylim(0, 105)
        ax.grid(axis="y", color=GRADE, linewidth=0.5)
        ax.set_axisbelow(True)
        ax.set_xlabel(T("Tentativa"))
    axs[0][0].set_ylabel(T("Objetivos atingidos (%)"))
    salvar(fig, pasta, "fig4_qp4_curva")


def main() -> None:
    global IDIOMA
    args = sys.argv[1:]
    if "--en" in args:
        IDIOMA = "en"
        args.remove("--en")
    a = Path(args[0]) if args else RAIZ / "saida" / "analise"
    pasta = a / "figuras"
    pasta.mkdir(parents=True, exist_ok=True)
    fig2_qp1(a, pasta)
    fig3_qp3(a, pasta)
    fig4_qp4(a, pasta)


if __name__ == "__main__":
    main()
