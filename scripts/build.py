"""Gera o site estático em site/ a partir de artigos/*.md.

Uso: pip install -r requirements.txt && python3 scripts/build.py
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

# Link do CANAL do WhatsApp (somente leitura), não de grupo. Vazio = links não aparecem no site.
WHATSAPP_CANAL_URL = ""

# Metadados de cada artigo: seção (chapéu) e ilustração (ver ILUSTRACOES).
ARTIGOS = {
    "01": {"secao": "Entenda", "ilustracao": "solar", "foto": "campo-solar", "alt": "Campo de painéis solares ao entardecer"},
    "02": {"secao": "Solar", "ilustracao": "casa", "foto": "telhado-solar", "alt": "Painéis solares sobre telhado residencial"},
    "03": {"secao": "Checklist", "ilustracao": "lampada"},
    "04": {"secao": "Investidor", "ilustracao": "eolica", "foto": "parque-eolico", "alt": "Parque eólico ao pôr do sol"},
    "05": {"secao": "Investidor", "ilustracao": "grafico"},
    "06": {"secao": "Investidor", "ilustracao": "torre"},
    "07": {"secao": "Conta de luz", "ilustracao": "bandeiras"},
    "08": {"secao": "Rede", "ilustracao": "curtailment", "foto": "linhas-transmissao", "alt": "Torres e linhas de transmissão ao anoitecer"},
    "09": {"secao": "Curiosidade", "ilustracao": "flutuante", "foto": "solar-flutuante", "alt": "Usina solar flutuante sobre reservatório"},
    "10": {"secao": "Tecnologia", "ilustracao": "bateria"},
    "11": {"secao": "Mercado livre", "ilustracao": "mercado"},
    "12": {"secao": "Glossário", "ilustracao": "glossario"},
    "13": {"secao": "IA e energia", "ilustracao": "datacenter", "foto": "data-center", "alt": "Corredor de data center com racks de servidores"},
}

# Composição da home. Seções sem artigos não aparecem.
DESTAQUE = "13"
ULTIMAS = ["07", "08", "11", "10"]
SECOES = [
    {"id": "na-pratica", "titulo": "Na prática", "artigos": ["11", "02", "03", "01"]},
    {"id": "investidor", "titulo": "Investidor", "artigos": ["04", "05", "06", "08"]},
    {"id": "variedades", "titulo": "Variedades", "artigos": ["09", "12", "10"]},
]
EM_PAUTA = [("IA e data centers", "13"), ("Bandeiras tarifárias", "07"), ("Lei 14.300", "02"), ("Curtailment", "08"),
            ("Mercado livre", "11"), ("Baterias", "10")]

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

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900'
         '&amp;family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400&amp;display=swap" rel="stylesheet">')

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
.secao-topo{display:flex;justify-content:space-between;align-items:baseline;gap:16px;margin-bottom:20px;border-top:4px solid var(--ink);padding-top:10px}
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
    <form name="newsletter" method="POST" action="/obrigado.html" data-netlify="true" netlify-honeypot="empresa">
      <input type="hidden" name="form-name" value="newsletter">
      <input type="hidden" name="origem" value="{origem}">
      <input type="hidden" name="versao_consentimento" value="v2-2026-09">
      <p class="hidden"><label>Não preencha: <input name="empresa"></label></p>
      <div class="campos">
        <label class="campo">Nome<input name="nome" type="text" autocomplete="name" required></label>
        <label class="campo">E-mail<input name="email" type="email" autocomplete="email" required></label>
      </div>
      <label class="check"><input type="checkbox" name="consentimento_newsletter" value="sim" required>
        <span>Quero receber a newsletter Energia &amp; Capital e concordo com a <a href="/privacidade.html">Política de Privacidade</a>.</span></label>
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


def cabecalho(completo, secoes_home):
    data = ('<span class="data" id="hoje"></span>'
            '<script>try{document.getElementById("hoje").textContent=new Date().toLocaleDateString("pt-BR",'
            '{weekday:"long",day:"numeric",month:"long",year:"numeric"})}catch(e){}</script>')
    topo = (f'<div class="topbar"><div class="wrap">{data}<nav aria-label="Atalhos">'
            f'{link_whatsapp("", "Canal no WhatsApp")}<a class="btn-sol" href="#newsletter">Assine grátis</a></nav></div></div>')
    links = "".join(f'<a href="/#{s["id"]}">{html.escape(s["titulo"])}</a>' for s in secoes_home)
    if completo:
        return topo + f"""
<header class="masthead">
  <div class="wrap marca">
    <a class="logo" href="/" aria-label="Energia &amp; Capital — página inicial">{simbolo(64)}
      <span class="nome cond"><span>ENERGIA</span><span><span class="amp">&amp;</span>CAPITAL</span></span></a>
    <p class="slogan">Notícias, guias e análises sobre energia no Brasil</p>
  </div>
  <nav class="secoes" aria-label="Seções"><div class="wrap"><a class="ativo" href="/">Início</a>{links}<a href="#newsletter">Newsletter</a></div></nav>
</header>"""
    return topo + f"""
<header class="masthead compacto">
  <div class="wrap">
    <a class="logo-h cond" href="/" aria-label="Energia &amp; Capital — página inicial">{simbolo(40)}<span>ENERGIA<span class="amp">&amp;</span>CAPITAL</span></a>
    <nav aria-label="Seções"><a href="/">Início</a>{links}</nav>
  </div>
</header>"""


def rodape():
    return f"""
<footer class="rodape"><div class="wrap">
  <span class="assinatura cond">{simbolo(32, invertido=True)} ENERGIA &amp; CAPITAL</span>
  <p>{DISCLAIMER} <a href="/privacidade.html">Política de Privacidade</a></p>
</div></footer>"""


def page(title, body, description, secoes_home, completo=False, origem="pagina"):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta name="theme-color" content="#0E1B17">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="/style.css">
</head>
<body>
{cabecalho(completo, secoes_home)}
{body}
{FORM.format(origem=origem, whatsapp=link_whatsapp("wa", "Prefere WhatsApp? Siga o canal Energia &amp; Capital"))}
{rodape()}
</body>
</html>
"""


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
        arts[num] = {
            "num": num, "slug": path.stem, "title": title, "summary": blocos[i].strip(),
            "corpo": corpo, "leitura": max(1, round(palavras / 200)), **meta,
        }
    return arts


def url(a):
    return f"/artigos/{a['slug']}.html"


def thumb(a, classe="thumb", grande=False):
    if a.get("foto"):
        pasta = "img" if grande else "img/thumb"
        return (f'<div class="{classe}"><img src="/{pasta}/{a["foto"]}.jpg" alt="{html.escape(a["alt"])}" '
                f'loading="lazy" width="1600" height="900"></div>')
    return f'<div class="{classe}">{ILUSTRACOES[a["ilustracao"]]}</div>'


def home(arts, secoes):
    d = arts[DESTAQUE]
    ultimas = "".join(
        f'<a class="item-lista" href="{url(a)}">{thumb(a)}<span><span class="kicker">{a["secao"]}</span>'
        f'<strong>{html.escape(a["title"])}</strong></span></a>'
        for a in (arts[n] for n in ULTIMAS))
    pauta = "".join(f'<a href="{url(arts[n])}">{html.escape(t)}</a>' for t, n in EM_PAUTA)
    out = [f'<div class="pauta"><div class="wrap"><span class="tag">Em pauta</span>{pauta}</div></div>',
           '<main class="wrap">',
           f"""<section class="destaque">
  <article class="principal"><a href="{url(d)}">
    {thumb(d, grande=True)}
    <span class="kicker">{d["secao"]}</span>
    <h1 class="cond">{html.escape(d["title"])}</h1>
    <p class="linha-fina serif">{html.escape(resumo(d["summary"], 260))}</p>
    <p class="meta">Redação · {d["leitura"]} min de leitura</p>
  </a></article>
  <aside class="lateral"><h2 class="rotulo">Últimas</h2>{ultimas}</aside>
</section>"""]
    for s in secoes:
        itens = [arts[n] for n in s["artigos"]]
        topo = f'<div class="secao-topo"><h2 class="cond">{html.escape(s["titulo"])}</h2></div>'
        if s["id"] == "investidor" and len(itens) > 1:
            g, resto = itens[0], itens[1:]
            lista = "".join(f'<a href="{url(a)}"><span class="kicker">{a["secao"]}</span><strong>{html.escape(a["title"])}</strong></a>' for a in resto)
            corpo = (f'<div class="dupla"><a class="card-grande" href="{url(g)}">{thumb(g)}<span class="txt">'
                     f'<span class="kicker">Análise</span><strong class="cond">{html.escape(g["title"])}</strong>'
                     f'<span class="serif">{html.escape(resumo(g["summary"]))}</span></span></a>'
                     f'<div class="lista-texto">{lista}</div></div>')
        else:
            corpo = '<div class="grade">' + "".join(
                f'<a class="card" href="{url(a)}">{thumb(a)}<span class="kicker">{a["secao"]}</span>'
                f'<strong>{html.escape(a["title"])}</strong></a>' for a in itens) + "</div>"
        out.append(f'<section class="secao" id="{s["id"]}">{topo}{corpo}</section>')
    out.append("</main>")
    return "\n".join(out)


def artigo(a, arts, md):
    outros = [x for n, x in arts.items() if n != a["num"]][:3]
    mais = "".join(f'<a href="{url(x)}"><span class="n">{i}</span><strong>{html.escape(x["title"])}</strong></a>'
                   for i, x in enumerate(outros, 1))
    return f"""<main class="wrap"><div class="artigo-layout">
  <article class="artigo">
    <p class="trilha"><a href="/">Início</a> / {a["secao"]}</p>
    <span class="kicker">{a["secao"]}</span>
    <h1 class="cond">{html.escape(a["title"])}</h1>
    <p class="linha-fina serif">{md.reset().convert(a["summary"])[3:-4]}</p>
    <div class="byline"><b>Redação Energia &amp; Capital</b><span>{a["leitura"]} min de leitura</span></div>
    {thumb(a, "thumb capa", grande=True)}
    {'<p class="credito">Imagem: ilustração digital / Energia &amp; Capital</p>' if a.get("foto") else ""}
    <div class="corpo">{md.reset().convert(a["corpo"])}</div>
    <div class="aviso">{DISCLAIMER}</div>
  </article>
  <aside class="lateral" style="gap:32px">
    <div class="cta-lateral">{simbolo(44, invertido=True)}<strong class="cond">O essencial da energia no seu e-mail</strong>
      <a class="btn-sol" href="#newsletter">Assinar grátis</a></div>
    <div class="mais-lidas"><h2 class="rotulo">Leia também</h2>{mais}</div>
  </aside>
</div></main>"""


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "artigos").mkdir(parents=True)
    (OUT / "style.css").write_text(CSS, encoding="utf-8")
    (OUT / "favicon.svg").write_text(simbolo(64), encoding="utf-8")
    shutil.copytree(ROOT / "imagens", OUT / "img")

    arts = load_articles()
    secoes = [s for s in SECOES if s["artigos"]]
    md = markdown.Markdown(extensions=["tables"])

    for a in arts.values():
        (OUT / "artigos" / f"{a['slug']}.html").write_text(
            page(f"{a['title']} | Energia & Capital", artigo(a, arts, md), resumo(a["summary"], 160),
                 secoes, origem=a["slug"]), encoding="utf-8")

    (OUT / "index.html").write_text(
        page("Energia & Capital — notícias, guias e análises sobre energia", home(arts, secoes),
             "Notícias, guias práticos e análises sobre energia no Brasil.", secoes, completo=True, origem="home"),
        encoding="utf-8")

    (OUT / "obrigado.html").write_text(page(
        "Inscrição confirmada | Energia & Capital",
        '<main class="wrap pagina-simples"><h1 class="cond">Inscrição recebida</h1>'
        '<p class="serif" style="font-size:20px">Obrigado. Você receberá a próxima edição da Energia &amp; Capital no seu e-mail.</p>'
        '<p><a class="btn-sol" href="/">Voltar à página inicial</a></p></main>',
        "Inscrição confirmada.", secoes, origem="obrigado"), encoding="utf-8")

    privacidade = (ROOT / "landing" / "privacidade.md").read_text(encoding="utf-8")
    privacidade = privacidade.replace("{CONTROLADOR}", CONTROLADOR).replace("{EMAIL}", EMAIL_PRIVACIDADE)
    (OUT / "privacidade.html").write_text(page(
        "Política de Privacidade | Energia & Capital",
        f'<main class="wrap pagina-simples corpo">{md.reset().convert(privacidade)}</main>',
        "Política de Privacidade da Energia & Capital.", secoes, origem="privacidade"), encoding="utf-8")

    for p in OUT.rglob("*.html"):
        if re.search(r"\[(RAZÃO|00\.|email-|DADO)", p.read_text(encoding="utf-8")):
            print(f"ATENÇÃO: placeholder pendente em {p.relative_to(ROOT)}")
    print(f"Site gerado em {OUT.relative_to(ROOT)}/ ({len(arts)} artigos)")


if __name__ == "__main__":
    main()
