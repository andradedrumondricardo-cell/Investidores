# Fluxo pós-lead

## O que o lead autorizou
Na landing, o lead consente com **newsletter educacional**. Contato comercial é um consentimento **separado e opcional** (LGPD, art. 8º §4º — finalidade específica).

## Segmentação

| Segmento | Origem | O que pode receber |
|---|---|---|
| A — Newsletter | Landing, só consentimento 1 | Conteúdo educacional. Nada de oferta. |
| B — Aceitou contato | Landing, consentimentos 1 e 2 | Educacional + aviso quando houver **oferta regular** (CVM 88 / CVM 160), pelo canal oficial dela |
| C — Relacionamento prévio | Rede pessoal dos sócios, sem origem no marketing | Conversa individual sobre SCP privada, com assessoria jurídica |

**Nunca migrar lead do segmento A/B para C.** A origem do contato é o que define se a abordagem é privada.

## Nutrição (segmentos A e B)
- 1 e-mail a cada 15 dias com artigo novo.
- Webinar educacional sobre o setor (sem slide de produto, sem Q&A sobre "como investir"). Se perguntarem: *"Não fazemos oferta de investimento por este canal."*
- Pesquisa de interesse (opcional): "Quais temas do setor elétrico você quer entender?" — nunca "quanto você investiria".

## Quando houver oferta regular
- Comunicação ao segmento B apontando para a plataforma/coordenador autorizado.
- Todo material de oferta segue as regras da própria oferta (lâmina, avisos obrigatórios, suitability feito pela plataforma/intermediário).

## Ferramenta: Brevo

Cada inscrição verificada no Netlify Forms dispara a função `netlify/functions/submission-created.js`, que cria ou atualiza o contato no Brevo:
- todos os inscritos entram na lista **Newsletter** (segmento A);
- quem marcou o consentimento de contato entra também na lista **Aceitou contato** (segmento B).

O registro do consentimento (texto, versão `versao_consentimento`, data e origem) continua no Netlify Forms, que é a fonte da prova. Exporte o CSV quando precisar e não guarde os dados no GitHub.

Configuração (uma vez):
1. Conta grátis no Brevo; autenticar o domínio energiaecapital.com.br (registros DNS no painel do Netlify DNS) e cadastrar o remetente.
2. Criar as listas **Newsletter** e **Aceitou contato** e anotar os IDs numéricos.
3. Gerar uma chave de API no Brevo (SMTP & API → Chaves de API).
4. No Netlify, em Site configuration → Environment variables (escopo Functions): `BREVO_API_KEY`, `BREVO_LISTA_NEWSLETTER`, `BREVO_LISTA_CONTATO` e, se o atributo de nome da conta não for `FIRSTNAME`, `BREVO_ATRIBUTO_NOME`. Depois, novo deploy.
5. Importar os inscritos anteriores pelo CSV do Netlify Forms (Contatos → Importar), respeitando as duas listas.

Regras de envio no Brevo:
- Lista **Newsletter**: só conteúdo educacional (artigos, guias). Nada de oferta, nem "em breve".
- Lista **Aceitou contato**: além do educacional, aviso de oferta **regular** (CVM 88 / CVM 160) apontando para a plataforma ou o coordenador autorizado, quando houver.
- Nenhum contato dessas listas vai para conversa sobre SCP privada (segmento C).
- Todo e-mail sai com o link de descadastro do Brevo; descadastrados não voltam à lista sem nova inscrição.

## Registro
Guardar: data e texto do consentimento, IP, versão da política de privacidade, histórico de envios e opt-outs.
