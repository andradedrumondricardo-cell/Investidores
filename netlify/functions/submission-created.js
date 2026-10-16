// Envia cada inscrição verificada do formulário "newsletter" (Netlify Forms) para o Brevo.
// O Netlify chama esta função automaticamente a cada envio aprovado pelo filtro de spam.
// Variáveis de ambiente (Netlify → Site configuration → Environment variables, escopo Functions):
//   BREVO_API_KEY           chave de API do Brevo (nunca no código)
//   BREVO_LISTA_NEWSLETTER  ID numérico da lista "Newsletter" (segmento A)
//   BREVO_LISTA_CONTATO     ID numérico da lista "Aceitou contato" (segmento B)
//   BREVO_ATRIBUTO_NOME     opcional; atributo do nome no Brevo (padrão: FIRSTNAME)
// O registro do consentimento (texto, versão, data) continua no Netlify Forms.

const ok = (msg) => ({ statusCode: 200, body: msg });

async function criaContato(contato, chave) {
  return fetch('https://api.brevo.com/v3/contacts', {
    method: 'POST',
    headers: { 'api-key': chave, accept: 'application/json', 'content-type': 'application/json' },
    body: JSON.stringify(contato),
  });
}

exports.handler = async (event) => {
  let payload;
  try {
    ({ payload } = JSON.parse(event.body || '{}'));
  } catch (e) {
    console.error('Corpo inválido', e);
    return ok('ignorado');
  }
  if (!payload || payload.form_name !== 'newsletter') return ok('outro formulário');

  const d = payload.data || {};
  const email = String(d.email || '').trim().toLowerCase();
  if (!email || d.consentimento_newsletter !== 'sim') return ok('sem e-mail ou sem consentimento');

  const chave = process.env.BREVO_API_KEY;
  const listaNews = Number(process.env.BREVO_LISTA_NEWSLETTER);
  if (!chave || !listaNews) {
    console.warn('Brevo não configurado (BREVO_API_KEY / BREVO_LISTA_NEWSLETTER). Inscrição mantida só no Netlify Forms.');
    return ok('brevo não configurado');
  }

  const listIds = [listaNews];
  const listaContato = Number(process.env.BREVO_LISTA_CONTATO);
  if (d.consentimento_contato === 'sim' && listaContato) listIds.push(listaContato);

  const atributo = process.env.BREVO_ATRIBUTO_NOME || 'FIRSTNAME';
  const nome = String(d.nome || '').trim().slice(0, 100);
  const contato = { email, listIds, updateEnabled: true };
  if (nome) contato.attributes = { [atributo]: nome };

  let resp = await criaContato(contato, chave);
  if (resp.status === 400 && contato.attributes) {
    // Atributo de nome inexistente na conta: grava o contato mesmo assim, sem o nome.
    console.warn('Brevo recusou o atributo de nome:', await resp.text());
    delete contato.attributes;
    resp = await criaContato(contato, chave);
  }
  if (!resp.ok) {
    console.error('Falha ao enviar contato ao Brevo:', resp.status, await resp.text());
    return ok('falha no brevo');
  }
  return ok('contato enviado ao brevo');
};
