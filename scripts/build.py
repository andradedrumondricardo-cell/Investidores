"""Gera o site estático em site/ a partir de artigos/*.md.

Uso: pip install -r requirements.txt && python3 scripts/build.py
"""
import datetime
import html
import json
import os
import pathlib
import re
import shutil
import subprocess

import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site"

# Preencher antes de divulgar o link (exigência LGPD: identificação do controlador e canal do titular).
CONTROLADOR = "ZeroInvest [RAZÃO SOCIAL], CNPJ [00.000.000/0000-00]"
EMAIL_PRIVACIDADE = "[email-de-privacidade@dominio]"

# Endereço público do site: o Netlify define URL no build (domínio principal). Localmente, defina SITE_URL.
SITE = (os.environ.get("SITE_URL") or os.environ.get("URL") or "https://energiaecapital.com.br").rstrip("/")
# Código de verificação do Google Search Console (opcional; método "Tag HTML"). Definir como variável no Netlify.
GOOGLE_VERIFICATION = os.environ.get("GOOGLE_SITE_VERIFICATION", "")

# Link do CANAL do WhatsApp (somente leitura), não de grupo. Vazio = links não aparecem no site.
WHATSAPP_CANAL_URL = ""

# Metadados de cada artigo: data de publicação, seção (chapéu), ilustração (ver ILUSTRACOES) e foto opcional.
# Novo artigo: acrescente uma linha com "publicado" na data de hoje (AAAA-MM-DD) e "seo" (título para o Google,
# até ~60 caracteres, com a palavra-chave principal no início).
ARTIGOS = {
    "01": {"seo": "Por que contratos de energia duram 10, 15 ou 20 anos", "publicado": "2026-09-25", "secao": "Entenda", "ilustracao": "solar", "foto": "campo-solar", "alt": "Usina solar instalada em antigo aeródromo em Neuhardenberg, Alemanha"},
    "02": {"seo": "Geração distribuída: como a energia solar vira desconto na conta", "publicado": "2026-09-25", "secao": "Solar", "ilustracao": "casa", "foto": "telhado-solar", "alt": "Casa com painéis solares no telhado"},
    "03": {"seo": "Checklist: como avaliar os riscos de um projeto de energia", "publicado": "2026-09-25", "secao": "Checklist", "ilustracao": "lampada"},
    "04": {"seo": "Energia como classe de ativo: por que investidores gostam", "publicado": "2026-09-25", "secao": "Investidor", "ilustracao": "eolica", "foto": "parque-eolico", "alt": "Parque eólico da Copel"},
    "05": {"seo": "Como se forma o retorno (TIR) de um projeto de energia", "publicado": "2026-09-25", "secao": "Investidor", "ilustracao": "grafico"},
    "06": {"seo": "Investimento em infraestrutura de energia: caminhos regulados", "publicado": "2026-09-25", "secao": "Investidor", "ilustracao": "torre"},
    "07": {"seo": "Bandeiras tarifárias: o que significa cada cor da conta de luz", "publicado": "2026-10-03", "secao": "Conta de luz", "ilustracao": "bandeiras"},
    "08": {"seo": "Curtailment: por que usinas solares e eólicas geram menos", "publicado": "2026-10-03", "secao": "Rede", "ilustracao": "curtailment", "foto": "linhas-transmissao", "alt": "Torres e linhas de transmissão de energia"},
    "09": {"seo": "Usina solar flutuante: como funciona e vantagens", "publicado": "2026-10-03", "secao": "Curiosidade", "ilustracao": "flutuante", "foto": "solar-flutuante", "alt": "Usina fotovoltaica flutuante Araucária, em São Paulo"},
    "10": {"seo": "Baterias na rede elétrica: o que muda com o armazenamento", "publicado": "2026-10-03", "secao": "Tecnologia", "ilustracao": "bateria", "foto": "baterias", "alt": "Sistema de armazenamento em baterias ao lado de usina solar na Califórnia, EUA"},
    "11": {"seo": "Mercado livre de energia: quem pode migrar e como funciona", "publicado": "2026-10-03", "secao": "Mercado livre", "ilustracao": "mercado"},
    "12": {"seo": "Glossário do setor elétrico: 20 termos para entender energia", "publicado": "2026-10-03", "secao": "Glossário", "ilustracao": "glossario"},
    "13": {"seo": "IA e data centers: o desafio de energia no Brasil", "publicado": "2026-10-03", "secao": "IA e energia", "ilustracao": "datacenter", "foto": "data-center", "alt": "Racks de servidores iluminados em um data center"},
}

# Composição da home. Seções sem artigos não aparecem.
DESTAQUE = "13"
ULTIMAS = ["07", "08", "11", "10"]
SECOES = [
    {"id": "na-pratica", "titulo": "Na prática", "artigos": ["11", "02", "03", "01"],
     "seo": "Guias práticos de energia: conta de luz, solar e mercado livre",
     "descricao": "Guias práticos para entender a conta de luz, a energia solar no telhado, o mercado livre e os contratos do setor elétrico."},
    {"id": "investidor", "titulo": "Investidor", "artigos": ["04", "05", "06", "08", "13"],
     "seo": "Energia para investidores: análises do setor elétrico",
     "descricao": "Análises sobre energia como classe de ativo: como os projetos geram caixa, como o retorno se forma e quais riscos pesam."},
    {"id": "variedades", "titulo": "Variedades", "artigos": ["09", "12", "10", "07"],
     "seo": "Curiosidades e tecnologia em energia: solar flutuante, baterias",
     "descricao": "Curiosidades, tecnologia e glossário do setor de energia: usinas solares flutuantes, baterias, bandeiras tarifárias e mais."},
]
EM_PAUTA = [("IA e data centers", "13"), ("Bandeiras tarifárias", "07"), ("Lei 14.300", "02"), ("Curtailment", "08"),
            ("Mercado livre", "11"), ("Baterias", "10")]

CREDITOS = json.loads((ROOT / "imagens" / "creditos.json").read_text(encoding="utf-8"))


def credito(foto):
    c = CREDITOS.get(foto)
    if not c:
        return ""
    return (f'Foto: <a href="{html.escape(c["pagina"])}" rel="noopener">{html.escape(c["autor"])}</a> / Wikimedia Commons · '
            f'<a href="{html.escape(c["licenca_url"] or c["pagina"])}" rel="noopener">{html.escape(c["licenca"])}</a> · recortada')


DISCLAIMER = (
    "Energia &amp; Capital é uma publicação mantida pela ZeroInvest, empresa que desenvolve projetos de energia. "
    "O conteúdo é educacional e informativo e não constitui oferta, recomendação ou solicitação de investimento "
    "em valores mobiliários. Retornos passados ou de terceiros não garantem resultados futuros."
)

SIMBOLO = ('<svg width="{s}" height="{s}" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="{bg}"/>'
           '<circle cx="32" cy="32" r="19" fill="{fg}"/><path d="M36 9 L21 36 H31 L27 55 L44 26 H34 Z" fill="{bg}"/></svg>')


def simbolo(s, invertido=False):
    return SIMBOLO.format(s=s, bg="#F5C400" if invertido else "#0E1B17", fg="#0E1B17" if invertido else "#F5C400")


ICONE_WA = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#F5C400" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.4 8.4 0 1 1 21 11.5z"/></svg>')

_SVG = '<svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true">{}</svg>'
ILUSTRACOES = {
    "solar": _SVG.format(
        '<rect width="400" height="300" fill="#DDEBE4"/><circle cx="320" cy="72" r="40" fill="#F5C400"/>'
        '<path d="M0 190 Q100 160 200 185 T400 172 V300 H0 Z" fill="#0B6B45"/>'
        '<g fill="#0E1B17" stroke="#3E6B5C" stroke-width="1.5"><path d="M20 215 L120 215 L135 190 L35 190 Z"/>'
        '<path d="M150 215 L250 215 L265 190 L165 190 Z"/><path d="M280 215 L380 215 L395 190 L295 190 Z"/>'
        '<path d="M5 265 L115 265 L132 235 L22 235 Z"/><path d="M145 265 L255 265 L272 235 L162 235 Z"/>'
        '<path d="M285 265 L395 265 L412 235 L302 235 Z"/></g>'),
    "casa": _SVG.format(
        '<rect width="400" height="300" fill="#FBE7A1"/><circle cx="320" cy="70" r="34" fill="#F5C400" stroke="#0E1B17" stroke-width="4"/>'
        '<path d="M90 170 L200 90 L310 170 V250 H90 Z" fill="#FFFFFF" stroke="#0E1B17" stroke-width="5"/>'
        '<path d="M200 90 L310 170 L262 170 L176 107 Z" fill="#0E1B17"/><rect x="180" y="190" width="40" height="60" fill="#0E1B17"/>'),
    "lampada": _SVG.format(
        '<rect width="400" height="300" fill="#DDEBE4"/>'
        '<path d="M200 60 a60 60 0 0 1 38 106 v30 h-76 v-30 a60 60 0 0 1 38 -106 z" fill="#F5C400" stroke="#0E1B17" stroke-width="5"/>'
        '<path d="M168 216 H232 M176 236 H224" stroke="#0E1B17" stroke-width="5" stroke-linecap="round"/>'),
    "eolica": _SVG.format(
        '<rect width="400" height="300" fill="#0B6B45"/><g stroke="#FFFFFF" stroke-width="5" fill="none" stroke-linecap="round">'
        '<path d="M110 260 V120 M110 120 L70 95 M110 120 L150 98 M110 120 L112 72"/>'
        '<path d="M270 260 V90 M270 90 L228 66 M270 90 L312 68 M270 90 L272 40"/></g>'
        '<path d="M0 250 Q120 220 220 245 T400 235 V300 H0 Z" fill="#0E1B17"/><circle cx="335" cy="200" r="26" fill="#F5C400"/>'),
    "grafico": _SVG.format(
        '<rect width="400" height="300" fill="#F3F4EF"/><g fill="#0B6B45"><rect x="70" y="180" width="44" height="80"/>'
        '<rect x="140" y="150" width="44" height="110"/><rect x="210" y="115" width="44" height="145"/><rect x="280" y="80" width="44" height="180"/></g>'
        '<path d="M60 170 L160 130 L230 100 L340 55" stroke="#0E1B17" stroke-width="6" fill="none" stroke-linecap="round"/>'
        '<circle cx="340" cy="55" r="12" fill="#F5C400" stroke="#0E1B17" stroke-width="4"/>'),
    "torre": _SVG.format(
        '<rect width="400" height="300" fill="#0E1B17"/><g stroke="#F5C400" stroke-width="5" fill="none" stroke-linecap="round">'
        '<path d="M200 40 L150 260 M200 40 L250 260 M162 205 H238 M172 160 H228 M120 100 H280 M155 245 L235 165 M245 245 L165 165"/>'
        '<path d="M120 100 L100 120 M280 100 L300 120"/></g>'),
    "bandeiras": _SVG.format(
        '<rect width="400" height="300" fill="#F3F4EF"/><rect x="80" y="80" width="70" height="140" rx="10" fill="#0B6B45"/>'
        '<rect x="165" y="80" width="70" height="140" rx="10" fill="#F5C400"/><rect x="250" y="80" width="70" height="140" rx="10" fill="#C2410C"/>'
        '<path d="M80 240 H320" stroke="#0E1B17" stroke-width="5" stroke-linecap="round"/>'),
    "curtailment": _SVG.format(
        '<rect width="400" height="300" fill="#FBE7A1"/><circle cx="90" cy="70" r="34" fill="#F5C400" stroke="#0E1B17" stroke-width="4"/>'
        '<g fill="#0E1B17"><path d="M40 250 L170 250 L190 215 L60 215 Z"/><path d="M40 200 L170 200 L190 165 L60 165 Z"/></g>'
        '<g stroke="#0E1B17" stroke-width="10" stroke-linecap="round" fill="none"><path d="M300 70 V210"/><path d="M255 170 L300 215 L345 170"/></g>'),
    "flutuante": _SVG.format(
        '<rect width="400" height="300" fill="#BFD9E8"/><circle cx="330" cy="70" r="34" fill="#F5C400"/>'
        '<path d="M0 150 Q50 140 100 150 T200 150 T300 150 T400 150" stroke="#FFFFFF" stroke-width="4" fill="none"/>'
        '<g fill="#0E1B17"><path d="M40 200 L150 200 L170 180 L60 180 Z"/><path d="M175 200 L285 200 L305 180 L195 180 Z"/>'
        '<path d="M30 250 L150 250 L172 226 L52 226 Z"/><path d="M180 250 L300 250 L322 226 L202 226 Z"/></g>'),
    "bateria": _SVG.format(
        '<rect width="400" height="300" fill="#0B6B45"/><rect x="120" y="95" width="150" height="110" rx="14" fill="none" stroke="#FFFFFF" stroke-width="7"/>'
        '<rect x="270" y="128" width="16" height="44" rx="4" fill="#FFFFFF"/><rect x="134" y="109" width="84" height="82" rx="5" fill="#F5C400"/>'),
    "mercado": _SVG.format(
        '<rect width="400" height="300" fill="#DDEBE4"/><g fill="none" stroke="#0E1B17" stroke-width="8" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M90 120 H290 M250 80 L290 120 L250 160"/><path d="M310 190 H110 M150 150 L110 190 L150 230"/></g>'
        '<circle cx="200" cy="155" r="18" fill="#F5C400" stroke="#0E1B17" stroke-width="4"/>'),
    "datacenter": _SVG.format(
        '<rect width="400" height="300" fill="#0E1B17"/>'
        '<g fill="#1F332C" stroke="#3E6B5C" stroke-width="2"><rect x="70" y="60" width="70" height="180" rx="6"/>'
        '<rect x="165" y="60" width="70" height="180" rx="6"/><rect x="260" y="60" width="70" height="180" rx="6"/></g>'
        '<g fill="#F5C400"><rect x="82" y="80" width="46" height="6" rx="3"/><rect x="82" y="100" width="46" height="6" rx="3"/>'
        '<rect x="82" y="120" width="30" height="6" rx="3"/><rect x="177" y="80" width="46" height="6" rx="3"/>'
        '<rect x="177" y="100" width="30" height="6" rx="3"/><rect x="272" y="80" width="46" height="6" rx="3"/>'
        '<rect x="272" y="100" width="46" height="6" rx="3"/><rect x="272" y="120" width="46" height="6" rx="3"/></g>'
        '<circle cx="200" cy="190" r="34" fill="#F5C400"/><path d="M204 162 L186 194 H198 L194 218 L214 184 H202 Z" fill="#0E1B17"/>'),
    "glossario": _SVG.format(
        '<rect width="400" height="300" fill="#F5C400"/><text x="200" y="175" text-anchor="middle" '
        'font-family="Archivo, sans-serif" font-weight="900" font-size="58" fill="#0E1B17">kWh → MW</text>'),
}

_FONTS_URL = ("https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900"
              "&amp;family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400&amp;display=swap")
# Fontes carregadas sem bloquear a renderização (media=print + onload); fallback para quem não roda JS.
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         f'<link rel="stylesheet" href="{_FONTS_URL}" media="print" onload="this.media=\'all\'">'
         f'<noscript><link rel="stylesheet" href="{_FONTS_URL}"></noscript>')

CSS = """
:root{--ink:#0E1B17;--sol:#F5C400;--verde:#0B6B45;--papel:#F3F4EF;--linha:#DDE2DF;--muted:#4A5752;--texto:#1C2421}
*{box-sizing:border-box}
html{color-scheme:light}
body{margin:0;background:#fff;color:var(--ink);font:16px/1.5 'Archivo',system-ui,sans-serif}
a{color:inherit;text-decoration:none}
a:hover{color:var(--verde)}
.wrap{max-width:1240px;margin:0 auto;padding:0 24px}
.cond{font-stretch:80%;font-weight:900;letter-spacing:-.01em}
.kicker{font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.08em;color:var(--verde)}
.serif{font-family:'Newsreader',Georgia,serif}
svg{display:block}
.thumb{border-radius:8px;overflow:hidden;background:var(--papel)}
.thumb svg{width:100%;height:100%}
.thumb img{width:100%;height:100%;object-fit:cover;display:block}
.credito{margin:-20px 0 28px;font-size:12px;color:var(--muted)}
.credito a{color:var(--muted);text-decoration:underline}

/* topo */
.topbar{background:var(--ink);color:#fff;font-size:13px}
.topbar .wrap{display:flex;flex-wrap:wrap;gap:12px;justify-content:space-between;align-items:center;padding-top:8px;padding-bottom:8px}
.topbar .data{color:#C9D3CE;display:inline-block}
.topbar .data::first-letter{text-transform:uppercase}
.topbar nav{display:flex;gap:20px;align-items:center;flex-wrap:wrap}
.topbar a{display:inline-flex;gap:6px;align-items:center;color:#fff}
.btn-sol{background:var(--sol);color:var(--ink)!important;font-weight:800;padding:7px 14px;border-radius:6px}
.btn-sol:hover{filter:brightness(.95)}
.masthead{border-bottom:1px solid var(--linha)}
.masthead .marca{display:flex;flex-direction:column;align-items:center;gap:10px;padding:28px 0 20px}
.logo{display:flex;align-items:center;gap:16px;color:var(--ink)}
.logo:hover{color:var(--ink)}
.logo .nome{display:flex;flex-direction:column;line-height:.9;font-size:46px}
.amp{background:var(--sol);padding:0 4px}
.slogan{margin:0;font-family:'Newsreader',serif;font-style:italic;font-size:17px;color:var(--muted)}
.secoes{border-top:1px solid var(--linha)}
.secoes .wrap{display:flex;flex-wrap:wrap;justify-content:center;gap:0 28px;font-weight:700;font-size:14px;text-transform:uppercase;letter-spacing:.06em}
.secoes a{padding:14px 0;border-bottom:3px solid transparent;white-space:nowrap}
.secoes a:hover,.secoes a.ativo{border-bottom-color:var(--sol);color:var(--ink)}
.compacto .wrap{display:flex;flex-wrap:wrap;gap:12px 24px;justify-content:space-between;align-items:center;padding-top:14px;padding-bottom:14px}
.logo-h{display:flex;align-items:center;gap:10px;font-size:26px;color:var(--ink)}
.logo-h .amp{padding:0 3px;margin:0 2px}
.compacto nav{display:flex;flex-wrap:wrap;gap:4px 20px;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.pauta{background:var(--papel);border-bottom:1px solid var(--linha)}
.pauta .wrap{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;font-size:14px;padding-top:10px;padding-bottom:10px}
.pauta .tag{font-weight:800;text-transform:uppercase;letter-spacing:.08em;font-size:12px;background:var(--ink);color:var(--sol);padding:4px 8px;border-radius:4px}
.pauta a:hover{text-decoration:underline}

/* home */
.destaque{display:flex;flex-wrap:wrap;gap:32px;padding:32px 0 40px;border-bottom:1px solid var(--linha)}
.destaque .principal{flex:999 1 560px;min-width:0}
.destaque .principal .thumb{aspect-ratio:16/9;border-radius:10px}
.destaque h1{margin:8px 0 0;font-size:48px;line-height:1.02}
.destaque .linha-fina{margin:14px 0 0;font-size:20px;line-height:1.45;color:#2D3934}
.destaque .meta{margin:12px 0 0;font-size:13px;color:var(--muted)}
.destaque .principal .kicker{display:block;margin-top:18px}
.lateral{flex:1 1 320px;min-width:0;display:flex;flex-direction:column}
.rotulo{margin:0 0 4px;font-size:14px;font-weight:800;text-transform:uppercase;letter-spacing:.08em;border-top:4px solid var(--ink);padding-top:10px}
.item-lista{display:flex;gap:14px;padding:16px 0;border-bottom:1px solid var(--linha)}
.item-lista:last-child{border-bottom:0}
.item-lista .thumb{width:96px;height:72px;flex:none;border-radius:6px}
.item-lista span{display:flex;flex-direction:column;gap:4px}
.item-lista strong{font-size:18px;line-height:1.15;font-stretch:85%;font-weight:800}
.secao{padding:40px 0;border-bottom:1px solid var(--linha)}
.secao:last-of-type{border-bottom:0}
.secao-topo{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:16px;margin-bottom:20px;border-top:4px solid var(--ink);padding-top:10px}
.secao-topo h2{margin:0;font-size:28px;text-transform:uppercase}
.grade{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:24px}
.card{display:flex;flex-direction:column;gap:10px}
.card .thumb{aspect-ratio:4/3}
.card strong{font-size:21px;line-height:1.15;font-stretch:85%;font-weight:800}
.dupla{display:flex;flex-wrap:wrap;gap:32px}
.card-grande{flex:2 1 480px;min-width:0;display:flex;flex-wrap:wrap;gap:20px;background:var(--papel);border-radius:10px;padding:20px}
.card-grande .thumb{flex:1 1 220px;aspect-ratio:4/3}
.card-grande span.txt{flex:1 1 220px;display:flex;flex-direction:column;gap:10px}
.card-grande strong{font-size:28px;line-height:1.05}
.card-grande .serif{font-size:17px;line-height:1.45;color:#2D3934}
.lista-texto{flex:1 1 300px;min-width:0;display:flex;flex-direction:column}
.lista-texto a{display:flex;flex-direction:column;gap:6px;padding:18px 0;border-bottom:1px solid var(--linha)}
.lista-texto a:first-child{padding-top:0}
.lista-texto a:last-child{border-bottom:0}
.lista-texto strong{font-size:21px;line-height:1.15;font-stretch:85%;font-weight:800}

/* artigo */
.artigo-layout{display:flex;flex-wrap:wrap;gap:48px;padding:32px 0 56px}
.artigo{flex:999 1 600px;min-width:0}
.trilha{margin:0 0 12px;font-size:13px;color:var(--muted)}
.trilha a{color:var(--verde)}
.artigo h1{margin:8px 0 0;font-size:52px;line-height:1.02}
.artigo .linha-fina{margin:16px 0 0;font-size:22px;line-height:1.45;color:#2D3934}
.byline{display:flex;flex-wrap:wrap;gap:8px 16px;margin:20px 0 24px;padding:14px 0;border-top:1px solid var(--linha);border-bottom:1px solid var(--linha);font-size:14px;color:var(--muted)}
.byline b{color:var(--ink)}
.artigo .capa{aspect-ratio:16/9;border-radius:10px;margin-bottom:28px}
.corpo{font-family:'Newsreader',Georgia,serif;font-size:20px;line-height:1.65;color:var(--texto)}
.corpo h2{font-family:'Archivo',sans-serif;font-size:28px;font-weight:900;font-stretch:85%;line-height:1.1;margin:36px 0 10px;color:var(--ink)}
.corpo a{color:var(--verde);text-decoration:underline}
.corpo table{width:100%;border-collapse:collapse;font:15px/1.45 'Archivo',sans-serif;display:block;overflow-x:auto;margin:16px 0}
.corpo th,.corpo td{border-bottom:1px solid var(--linha);padding:10px 8px;text-align:left;vertical-align:top}
.corpo th{background:var(--papel)}
.aviso{margin-top:32px;padding:18px 20px;border:1px solid var(--linha);border-radius:10px;font-size:13px;line-height:1.6;color:var(--muted)}
.cta-lateral{background:var(--ink);color:#fff;border-radius:12px;padding:24px;display:flex;flex-direction:column;gap:14px}
.cta-lateral strong{font-size:24px;line-height:1.05}
.cta-lateral .btn-sol{text-align:center;padding:12px}
.mais-lidas a{display:flex;gap:14px;padding:14px 0;border-bottom:1px solid var(--linha)}
.mais-lidas a:last-child{border-bottom:0}
.mais-lidas .n{font-size:36px;font-weight:900;font-stretch:75%;color:var(--sol);-webkit-text-stroke:1px var(--ink);line-height:1}
.mais-lidas strong{font-size:17px;line-height:1.2;font-stretch:85%;font-weight:800}
.pagina-simples{max-width:760px;padding:40px 24px 56px}
.pagina-simples h1{font-size:44px;line-height:1.05;margin:0 0 16px}

/* newsletter */
.news{background:var(--ink);color:#fff;margin-top:16px}
.news .wrap{display:flex;flex-wrap:wrap;gap:40px;align-items:center;padding-top:48px;padding-bottom:48px}
.news .chamada{flex:1 1 380px;display:flex;flex-direction:column;gap:12px}
.news .chamada .kicker{color:var(--sol)}
.news h2{margin:0;font-size:40px;line-height:1.02}
.news .chamada p{margin:0;font-size:18px;line-height:1.45;color:#C9D3CE}
.news form{flex:1 1 380px;display:flex;flex-direction:column;gap:12px}
.news .campos{display:flex;flex-wrap:wrap;gap:10px}
.news label.campo{display:flex;flex-direction:column;gap:6px;font-size:13px;font-weight:700}
.news label.campo:first-child{flex:1 1 160px}
.news label.campo:last-child{flex:2 1 220px}
.news input[type=text],.news input[type=email]{padding:13px 14px;border-radius:8px;border:0;font:inherit;font-size:16px;font-weight:400;color:var(--ink)}
.news .check{display:flex;gap:10px;align-items:flex-start;font-size:13px;color:#C9D3CE}
.news .check input{margin-top:3px}
.news .check a{color:#fff;text-decoration:underline}
.news button{min-height:48px;border:0;border-radius:8px;background:var(--sol);color:var(--ink);font:inherit;font-size:16px;font-weight:800;cursor:pointer}
.news .wa{display:inline-flex;gap:8px;align-items:center;color:#fff;font-size:14px;font-weight:700;margin-top:4px}
.hidden{display:none}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.secao-topo a{font-size:14px;font-weight:700}
.secao-topo a:hover{text-decoration:underline}
.hub-topo{padding:32px 0 8px}
.hub-topo h1{margin:8px 0 0;font-size:48px;line-height:1.02}
.hub-topo p{margin:12px 0 0;font-size:20px;line-height:1.45;color:#2D3934;max-width:760px}
.hub-topo .trilha{margin:0;font-size:13px;color:var(--muted)}
.card .serif{font-size:16px;line-height:1.45;color:#2D3934}
.card time,.meta-card{font-size:13px;color:var(--muted)}
footer.rodape{background:var(--ink);border-top:1px solid #2B3430;color:#9AA6A0}
footer.rodape .wrap{display:flex;flex-wrap:wrap;gap:24px;justify-content:space-between;padding-top:28px;padding-bottom:40px;font-size:13px;line-height:1.6}
footer.rodape .assinatura{display:flex;align-items:center;gap:10px;color:#fff;font-size:18px}
footer.rodape p{margin:0;flex:1 1 520px;max-width:760px}
footer.rodape a{color:#fff;text-decoration:underline}

@media (max-width:640px){
  .logo .nome{font-size:34px}.logo svg{width:48px;height:48px}
  .destaque h1{font-size:34px}.artigo h1{font-size:36px}
  .destaque .linha-fina,.artigo .linha-fina{font-size:18px}
  .corpo{font-size:18px}.news h2{font-size:32px}
  .secoes .wrap{justify-content:flex-start;gap:0 18px;overflow-x:auto;flex-wrap:nowrap}
}
"""

FORM = """
<section class="news" id="newsletter">
  <div class="wrap">
    <div class="chamada">
      <span class="kicker">Newsletter quinzenal · grátis</span>
      <h2 class="cond">O essencial da energia, direto no seu e-mail</h2>
      <p class="serif">Notícias, guias práticos e análises do setor, em linguagem direta.</p>
    </div>
    <form name="newsletter" method="POST" action="/obrigado/" data-netlify="true" netlify-honeypot="empresa">
      <input type="hidden" name="form-name" value="newsletter">
      <input type="hidden" name="origem" value="{origem}">
      <input type="hidden" name="versao_consentimento" value="v2-2026-09">
      <p class="hidden"><label>Não preencha: <input name="empresa"></label></p>
      <div class="campos">
        <label class="campo">Nome<input name="nome" type="text" autocomplete="name" required></label>
        <label class="campo">E-mail<input name="email" type="email" autocomplete="email" required></label>
      </div>
      <label class="check"><input type="checkbox" name="consentimento_newsletter" value="sim" required>
        <span>Quero receber a newsletter Energia &amp; Capital e concordo com a <a href="/privacidade/">Política de Privacidade</a>.</span></label>
      <label class="check"><input type="checkbox" name="consentimento_contato" value="sim">
        <span>(Opcional) Aceito ser informado(a) pela ZeroInvest, por e-mail, sobre eventuais iniciativas futuras relacionadas ao setor de energia, que seguirão a regulamentação aplicável.</span></label>
      <button type="submit">Assinar grátis</button>
      {whatsapp}
    </form>
  </div>
</section>
"""


def link_whatsapp(classe, texto):
    if not WHATSAPP_CANAL_URL:
        return ""
    return (f'<a class="{classe}" href="{html.escape(WHATSAPP_CANAL_URL)}" target="_blank" rel="noopener">'
            f'{ICONE_WA} {texto}</a>')




ATIVO = ' class="ativo"'


def cabecalho(completo, secoes_home, ativo=""):
    data = ('<span class="data" id="hoje"></span>'
            '<script>try{document.getElementById("hoje").textContent=new Date().toLocaleDateString("pt-BR",'
            '{weekday:"long",day:"numeric",month:"long",year:"numeric"})}catch(e){}</script>')
    topo = (f'<div class="topbar"><div class="wrap">{data}<nav aria-label="Atalhos">'
            f'{link_whatsapp("", "Canal no WhatsApp")}<a class="btn-sol" href="#newsletter">Assine grátis</a></nav></div></div>')
    links = "".join(f'<a{ATIVO if s["id"] == ativo else ""} href="/{s["id"]}/">{html.escape(s["titulo"])}</a>'
                    for s in secoes_home)
    if completo:
        return topo + f"""
<header class="masthead">
  <div class="wrap marca">
    <a class="logo" href="/" aria-label="Energia &amp; Capital — página inicial">{simbolo(64)}
      <span class="nome cond"><span>ENERGIA</span><span><span class="amp">&amp;</span>CAPITAL</span></span></a>
    <p class="slogan">Notícias, guias e análises sobre energia no Brasil</p>
  </div>
  <nav class="secoes" aria-label="Seções"><div class="wrap"><a class="ativo" href="/">Início</a>{links}<a href="/sobre/">Sobre</a></div></nav>
</header>"""
    return topo + f"""
<header class="masthead compacto">
  <div class="wrap">
    <a class="logo-h cond" href="/" aria-label="Energia &amp; Capital — página inicial">{simbolo(40)}<span>ENERGIA<span class="amp">&amp;</span>CAPITAL</span></a>
    <nav aria-label="Seções"><a href="/">Início</a>{links}<a href="/sobre/">Sobre</a></nav>
  </div>
</header>"""


def rodape():
    return f"""
<footer class="rodape"><div class="wrap">
  <span class="assinatura cond">{simbolo(32, invertido=True)} ENERGIA &amp; CAPITAL</span>
  <p>{DISCLAIMER} <a href="/sobre/">Sobre a publicação</a> · <a href="/privacidade/">Política de Privacidade</a> ·
  <a href="/creditos/">Créditos das imagens</a> · <a href="/feed.xml">RSS</a></p>
</div></footer>"""


MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto",
         "setembro", "outubro", "novembro", "dezembro"]


def git_datas(path):
    """(primeira, última) data de commit do arquivo, em ISO 8601; None se não houver histórico."""
    try:
        out = subprocess.run(["git", "log", "--follow", "--format=%aI", "--", str(path)], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.split()
        return (out[-1], out[0]) if out else (None, None)
    except (OSError, subprocess.CalledProcessError):
        return (None, None)


def data_br(iso):
    d = datetime.date.fromisoformat(iso[:10])
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def absoluto(caminho):
    return f"{SITE}{caminho}"


ORG = {"@type": "Organization", "name": "Energia & Capital", "url": None,
       "logo": {"@type": "ImageObject", "url": None, "width": 512, "height": 512}}


def org():
    o = json.loads(json.dumps(ORG))
    o["url"] = absoluto("/")
    o["logo"]["url"] = absoluto("/img/logo.png")
    return o


def page(title, body, description, secoes_home, completo=False, origem="pagina", caminho="/",
         imagem="/img/og-padrao.png", tipo="website", jsonld=None, indexar=True, ativo=""):
    extras = [f'<link rel="canonical" href="{absoluto(caminho)}">',
              f'<meta property="og:url" content="{absoluto(caminho)}">',
              f'<meta property="og:type" content="{tipo}">',
              '<meta property="og:site_name" content="Energia &amp; Capital">',
              '<meta property="og:locale" content="pt_BR">',
              f'<meta property="og:image" content="{absoluto(imagem)}">',
              f'<meta property="og:image:width" content="{1200 if imagem.endswith(".png") else 1600}">',
              f'<meta property="og:image:height" content="{630 if imagem.endswith(".png") else 900}">',
              '<meta name="twitter:card" content="summary_large_image">',
              '<meta name="robots" content="' + ("index, follow, max-image-preview:large, max-snippet:-1" if indexar else "noindex, follow") + '">']
    if GOOGLE_VERIFICATION and caminho == "/":
        extras.append(f'<meta name="google-site-verification" content="{html.escape(GOOGLE_VERIFICATION)}">')
    for bloco in (jsonld if isinstance(jsonld, list) else [jsonld] if jsonld else []):
        extras.append('<script type="application/ld+json">' + json.dumps(bloco, ensure_ascii=False).replace("</", "<\\/") + "</script>")
    extras = "\n".join(extras)
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
{extras}
<meta name="theme-color" content="#0E1B17">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/img/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="Energia &amp; Capital" href="/feed.xml">
{FONTS}
<style>{CSS}</style>
</head>
<body>
{cabecalho(completo, secoes_home, ativo)}
{body}
{FORM.format(origem=origem, whatsapp=link_whatsapp("wa", "Prefere WhatsApp? Siga o canal Energia &amp; Capital"))}
{rodape()}
</body>
</html>
"""


def titulo(t):
    """Acrescenta a marca só se o título couber no limite exibido pelo Google (~65 caracteres)."""
    completo = f"{t} | Energia & Capital"
    return completo if len(completo) <= 65 else t


def resumo(texto, limite=180):
    texto = re.sub(r"[*_]", "", texto)
    return texto if len(texto) <= limite else texto[:limite].rsplit(" ", 1)[0] + "…"


def load_articles():
    arts = {}
    for num, meta in ARTIGOS.items():
        path = next((ROOT / "artigos").glob(f"{num}-*.md"))
        src = path.read_text(encoding="utf-8").split("\n---\n")[0]  # rodapé vem do template
        title = re.search(r"^# (.+)$", src, re.M).group(1)
        blocos = [b for b in src.split("\n\n") if b.strip()]
        i = next(i for i, b in enumerate(blocos) if not b.startswith("#"))
        corpo = "\n\n".join(blocos[i + 1:])
        palavras = len(re.findall(r"\w+", src))
        atualizado = git_datas(path)[1] or meta["publicado"]
        arts[num] = {
            "num": num, "slug": re.sub(r"^\d+-", "", path.stem), "arquivo": path.stem, "title": title,
            "summary": blocos[i].strip(), "corpo": corpo, "palavras": palavras,
            "leitura": max(1, round(palavras / 200)), "atualizado": max(atualizado[:10], meta["publicado"]), **meta,
        }
    return arts


def url(a):
    return f"/artigos/{a['slug']}/"


def imagem_og(a):
    return f"/img/{a['foto']}.jpg" if a.get("foto") else "/img/og-padrao.png"


def thumb(a, classe="thumb", grande=False):
    if a.get("foto"):
        pasta = "img" if grande else "img/thumb"
        carga = 'fetchpriority="high"' if grande else 'loading="lazy"'
        fontes = (f'/img/thumb/{a["foto"]}.webp 640w, /img/{a["foto"]}.webp 1600w" sizes="(max-width: 700px) 100vw, 820px'
                  if grande else f'/img/thumb/{a["foto"]}.webp')
        return (f'<div class="{classe}"><picture><source type="image/webp" srcset="{fontes}">'
                f'<img src="/{pasta}/{a["foto"]}.jpg" alt="{html.escape(a["alt"])}" {carga} decoding="async" '
                f'width="1600" height="900"></picture></div>')
    return f'<div class="{classe}">{ILUSTRACOES[a["ilustracao"]]}</div>'


def card(a, com_resumo=False):
    extra = f'<span class="serif">{html.escape(resumo(a["summary"], 140))}</span>' if com_resumo else ""
    return (f'<a class="card" href="{url(a)}">{thumb(a)}<span class="kicker">{a["secao"]}</span>'
            f'<strong>{html.escape(a["title"])}</strong>{extra}'
            f'<time datetime="{a["publicado"]}">{data_br(a["publicado"])}</time></a>')


def home(arts, secoes):
    d = arts[DESTAQUE]
    ultimas = "".join(
        f'<a class="item-lista" href="{url(a)}">{thumb(a)}<span><span class="kicker">{a["secao"]}</span>'
        f'<strong>{html.escape(a["title"])}</strong></span></a>'
        for a in (arts[n] for n in ULTIMAS))
    pauta = "".join(f'<a href="{url(arts[n])}">{html.escape(t)}</a>' for t, n in EM_PAUTA)
    out = ['<h1 class="sr-only">Energia &amp; Capital: notícias, guias e análises sobre energia no Brasil</h1>',
           f'<nav class="pauta" aria-label="Em pauta"><div class="wrap"><span class="tag">Em pauta</span>{pauta}</div></nav>',
           '<main class="wrap">',
           f"""<section class="destaque">
  <article class="principal"><a href="{url(d)}">
    {thumb(d, grande=True)}
    <span class="kicker">{d["secao"]}</span>
    <h2 class="cond" style="margin:8px 0 0;font-size:48px;line-height:1.02">{html.escape(d["title"])}</h2>
    <p class="linha-fina serif">{html.escape(resumo(d["summary"], 260))}</p>
    <p class="meta">Redação · <time datetime="{d["publicado"]}">{data_br(d["publicado"])}</time> · {d["leitura"]} min de leitura</p>
  </a></article>
  <aside class="lateral"><h2 class="rotulo">Últimas</h2>{ultimas}</aside>
</section>"""]
    for s in secoes:
        itens = [arts[n] for n in s["artigos"]]
        topo = (f'<div class="secao-topo"><h2 class="cond">{html.escape(s["titulo"])}</h2>'
                f'<a href="/{s["id"]}/">Ver tudo em {html.escape(s["titulo"])} →</a></div>')
        if s["id"] == "investidor" and len(itens) > 1:
            g, resto = itens[0], itens[1:4]
            lista = "".join(f'<a href="{url(a)}"><span class="kicker">{a["secao"]}</span><strong>{html.escape(a["title"])}</strong></a>' for a in resto)
            corpo = (f'<div class="dupla"><a class="card-grande" href="{url(g)}">{thumb(g)}<span class="txt">'
                     f'<span class="kicker">Análise</span><strong class="cond">{html.escape(g["title"])}</strong>'
                     f'<span class="serif">{html.escape(resumo(g["summary"]))}</span></span></a>'
                     f'<div class="lista-texto">{lista}</div></div>')
        else:
            corpo = '<div class="grade">' + "".join(card(a) for a in itens[:4]) + "</div>"
        out.append(f'<section class="secao" id="{s["id"]}">{topo}{corpo}</section>')
    out.append("</main>")
    return "\n".join(out)


def hub(s, arts):
    itens = sorted((arts[n] for n in s["artigos"]), key=lambda a: a["publicado"], reverse=True)
    return (f'<main class="wrap"><div class="hub-topo"><p class="trilha"><a href="/">Início</a> / {html.escape(s["titulo"])}</p>'
            f'<h1 class="cond">{html.escape(s["titulo"])}</h1><p class="serif">{html.escape(s["descricao"])}</p></div>'
            f'<section class="secao"><div class="grade">{"".join(card(a, True) for a in itens)}</div></section></main>')


def breadcrumb(*nivel):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": nome, "item": absoluto(c)} for i, (nome, c) in enumerate(nivel, 1)]}


def grupo(a):
    return next((s for s in SECOES if a["num"] in s["artigos"]), SECOES[0])


def artigo_jsonld(a):
    return [{
        "@context": "https://schema.org", "@type": "Article",
        "headline": a["title"][:110], "description": resumo(a["summary"], 200), "inLanguage": "pt-BR",
        "mainEntityOfPage": absoluto(url(a)), "articleSection": a["secao"], "wordCount": a["palavras"],
        "datePublished": a["publicado"], "dateModified": a["atualizado"],
        "author": {"@type": "Organization", "name": "Redação Energia & Capital", "url": absoluto("/sobre/")},
        "publisher": org(), "image": [absoluto(imagem_og(a))],
    }, breadcrumb(("Início", "/"), (grupo(a)["titulo"], f"/{grupo(a)['id']}/"), (a["title"], url(a)))]


def relacionados(a, arts, n=3):
    mesmo = [arts[k] for k in grupo(a)["artigos"] if k != a["num"]]
    resto = sorted((x for x in arts.values() if x["num"] != a["num"] and x not in mesmo),
                   key=lambda x: x["publicado"], reverse=True)
    return (mesmo + resto)[:n]


def artigo(a, arts, md):
    g = grupo(a)
    mais = "".join(f'<a href="{url(x)}"><span class="n">{i}</span><strong>{html.escape(x["title"])}</strong></a>'
                   for i, x in enumerate(relacionados(a, arts), 1))
    return f"""<main class="wrap"><div class="artigo-layout">
  <article class="artigo">
    <nav class="trilha" aria-label="Trilha"><a href="/">Início</a> / <a href="/{g["id"]}/">{html.escape(g["titulo"])}</a></nav>
    <span class="kicker">{a["secao"]}</span>
    <h1 class="cond">{html.escape(a["title"])}</h1>
    <p class="linha-fina serif">{md.reset().convert(a["summary"])[3:-4]}</p>
    <div class="byline"><b><a href="/sobre/">Redação Energia &amp; Capital</a></b><time datetime="{a["publicado"]}">{data_br(a["publicado"])}</time><span>{a["leitura"]} min de leitura</span></div>
    {thumb(a, "thumb capa", grande=True)}
    {f'<p class="credito">{credito(a["foto"])}</p>' if a.get("foto") else ""}
    <div class="corpo">{md.reset().convert(a["corpo"])}</div>
    <div class="aviso">{DISCLAIMER}</div>
  </article>
  <aside class="lateral" style="gap:32px">
    <div class="cta-lateral">{simbolo(44, invertido=True)}<strong class="cond">O essencial da energia no seu e-mail</strong>
      <a class="btn-sol" href="#newsletter">Assinar grátis</a></div>
    <div class="mais-lidas"><h2 class="rotulo">Leia também</h2>{mais}</div>
  </aside>
</div></main>"""


SOBRE = f"""<main class="wrap pagina-simples corpo">
<h1 class="cond">Sobre a Energia &amp; Capital</h1>
<p>A <b>Energia &amp; Capital</b> é uma publicação sobre o setor de energia no Brasil. Explicamos, em linguagem direta,
como a energia é gerada, contratada e regulada — e o que isso significa para consumidores, empresas e investidores.</p>
<h2>Quem mantém</h2>
<p>A publicação é mantida pela <b>ZeroInvest</b>, empresa que desenvolve projetos de energia. Informamos essa relação em
todas as páginas. A Energia &amp; Capital não faz oferta, recomendação ou solicitação de investimento em valores
mobiliários, e nenhum conteúdo menciona produtos da ZeroInvest.</p>
<h2>Política editorial</h2>
<ul>
<li>Todo artigo cita fontes públicas — ANEEL, ONS, CCEE, EPE, legislação e relatórios setoriais.</li>
<li>Todo artigo traz uma seção de riscos: nenhum ativo ou tecnologia de energia é livre de risco.</li>
<li>Não usamos promessas de retorno, nem termos como "garantido" ou "sem risco".</li>
<li>Estimativas próprias da Redação são identificadas como tal.</li>
<li>Erros são corrigidos assim que identificados, com atualização da data do artigo.</li>
</ul>
<h2>Contato</h2>
<p>Correções, sugestões de pauta e dúvidas sobre dados pessoais: {EMAIL_PRIVACIDADE}.</p>
</main>"""


def rss(arts):
    itens = sorted(arts.values(), key=lambda a: a["publicado"], reverse=True)
    def data_rss(iso):
        return datetime.datetime.fromisoformat(iso + "T09:00:00-03:00").strftime("%a, %d %b %Y %H:%M:%S %z")
    corpo = "".join(
        f"<item><title>{html.escape(a['title'])}</title><link>{absoluto(url(a))}</link><guid>{absoluto(url(a))}</guid>"
        f"<pubDate>{data_rss(a['publicado'])}</pubDate><category>{html.escape(a['secao'])}</category>"
        f"<description>{html.escape(resumo(a['summary'], 300))}</description></item>" for a in itens)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>'
            f"<title>Energia &amp; Capital</title><link>{absoluto('/')}</link>"
            "<description>Notícias, guias e análises sobre energia no Brasil.</description><language>pt-BR</language>"
            f"{corpo}</channel></rss>\n")


def escreve(caminho, conteudo):
    destino = OUT / caminho.strip("/") / "index.html" if caminho.endswith("/") else OUT / caminho.lstrip("/")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(conteudo, encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / "style.css").write_text(CSS, encoding="utf-8")
    (OUT / "favicon.svg").write_text(simbolo(64).replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
                                     .replace(' aria-hidden="true"', ''), encoding="utf-8")
    shutil.copy(ROOT / "imagens" / "favicon.ico", OUT / "favicon.ico")
    shutil.copytree(ROOT / "imagens", OUT / "img", ignore=shutil.ignore_patterns("*.json", "redes"))

    arts = load_articles()
    secoes = [s for s in SECOES if s["artigos"]]
    md = markdown.Markdown(extensions=["tables"])

    for a in arts.values():
        escreve(url(a), page(titulo(a["seo"]), artigo(a, arts, md), resumo(a["summary"], 155),
                             secoes, origem=a["slug"], caminho=url(a), tipo="article", imagem=imagem_og(a),
                             jsonld=artigo_jsonld(a), ativo=grupo(a)["id"]))

    for s in secoes:
        escreve(f"/{s['id']}/", page(titulo(s["seo"]), hub(s, arts), s["descricao"], secoes,
                                     origem=s["id"], caminho=f"/{s['id']}/", ativo=s["id"],
                                     jsonld=breadcrumb(("Início", "/"), (s["titulo"], f"/{s['id']}/"))))

    escreve("/", page("Energia & Capital: notícias e análises sobre energia no Brasil", home(arts, secoes),
                      "Notícias, guias práticos e análises sobre o setor elétrico: energia solar, mercado livre, "
                      "conta de luz, data centers e investimento em infraestrutura.", secoes, completo=True, origem="home",
                      jsonld=[{"@context": "https://schema.org", "@type": "WebSite", "name": "Energia & Capital",
                               "url": absoluto("/"), "inLanguage": "pt-BR", "publisher": org()},
                              {"@context": "https://schema.org", **org()}]))

    escreve("/sobre/", page("Sobre a Energia & Capital: quem somos e política editorial", SOBRE,
                            "Quem mantém a Energia & Capital, nossa política editorial e como entrar em contato.",
                            secoes, origem="sobre", caminho="/sobre/",
                            jsonld={"@context": "https://schema.org", "@type": "AboutPage", "name": "Sobre a Energia & Capital",
                                    "url": absoluto("/sobre/"), "publisher": org()}))

    escreve("/obrigado/", page(
        "Inscrição confirmada | Energia & Capital",
        '<main class="wrap pagina-simples"><h1 class="cond">Inscrição recebida</h1>'
        '<p class="serif" style="font-size:20px">Obrigado. Você receberá a próxima edição da Energia &amp; Capital no seu e-mail.</p>'
        '<p><a class="btn-sol" href="/">Voltar à página inicial</a></p></main>',
        "Inscrição confirmada.", secoes, origem="obrigado", caminho="/obrigado/", indexar=False))

    privacidade = (ROOT / "landing" / "privacidade.md").read_text(encoding="utf-8")
    privacidade = privacidade.replace("{CONTROLADOR}", CONTROLADOR).replace("{EMAIL}", EMAIL_PRIVACIDADE)
    escreve("/privacidade/", page(
        "Política de Privacidade | Energia & Capital",
        f'<main class="wrap pagina-simples corpo">{md.reset().convert(privacidade)}</main>',
        "Como a Energia & Capital trata os dados de quem assina a newsletter, com base na LGPD.", secoes, origem="privacidade", caminho="/privacidade/"))

    linhas = "".join(f'<li><b>{html.escape(a["title"])}</b><br>{credito(a["foto"])}</li>'
                     for a in arts.values() if a.get("foto"))
    escreve("/creditos/", page(
        "Créditos das imagens | Energia & Capital",
        '<main class="wrap pagina-simples corpo"><h1 class="cond">Créditos das imagens</h1>'
        '<p>As fotos são do Wikimedia Commons, usadas conforme as licenças indicadas e recortadas para o formato do site. '
        f'As demais imagens são ilustrações da Energia &amp; Capital.</p><ul>{linhas}</ul></main>',
        "Autores e licenças das fotos usadas nos artigos da Energia & Capital, publicação sobre o setor de energia.", secoes, origem="creditos", caminho="/creditos/"))

    escreve("/404.html", page(
        "Página não encontrada | Energia & Capital",
        '<main class="wrap pagina-simples"><h1 class="cond">Página não encontrada</h1>'
        '<p class="serif" style="font-size:20px">O endereço mudou ou não existe. Veja as últimas notícias na página inicial.</p>'
        '<p><a class="btn-sol" href="/">Ir para a página inicial</a></p></main>',
        "Página não encontrada.", secoes, origem="404", caminho="/404.html", indexar=False))

    # Sitemap com imagens, RSS, robots e redirecionamentos dos endereços antigos
    hoje = datetime.date.today().isoformat()
    ultima = max(a["atualizado"] for a in arts.values())
    urls = [("/", ultima, None)] + [(f"/{s['id']}/", ultima, None) for s in secoes]
    urls += [(url(a), a["atualizado"], imagem_og(a) if a.get("foto") else None) for a in arts.values()]
    urls += [("/sobre/", hoje, None), ("/privacidade/", None, None), ("/creditos/", None, None)]
    itens = "".join(f"<url><loc>{absoluto(c)}</loc>" + (f"<lastmod>{d}</lastmod>" if d else "")
                    + (f"<image:image><image:loc>{absoluto(i)}</image:loc></image:image>" if i else "") + "</url>"
                    for c, d, i in urls)
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        f'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">{itens}</urlset>\n', encoding="utf-8")
    (OUT / "feed.xml").write_text(rss(arts), encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /obrigado/\n\nSitemap: {absoluto('/sitemap.xml')}\n",
                                    encoding="utf-8")
    redirects = [f"/artigos/{a['arquivo']}.html {url(a)} 301" for a in arts.values()]
    redirects += [f"/{p}.html /{p}/ 301" for p in ("privacidade", "creditos", "obrigado")]
    (OUT / "_redirects").write_text("\n".join(redirects) + "\n", encoding="utf-8")
    if not SITE:
        print("ATENÇÃO: URL do site não definida (SITE_URL/URL); canonical e sitemap ficaram com caminhos relativos.")

    for p in OUT.rglob("*.html"):
        if re.search(r"\[(RAZÃO|00\.|email-|DADO)", p.read_text(encoding="utf-8")):
            print(f"ATENÇÃO: placeholder pendente em {p.relative_to(ROOT)}")
    print(f"Site gerado em {OUT.relative_to(ROOT)}/ ({len(arts)} artigos)")


if __name__ == "__main__":
    main()
