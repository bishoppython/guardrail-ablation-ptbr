"""Figura 1 do artigo: arquitetura do assistente, posição dos controles C1–C5 e fronteiras de confiança.

Uso: .venv/bin/python fig1_arquitetura.py [--en] [pasta de saída]   (padrão: saida/figuras)
--en gera a versão em inglês (fig1_arquitetura_en.*), para o manuscrito da Elsevier.
Diagrama, não gráfico de dados: controles em azul (a mesma cor primária das figuras 2–4), componentes do
sistema em branco com borda, fronteiras de confiança tracejadas. Legível em escala de cinza (controle = caixa
cheia; componente = caixa vazada).
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

RAIZ = Path(__file__).resolve().parent
TINTA, TINTA2, BORDA = "#0b0b0b", "#52514e", "#8a8984"
CONTROLE, CONTROLE_TXT = "#2a78d6", "white"
FRONTEIRA = "#c23b3a"
CM = 1 / 2.54

plt.rcParams.update({"font.size": 7.5, "pdf.fonttype": 42, "figure.dpi": 150,
                     "savefig.bbox": "tight", "savefig.pad_inches": 0.03})


EN = {
    "Cliente\nautenticado": "Authenticated\ncustomer",
    "Modelo de\nlinguagem": "Language\nmodel",
    "Resposta": "Response",
    "recusa padrão\nacima do limiar": "standard refusal\nabove threshold",
    "regenera 1×;\ndepois encaminha": "regenerates once;\nthen hands off",
    "Base de\nconhecimento": "Knowledge\nbase",
    "consulta": "query",
    "Ferramentas e banco\n(consultar, cancelar, reembolsar)": "Tools and database\n(look up, cancel, refund)",
    "chamada": "call",
    "retorno": "output",
    "cliente malicioso\n(A1, A3–A5)": "malicious customer\n(A1, A3–A5)",
    "atacante indireto (A2)": "indirect attacker (A2)",
    "controle avaliado": "evaluated control",
    "componente do sistema": "system component",
    "fronteira de confiança": "trust boundary",
}
IDIOMA = "pt"


def T(texto: str) -> str:
    """Rótulo no idioma da figura (pt é o texto-fonte; en vem do dicionário)."""
    return EN[texto] if IDIOMA == "en" else texto


def caixa(ax, x, y, w, h, texto, controle=False, fs=7.2):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.08",
                                facecolor=CONTROLE if controle else "white",
                                edgecolor=CONTROLE if controle else BORDA, linewidth=0.9, zorder=3))
    ax.text(x, y, texto, ha="center", va="center", fontsize=fs, zorder=4,
            color=CONTROLE_TXT if controle else TINTA, fontweight="bold" if controle else "normal")


def seta(ax, p, q, estilo="-|>", cor=TINTA2, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=estilo, mutation_scale=7, color=cor, linewidth=0.8,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0, zorder=2))


def fronteira(ax, x0, y0, x1, y1, rotulo, dx=0.0, dy=0.0, ha="center"):
    ax.plot([x0, x1], [y0, y1], linestyle=(0, (3, 2)), color=FRONTEIRA, linewidth=0.9, zorder=1)
    ax.text(x1 + dx, y1 + dy, rotulo, color=FRONTEIRA, fontsize=6.5, ha=ha, va="center")


def main() -> None:
    global IDIOMA
    args = sys.argv[1:]
    if "--en" in args:
        IDIOMA = "en"
        args.remove("--en")
    sufixo = "_en" if IDIOMA == "en" else ""
    pasta = Path(args[0]) if args else RAIZ / "saida" / "figuras"
    pasta.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(16 * CM, 7.2 * CM))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 7.2)
    ax.axis("off")

    w, h, wc = 1.9, 0.75, 0.75  # componente; controle (quadrado)
    ym, yt, yb = 3.6, 6.1, 1.25  # linha do meio (conversa), de cima (recuperação), de baixo (ferramentas)
    xm, wm = 8.2, 2.4  # modelo

    def linha(pts, cor=TINTA2):  # polilinha ortogonal com seta no último trecho
        for a, b in zip(pts[:-2], pts[1:-1]):
            ax.plot([a[0], b[0]], [a[1], b[1]], color=cor, linewidth=0.8, zorder=2, solid_capstyle="butt")
        seta(ax, pts[-2], pts[-1], cor=cor)

    # linha do meio: conversa
    caixa(ax, 1.3, ym, 2.3, 0.95, T("Cliente\nautenticado"), fs=6.8)
    caixa(ax, 3.9, ym, wc, h, "C1", True)
    caixa(ax, xm, ym, wm, 1.15, T("Modelo de\nlinguagem"))
    caixa(ax, 10.6, ym, wc, h, "C4", True)
    caixa(ax, 11.7, ym, wc, h, "C3", True)
    caixa(ax, 13.6, ym, 1.9, h, T("Resposta"))
    seta(ax, (2.45, ym), (3.9 - wc / 2, ym))
    seta(ax, (3.9 + wc / 2, ym), (xm - wm / 2, ym))
    seta(ax, (xm + wm / 2, ym), (10.6 - wc / 2, ym))
    seta(ax, (10.6 + wc / 2, ym), (11.7 - wc / 2, ym))
    seta(ax, (11.7 + wc / 2, ym), (13.6 - 0.95, ym))
    ax.text(3.9, ym - 0.5, T("recusa padrão\nacima do limiar"), ha="center", va="top", fontsize=6, color=TINTA2)
    ax.text(10.6, ym - 0.5, T("regenera 1×;\ndepois encaminha"), ha="center", va="top", fontsize=6, color=TINTA2)

    # linha de cima: recuperação
    caixa(ax, 1.3, yt, 2.3, 0.95, T("Base de\nconhecimento"), fs=6.8)
    caixa(ax, 4.75, yt, 2.1, h, "BM25 (top-4)", fs=6.8)
    caixa(ax, 6.4, yt, wc, h, "C3", True)
    caixa(ax, 7.4, yt, wc, h, "C2", True)
    seta(ax, (2.45, yt), (4.75 - 1.05, yt))
    seta(ax, (4.75 + 1.05, yt), (6.4 - wc / 2, yt))
    seta(ax, (6.4 + wc / 2, yt), (7.4 - wc / 2, yt))
    seta(ax, (7.4, yt - h / 2), (7.4, ym + 0.575))
    linha([(3.9, ym + h / 2), (3.9, 4.85), (4.75, 4.85), (4.75, yt - h / 2)])
    ax.text(4.85, 4.95, T("consulta"), fontsize=6, color=TINTA2, ha="left", va="bottom")

    # linha de baixo: ferramentas
    caixa(ax, 10.2, yb, wc, h, "C5", True)
    caixa(ax, 12.85, yb, 3.4, h, T("Ferramentas e banco\n(consultar, cancelar, reembolsar)"), fs=5.7)
    caixa(ax, 7.6, yb, wc, h, "C3", True)
    caixa(ax, 6.5, yb, wc, h, "C2", True)
    linha([(8.9, ym - 0.575), (8.9, yb), (10.2 - wc / 2, yb)])
    ax.text(9.0, 1.95, T("chamada"), fontsize=6, color=TINTA2, ha="left", va="center")
    seta(ax, (10.2 + wc / 2, yb), (12.85 - 1.7, yb))
    linha([(12.85, yb - h / 2), (12.85, 0.3), (7.6, 0.3), (7.6, yb - h / 2)])
    ax.text(10.2, 0.22, T("retorno"), fontsize=6, color=TINTA2, ha="center", va="top")
    seta(ax, (7.6 - wc / 2, yb), (6.5 + wc / 2, yb))
    linha([(6.5, yb + h / 2), (6.5, 2.4), (7.5, 2.4), (7.5, ym - 0.575)])

    # fronteiras de confiança
    fronteira(ax, 2.95, 3.0, 2.95, 4.3, "F1", dx=0.1, dy=0.05, ha="left")
    fronteira(ax, 2.95, 5.45, 2.95, 6.75, "F2", dx=0.1, dy=0.05, ha="left")
    fronteira(ax, 9.55, 0.65, 9.55, 1.85, "F3", dx=0.1, dy=0.05, ha="left")

    # atacantes
    ax.text(1.3, 2.95, T("cliente malicioso\n(A1, A3–A5)"), ha="center", va="top", fontsize=6.3,
            color=FRONTEIRA, style="italic")
    ax.text(1.3, 6.7, T("atacante indireto (A2)"), ha="center", va="bottom", fontsize=6.3,
            color=FRONTEIRA, style="italic")

    # legenda
    lx, ly = 11.9, 6.55
    caixa(ax, lx, ly, 0.45, 0.32, "", True)
    ax.text(lx + 0.4, ly, T("controle avaliado"), va="center", fontsize=6.5)
    caixa(ax, lx, ly - 0.5, 0.45, 0.32, "")
    ax.text(lx + 0.4, ly - 0.5, T("componente do sistema"), va="center", fontsize=6.5)
    ax.plot([lx - 0.22, lx + 0.22], [ly - 1.0] * 2, linestyle=(0, (3, 2)), color=FRONTEIRA, linewidth=0.9)
    ax.text(lx + 0.4, ly - 1.0, T("fronteira de confiança"), va="center", fontsize=6.5)

    for ext in ("pdf", "png"):
        fig.savefig(pasta / f"fig1_arquitetura{sufixo}.{ext}")
    print("gravada", pasta / f"fig1_arquitetura{sufixo}.pdf")


if __name__ == "__main__":
    main()
