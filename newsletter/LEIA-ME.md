# Newsletter (Brevo)

- `boas-vindas.html`: e-mail da automação de boas-vindas (entrada na lista Newsletter, #3).
- `AAAA-MM-edicao-NN.html`: uma edição quinzenal por arquivo. Para a próxima, duplique a última e troque os cards.

Como usar no Brevo: Campanhas → E-mail → Criar → no editor, escolha **Colar seu código** e cole o HTML.
Remetente: Energia & Capital <newsletter@energiaecapital.com.br> · Responder para: Gmail do Ricardo.

Regras:
- Envie só para a lista **Newsletter** (#3). A lista **Aceitou contato** (#4) serve apenas para avisos de oferta regular (CVM 88/160), quando houver.
- Conteúdo só educacional: nada de oferta, produto, SCP da ZeroInvest ou promessa de retorno.
- Personalização: `{% if contact.FIRSTNAME %}, {{ contact.FIRSTNAME }}{% endif %}`; descadastro: `{{ unsubscribe }}` (obrigatório).
