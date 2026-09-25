"""Gera o site estático em site/ a partir de artigos/*.md.

Uso: pip install markdown && python3 scripts/build.py
"""
import html
import pathlib
import re
import shutil

import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site"

# Preencher antes de divulgar o link (exigência LGPD: identificação do controlador e canal do titular).
CONTROLADOR = "ZeroInvest [RAZÃO SOCIAL], CNPJ [00.000.000/0000-00]"
EMAIL_PRIVACIDADE = "[email-de-privacidade@dominio]"

# Ordem de publicação (ver docs/05-linha-editorial.md)
ORDEM = ["04", "05", "06", "01", "02", "03"]

DISCLAIMER = (
    "Energia &amp; Capital é uma publicação mantida pela ZeroInvest, empresa que desenvolve projetos de energia. "
    "O conteúdo é educacional e informativo e não constitui oferta, recomendação ou solicitação de investimento "
    "em valores mobiliários. Retornos passados ou de terceiros não garantem resultados futuros."
)

CSS = """
:root{--bg:#f7f8f6;--fg:#1c2421;--muted:#5b6661;--accent:#1f7a55;--card:#fff;--line:#dde2df}
@media (prefers-color-scheme:dark){:root{--bg:#121715;--fg:#e7ece9;--muted:#9aa6a0;--accent:#4cc28f;--card:#1a211e;--line:#2b3430}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.65 system-ui,-apple-system,"Segoe UI",sans-serif}
a{color:var(--accent)}
header.top{border-bottom:1px solid var(--line)}
header.top div{max-width:720px;margin:0 auto;padding:14px 16px;display:flex;justify-content:space-between;align-items:center;gap:12px}
.brand{font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--accent);text-decoration:none}
.brand small{display:block;font-weight:500;letter-spacing:0;text-transform:none;color:var(--muted);font-size:.75rem}
main{max-width:720px;margin:0 auto;padding:40px 16px}
h1{font-size:2rem;line-height:1.2;margin:0 0 16px}
h2{font-size:1.3rem;margin:36px 0 10px}
.lead{color:var(--muted);font-size:1.1rem;margin:0 0 28px}
table{width:100%;border-collapse:collapse;font-size:.92rem;display:block;overflow-x:auto}
th,td{border-bottom:1px solid var(--line);padding:8px;text-align:left;vertical-align:top}
.cards{list-style:none;padding:0;margin:0 0 40px;display:grid;gap:12px}
.cards a{display:block;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;text-decoration:none;color:var(--fg)}
.cards a:hover{border-color:var(--accent)}
.cards strong{display:block;margin-bottom:4px}
.cards span{color:var(--muted);font-size:.92rem}
form{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:22px;margin-top:40px}
form h3{margin:0 0 6px}
form p.sub{margin:0 0 16px;color:var(--muted);font-size:.95rem}
label.field{display:block;font-weight:600;margin-bottom:6px}
input[type=text],input[type=email]{width:100%;padding:10px 12px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--fg);font:inherit;margin-bottom:14px}
.check{display:flex;gap:10px;align-items:flex-start;font-size:.88rem;color:var(--muted);margin-bottom:12px}
.check input{margin-top:5px}
button{width:100%;padding:12px;border:0;border-radius:8px;background:var(--accent);color:#fff;font:inherit;font-weight:600;cursor:pointer}
.hidden{display:none}
footer{max-width:720px;margin:0 auto;padding:24px 16px 48px;font-size:.8rem;color:var(--muted);border-top:1px solid var(--line)}
"""

FORM = """
<form name="newsletter" method="POST" action="/obrigado.html" data-netlify="true" netlify-honeypot="empresa">
  <input type="hidden" name="form-name" value="newsletter">
  <input type="hidden" name="origem" value="{origem}">
  <input type="hidden" name="versao_consentimento" value="v2-2026-09">
  <p class="hidden"><label>Não preencha: <input name="empresa"></label></p>
  <h3>Receba a Energia &amp; Capital</h3>
  <p class="sub">Análises quinzenais sobre energia como classe de ativo. Gratuito.</p>
  <label class="field" for="nome-{origem}">Nome</label>
  <input id="nome-{origem}" name="nome" type="text" autocomplete="name" required>
  <label class="field" for="email-{origem}">E-mail</label>
  <input id="email-{origem}" name="email" type="email" autocomplete="email" required>
  <label class="check"><input type="checkbox" name="consentimento_newsletter" value="sim" required>
    <span>Quero receber a newsletter Energia &amp; Capital e concordo com a <a href="/privacidade.html">Política de Privacidade</a>.</span></label>
  <label class="check"><input type="checkbox" name="consentimento_contato" value="sim">
    <span>(Opcional) Aceito ser informado(a) pela ZeroInvest, por e-mail, sobre eventuais iniciativas futuras relacionadas ao setor de energia, que seguirão a regulamentação aplicável.</span></label>
  <button type="submit">Assinar gratuitamente</button>
</form>
"""


def page(title, body, description=""):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<header class="top"><div><a class="brand" href="/">Energia &amp; Capital<small>Energia como classe de ativo</small></a></div></header>
<main>
{body}
</main>
<footer>{DISCLAIMER}<br><br><a href="/privacidade.html">Política de Privacidade</a></footer>
</body>
</html>
"""


def resumo(texto, limite=180):
    texto = re.sub(r"[*_]", "", texto)
    return texto if len(texto) <= limite else texto[:limite].rsplit(" ", 1)[0] + "…"


def load_articles():
    arts = []
    for num in ORDEM:
        path = next((ROOT / "artigos").glob(f"{num}-*.md"))
        src = path.read_text(encoding="utf-8")
        src = src.split("\n---\n")[0]  # rodapé vem do template
        title = re.search(r"^# (.+)$", src, re.M).group(1)
        first_par = next(p for p in src.split("\n\n")[1:] if p.strip() and not p.startswith("#"))
        arts.append({"slug": path.stem, "title": title, "summary": first_par.strip(), "md": src})
    return arts


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "artigos").mkdir(parents=True)
    (OUT / "style.css").write_text(CSS, encoding="utf-8")

    arts = load_articles()
    md = markdown.Markdown(extensions=["tables"])

    for a in arts:
        body = md.reset().convert(a["md"]) + FORM.format(origem=a["slug"])
        (OUT / "artigos" / f"{a['slug']}.html").write_text(
            page(f"{a['title']} | Energia & Capital", body, a["summary"][:160]), encoding="utf-8")

    cards = "\n".join(
        f'<li><a href="/artigos/{a["slug"]}.html"><strong>{html.escape(a["title"])}</strong>'
        f'<span>{html.escape(resumo(a["summary"]))}</span></a></li>'
        for a in arts)
    home = f"""<h1>Energia como classe de ativo</h1>
<p class="lead">Análises sobre como ativos de energia geram caixa, como o retorno se forma e quais riscos pesam — para quem pensa como investidor.</p>
<ul class="cards">
{cards}
</ul>
{FORM.format(origem="home")}"""
    (OUT / "index.html").write_text(
        page("Energia & Capital", home, "Análises sobre infraestrutura de energia sob a ótica do investidor."), encoding="utf-8")

    (OUT / "obrigado.html").write_text(page("Inscrição confirmada | Energia & Capital",
        '<h1>Inscrição recebida</h1><p class="lead">Obrigado. Você receberá a próxima edição da Energia &amp; Capital no seu e-mail.</p>'
        '<p><a href="/">Voltar aos artigos</a></p>'), encoding="utf-8")

    privacidade = (ROOT / "landing" / "privacidade.md").read_text(encoding="utf-8")
    privacidade = privacidade.replace("{CONTROLADOR}", CONTROLADOR).replace("{EMAIL}", EMAIL_PRIVACIDADE)
    (OUT / "privacidade.html").write_text(page("Política de Privacidade | Energia & Capital",
        md.reset().convert(privacidade)), encoding="utf-8")

    pendentes = [p for p in OUT.rglob("*.html") if "[" in p.read_text() and re.search(r"\[(RAZÃO|00\.|email-|DADO)", p.read_text())]
    for p in pendentes:
        print(f"ATENÇÃO: placeholder pendente em {p.relative_to(ROOT)}")
    print(f"Site gerado em {OUT.relative_to(ROOT)}/ ({len(arts)} artigos)")


if __name__ == "__main__":
    main()
