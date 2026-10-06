# Baterias na rede: a caixa d'água que guarda energia para depois

Por mais de um século, a eletricidade precisou ser usada no instante em que era gerada. Baterias gigantes começam a mudar isso, guardando a sobra para depois. Entenda como funcionam, para que servem e em que pé está a regulação no Brasil.

## Em resumo
- Sistemas de armazenamento em baterias (BESS, na sigla em inglês) carregam quando sobra energia e descarregam quando a rede precisa.
- Predomina o lítio, sobretudo o tipo lítio-ferro-fosfato (LFP). Uma mesma bateria pode guardar energia para outro horário, ficar de reserva, estabilizar a rede, aliviar o pico e reduzir cortes.
- Dois números são essenciais: potência (MW) e energia (MWh). A divisão entre eles dá a duração, em geral de 2 a 4 horas em projetos de rede.
- No Brasil, uma lei de 2025 deu diretrizes para o armazenamento, e uma portaria de 2026 marcou para dezembro de 2026 os primeiros leilões só para baterias. Outras regras de remuneração seguem em discussão.

## Por que guardar energia virou assunto

Imagine sua casa sem caixa d'água: cada vez que alguém abrisse a torneira, a água teria de vir da rua naquele segundo. A rede elétrica funciona assim, com geração e consumo batendo a cada instante.

No Brasil, a caixa d'água sempre foram as hidrelétricas, com seus reservatórios. Mas a energia solar e eólica mudou o jogo. O sol bate no máximo ao meio-dia e some no fim da tarde, justamente quando você chega em casa e liga tudo.

Isso cria uma "rampa": em poucas horas, outras usinas correm para cobrir a saída do sol. Ao meio-dia, ao contrário, sobra energia, e renováveis são mandadas a gerar menos (veja [curtailment](/artigos/curtailment/)).

A bateria enche a caixa com a sobra do meio-dia e abre a torneira na rampa. Em países como Estados Unidos, China e Austrália, o armazenamento cresce depressa, puxado pela queda de custo das células de lítio apontada pela Agência Internacional de Energia (IEA).

## O que tem dentro de uma bateria de rede

Uma bateria de rede é bem mais que um monte de pilhas. As células ficam em contêineres com controle de temperatura e combate a incêndio, um sistema vigia cada uma, inversores adaptam a eletricidade à rede, e um "cérebro" decide a hora de encher e esvaziar.

Hoje domina o tipo **lítio-ferro-fosfato (LFP)**, que tende a ser mais estável com o calor e a durar mais ciclos, sem cobalto nem níquel. Guarda menos energia por quilo, o que pouco importa numa instalação parada no chão. Sódio-íon, baterias de fluxo e hidrelétricas reversíveis ainda têm pouca escala ou servem a durações longas.

## Os serviços que uma bateria presta

1. **Guardar para depois.** Encher quando a energia é barata ou sobra, no meio-dia, e esvaziar quando é cara ou escassa, no início da noite.
2. **Reserva.** Ficar de prontidão, como um estepe, para o pico ou para a falha de uma grande usina. Em vários países, isso é pago em leilões.
3. **Estabilizar a rede.** A rede trabalha a 60 Hz, ritmo que oscila quando geração e consumo se desencontram. Baterias reagem em frações de segundo.
4. **Aliviar o pico.** Descarregar nos horários críticos evita sobrecarga em linhas e pode adiar obras; em empresas, reduz a demanda na ponta.
5. **Menos cortes.** Perto de usinas renováveis, a bateria absorve a energia que seria cortada e a devolve mais tarde.
6. **Emergência:** religar usinas após um apagão e abastecer indústrias e data centers (veja [IA, data centers e energia](/artigos/ia-datacenters-energia/)).

Somar serviços costuma ser decisivo, mas depende de a regulação permitir.

## Largura do cano e tamanho da caixa: como ler os números

A **potência** é a largura do cano: quanto sai por instante. A **energia** é o tamanho da caixa: quanto cabe no total. Dividindo uma pela outra, você sabe por quantas horas a torneira fica aberta.

| Métrica | O que significa |
|---|---|
| Potência (MW) | Quanto a bateria entrega ou absorve por instante |
| Energia (MWh) | Quanto ela guarda no total |
| Duração (h) | Energia ÷ potência; em projetos de rede, costuma ser de 2 a 4 horas |
| Eficiência de ida e volta | Energia devolvida ÷ energia absorvida; no lítio, a perda costuma ficar na ordem de 10% a 15% |
| Ciclos | Cargas e descargas completas; mais ciclos geram mais receita, mas desgastam a bateria |
| Degradação | Perda gradual de capacidade com tempo e uso |

Uma bateria de **50 MW / 200 MWh** entrega 50 MW por até 4 horas. Uma de 50 MW / 100 MWh tem o mesmo cano e metade da caixa: só 2 horas.

Com o tempo, a caixa "encolhe": a degradação depende do tipo, da temperatura, de quanto a bateria é esvaziada e dos ciclos. Projetos costumam prever novos módulos ao longo da vida útil.

## Exemplo ilustrativo: do meio-dia para a noite

Suponha uma bateria de **20 MW / 80 MWh** (4 horas) ao lado de uma usina solar que sofreria corte ao meio-dia. Com eficiência de ida e volta de **88%**, ela devolve cerca de **70 MWh** no início da noite, vendidos a um preço suposto de **R$ 300 por MWh**.

| Item | Valor (hipotético) |
|---|---|
| Energia carregada por dia | 80 MWh |
| Energia devolvida (88%) | ~70 MWh |
| Receita diária (70 × R$ 300) | ~R$ 21 mil |
| Receita em 300 dias de operação | ~R$ 6,3 milhões |

*Números hipotéticos, apenas para ilustrar o mecanismo; não representam projeto, produto ou oferta existente.*

Veja como os riscos mexem na conta:

- **Degradação:** se a capacidade cair para 80%, a bateria devolve cerca de 56 MWh por dia, e a receita cai na mesma proporção, a menos que módulos sejam adicionados.
- **Preço:** se o preço da noite cair para R$ 200 por MWh, a receita anual vai para cerca de R$ 4,2 milhões.
- **Dias sem sobra:** sem corte, a bateria precisa comprar energia para carregar, e a margem vira a diferença de preço entre horários.

Do outro lado da balança estão os equipamentos (em geral importados), a conexão, a manutenção e as tarifas de uso da rede, ainda em definição.

## Em que pé está a regulação no Brasil

Uma lei de 2025 (Lei 15.269/2025) deu as diretrizes para o armazenamento, mas as regras detalhadas da ANEEL, a agência reguladora, ainda estão em construção. Em aberto:

- **O que a bateria é:** geração, consumo ou um agente próprio. Isso define as tarifas que paga, por exemplo, se paga ao carregar e ao descarregar.
- **Como é paga:** pela energia que vende, pela disponibilidade ou por serviços à rede, e se pode somar essas receitas.
- **Leilões:** uma portaria de 2026 do Ministério de Minas e Energia (Portaria MME 136/2026) definiu os dois primeiros leilões de reserva de capacidade só para baterias, previstos para 2 e 4 de dezembro de 2026, um deles com exigência de conteúdo nacional. Os contratos são de 15 anos, com início do fornecimento em agosto de 2028, e pagam pela disponibilidade do equipamento. Datas e regras podem mudar.

Por ora, os projetos no país são poucos e concentrados em usos específicos.

> Sem regra clara de remuneração, uma bateria pode ser útil para a rede e, ao mesmo tempo, não fechar a conta.

## O que isso significa para você

**Consumidor:** baterias podem reduzir o uso de térmicas caras no pico e o desperdício de renováveis. Em casas, são raras no Brasil, porque a [geração distribuída](/artigos/geracao-distribuida-como-funciona/) já usa a própria rede como "bateria", por meio de créditos.

**Empresa:** grandes consumidores podem usar baterias para reduzir a demanda na ponta, ter reserva em falhas e combinar com geração própria.

**Quem acompanha o setor:** o armazenamento deve ganhar peso com o aumento dos cortes e da rampa do fim da tarde. Vale observar remuneração, leilões, custo dos equipamentos e contratos (veja [contratos de longo prazo em energia](/artigos/contratos-longo-prazo-energia/) e [como avaliar riscos de projetos de energia](/artigos/como-avaliar-riscos-projetos-energia/)).

## Riscos

1. **Regulatório:** sem regras definitivas de remuneração e de encargos, a receita dos projetos é incerta.
2. **Tecnológico e de degradação:** as baterias perdem capacidade com o uso, e a vida útil depende do número de ciclos, da temperatura e da operação.
3. **Custo e câmbio:** os equipamentos são em grande parte importados; a variação do dólar e os impostos de importação pesam no investimento.
4. **Preço e receita de mercado:** a receita de guardar e vender depois depende da diferença de preço entre horários, que pode diminuir à medida que mais baterias entram no sistema.
5. **Incêndio e falhas:** exigem controle de temperatura, monitoramento e prevenção de incêndio; falhas podem causar paradas longas.

## Perguntas frequentes

### Por quanto tempo uma bateria de rede dura?
Depende do tipo, da temperatura e dos ciclos. Os projetos costumam ser planejados para mais de uma década, com perda gradual de capacidade, e o fabricante informa a capacidade mínima esperada.

### Baterias substituem as hidrelétricas?
Não. Baterias de 2 a 4 horas cuidam da variação dentro do dia; reservatórios guardam energia por meses. As duas se complementam.

### As baterias de lítio são perigosas?
Como todo equipamento que guarda muita energia, exigem cuidados: controle de temperatura, monitoramento das células, combate a incêndio e distância entre contêineres. O tipo LFP tende a ser mais estável com o calor.

### Por que ainda há poucas baterias no Brasil?
Principalmente porque as regras de remuneração e de encargos seguem em discussão. Sem saber como vai ser pago, o projeto tem dificuldade de obter financiamento.

## Fontes
- Lei 15.269/2025 — diretrizes para a regulação do armazenamento (planalto.gov.br)
- ANEEL — Consulta Pública 39/2023 (armazenamento) e Resolução Normativa 954/2021 (usinas híbridas e associadas) (gov.br/aneel)
- MME — Portaria MME 136/2026, diretrizes dos leilões de reserva de capacidade com baterias (gov.br/mme)
- EPE — estudos sobre armazenamento e Plano Decenal de Expansão de Energia (epe.gov.br)
- ONS — dados de operação e curvas de carga (ons.org.br)
- IEA — relatórios sobre baterias e armazenamento de energia (iea.org)

---
*Energia & Capital é uma publicação mantida pela ZeroInvest, empresa que desenvolve projetos de energia. O conteúdo é educacional e informativo, não constitui oferta, recomendação ou solicitação de investimento em valores mobiliários. Retornos passados ou de terceiros não garantem resultados futuros.*
