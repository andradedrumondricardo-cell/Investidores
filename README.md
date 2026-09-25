# Energia & Capital — publicação setorial (mantida pela ZeroInvest)

Material para gerar interesse no setor de energia sem que a comunicação se torne **oferta pública irregular** de valores mobiliários.

> ⚠️ Nada aqui substitui parecer de advogado especializado em mercado de capitais. Valide o fluxo completo (`docs/04-checklist-juridico.md`) antes de publicar.

## Premissa central

Participação em SCP oferecida a terceiros com promessa de retorno é, para a CVM, **contrato de investimento coletivo** (Lei 6.385/76, art. 2º, IX) — portanto valor mobiliário. Qualquer esforço de venda ao público em geral (site, redes sociais, anúncios, mailing) sem registro/dispensa caracteriza oferta pública irregular (Res. CVM 160), sujeita a *stop order*, multa e, em tese, crime (Lei 7.492/86, art. 7º).

**Consequência prática:** a publicação fala de **energia como classe de ativo**, com dados públicos de mercado, nunca da **oportunidade da ZeroInvest**. Não publique "IPCA + 15%" como expectativa, "baixo risco", "seguro" nem nada que ligue o artigo a um produto da ZeroInvest.

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `docs/01-riscos-regulatorios.md` | Mapa de riscos e como cada um é mitigado |
| `docs/02-guia-editorial.md` | Termos proibidos, substituições e regras de publicação |
| `docs/03-fluxo-pos-lead.md` | O que fazer (e não fazer) com o lead depois da captura |
| `docs/04-checklist-juridico.md` | Checklist para validação com advogado antes de ir ao ar |
| `docs/05-linha-editorial.md` | Posicionamento, pode/não pode, transparência e pauta |
| `artigos/` | 6 artigos (01–03 setoriais, 04–06 ótica do investidor) |
| `landing/privacidade.md` | Política de privacidade (preencher razão social, CNPJ e e-mail em `scripts/build.py`) |
| `scripts/build.py` | Gera o site em `site/` a partir dos artigos |
| `netlify.toml` | Configuração de deploy no Netlify |

## Publicar no Netlify

1. Netlify → **Add new site → Import an existing project → GitHub** → repositório `Investidores`.
2. Branch: a que contém este código. Build e pasta de publicação já vêm do `netlify.toml`.
3. Em **Forms**, ative a detecção de formulários. Inscrições ficam em *Forms → newsletter* (exportáveis em CSV).
4. Configure notificação de e-mail do formulário e, se quiser, domínio próprio.

Para testar localmente: `pip install -r requirements.txt && python3 scripts/build.py`, depois abra `site/index.html`.
