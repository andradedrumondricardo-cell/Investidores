# IA e data centers: o atalho elétrico e o MW parado que o Brasil ainda não usa

Enquanto grandes data centers esperam anos por uma ligação na transmissão, conexões ociosas e a sobra de renováveis abrem caminho para projetos de 5 a 20 MW. O maior obstáculo não é a energia, e sim o imposto sobre os equipamentos.

## Em resumo

- A corrida da IA virou uma disputa por megawatts conectados, e a rede não acompanha, aqui e lá fora.
- No Brasil, falta rede nos centros de consumo e sobra energia renovável onde está a geração; parte dela é cortada.
- Cargas de 5 a 20 MW podem se ligar pelas distribuidoras em meses, e conexões industriais ociosas são um atalho pouco explorado.
- Baterias fazem mais sentido para tirar a carga da rede na ponta do que para abastecer a noite inteira.
- O principal obstáculo econômico é o imposto sobre servidores e GPUs importados, não o preço da energia.

## A corrida agora é por megawatts

Imagine um galpão cheio de servidores novos, com tudo instalado, menos a tomada. A cena virou comum: a corrida da inteligência artificial deixou de ser por chips e virou uma corrida por megawatts conectados.

A consultoria JLL estima que a capacidade mundial de data centers vai dobrar até 2030, de 103 GW para 200 GW, com 97% de ocupação e três quartos das obras já pré-alugadas. Para a Agência Internacional de Energia (IEA), o consumo elétrico deles pode mais que dobrar no período.

A rede elétrica não acompanha. Em agosto, o Texas suspendeu novas aprovações de conexão de data centers diante de uma fila de centenas de gigawatts. No norte da Virgínia, maior polo do setor no mundo, uma carga de 100 MW pode esperar até sete anos.

O Brasil vive a mesma pressão, em escala menor e com um paradoxo: **falta rede onde está a demanda, e sobra energia onde está a geração.**

## A fila nos centros de consumo

Em fevereiro, havia cerca de 7 GW em pedidos de acesso de data centers à Rede Básica, a malha de transmissão de alta tensão, 3,9 GW só em São Paulo.

A nova política de acesso à transmissão, a PNAST, viabilizou 30,7 GW em 2026, sendo 13,5 GW de novas cargas. Em São Paulo, porém, 451 MW de consumo disputam 228 MW de margem num processo competitivo marcado para outubro.

A CPFL relatou ter negado cerca de 8 GW em pedidos de data centers no interior paulista. No Pecém, no Ceará, o operador do sistema, o ONS, chegou a suspender novas conexões de data centers por falta de infraestrutura e hoje condiciona parte dos projetos a novas obras de transmissão.

Parte desses pedidos é especulativa. A previsão oficial de carga de ONS, EPE e CCEE indica cerca de 5,7 GW médios de consumo de data centers em 2030, contra perto de 10 GW nas contas do Ministério de Minas e Energia. Mas a escassez é real para quem já tem equipamento contratado e precisa ligá-lo em meses.

O país tem hoje entre 706 e 826 MW de data centers instalados. E a capacidade com refrigeração líquida dos grandes operadores, exigida pelas GPUs (os chips usados em IA) atuais, está praticamente vendida até meados de 2027.

## O paradoxo: energia sobrando

Do outro lado, usinas renováveis são obrigadas a produzir menos, o chamado [curtailment](/artigos/curtailment/). É como uma loja com estoque cheio e a rua bloqueada. Em 2025, 20,6% da energia eólica e solar disponível deixou de ser gerada, uma perda estimada em mais de R$ 6 bilhões, segundo a consultoria Volt Robotics, com dados do ONS.

Uma portaria do MME (Portaria MME 140/2026) regulamentou o ressarcimento dos cortes de 2023 a 2025 por indisponibilidade externa ou confiabilidade elétrica, mas deixou de fora os cortes por excesso de oferta. Geradores com energia cortada ganharam motivo de sobra para vender a quem consuma.

Mas um data center ao lado da usina não resolve o corte em todo lugar. A análise da Redação com dados abertos do ONS mostra dois casos opostos:

- **Norte de Minas:** mais de 5 GW de solar em grandes usinas; cerca de 26% da geração possível foi cortada em doze meses. A parte causada por gargalo local caiu para perto de 2% depois dos reforços de transmissão concluídos neste ano. O restante é sobra de oferta no sistema, que qualquer consumidor da mesma região de preço (o submercado) absorve.
- **Oeste do Rio Grande do Norte:** nos complexos eólicos mais afetados, 60% a 68% do corte ainda é local. Ali, uma carga instalada perto da geração alivia de fato a rede.

## O atalho da distribuição

Se a transmissão é a rodovia congestionada, a distribuição são as ruas do bairro, e o atalho passa por elas. Cargas de 5 a 20 MW se ligam pelas distribuidoras, sob as regras de conexão da ANEEL. O orçamento sai em semanas e as obras levam meses, contra 42 a 60 meses típicos na Rede Básica.

Há também um estoque pouco explorado: fábricas que fecharam ou reduziram a produção, mas mantêm subestação própria e contrato de uso da rede ativo. A regulação permite trocar o titular mantendo as condições do contrato. É como "passar o ponto" de uma loja com a luz já ligada: quem assume herda a demanda contratada, sem fila.

O cuidado é que só a demanda contratada fica protegida:

- se o contrato foi encerrado, o pedido volta a ser uma conexão nova;
- qualquer aumento de demanda depende de estudo da distribuidora, inclusive no horário de ponta, já que um data center consome o mesmo 24 horas por dia.

A ANEEL incluiu as grandes cargas na distribuição em sua agenda regulatória de 2026–2027, e algumas distribuidoras sem margem já negam aumentos.

A tecnologia também ajuda. As GPUs de última geração exigem refrigeração líquida direto no chip, em circuito fechado. O calor pode sair por radiadores secos, com consumo de água próximo de zero, o que atende ao limite de 0,05 litro por kWh do Redata, o novo regime de impostos para data centers.

Esses sistemas são vendidos em módulos de 1 a 10 MW, entregues de três a seis meses após o pedido.

A inferência (o uso dos modelos já treinados, que pode ser espalhado por vários locais) deve superar o treino em demanda de capacidade a partir de 2027, segundo a JLL. Em junho, a Elea anunciou em Belém um data center para IA, junto a uma subestação da AXIA. Ele começa com 7,5 MW e pode chegar a 100 MW.

## Bateria para a ponta, não para a noite

Um data center flexível pode ajudar o sistema. Estimativas da Redação, com o perfil solar do ONS e as tarifas da Cemig, mostram duas situações:

- **Bateria para a noite inteira**, com a rede só como reserva, ainda não se paga. A energia sai entre R$ 450 e R$ 770 por MWh, contra R$ 330 a R$ 450 da rede com contrato no mercado livre em 138 kV. E a rede precisa seguir contratada para dias nublados.
- **Bateria de três a quatro horas para o horário de ponta** se paga em cinco a sete anos em média tensão. Ela tira o data center da rede justamente na rampa do fim da tarde, quando a geração solar some e o ONS mais precisa de alívio.

É uma caixa d'água que cobre só o horário em que a pressão da rua cai. Veja [baterias na rede](/artigos/baterias-na-rede/).

*Números hipotéticos, apenas para ilustrar o mecanismo; não representam projeto, produto ou oferta existente.*

## O obstáculo não é a energia

Comparada à de outros países, a energia brasileira fica no meio do caminho. Para uma grande carga em alta tensão, com tudo incluído, o custo estimado vai de US$ 81 a US$ 117 por MWh. É mais caro que no Texas (US$ 60 a 75), mas equivalente a Virgínia, Ohio, Chile e México. A energia em si custa quase o mesmo que no Texas; o que dobra a conta são as tarifas de rede, os encargos e o ICMS.

O que afasta o investimento é o imposto sobre os equipamentos importados: servidores e, principalmente, GPUs. Um exercício de custo total para um site de inferência de 10 MW, somando energia, infraestrutura e impostos sobre a TI:

- **Brasil sem benefícios fiscais:** cerca de US$ 430 por kW por mês, contra US$ 181 no Texas. Cerca de 77% da diferença é imposto.
- **Com o Redata**, criado por uma lei sancionada em setembro (Lei 15.504/2026), cai por cinco anos o imposto de importação. Já o PIS/Cofins e o IPI caem só até o fim de 2026, por causa da reforma tributária. E o ICMS ficou de fora.
- **Somando todas as alavancas**, o custo cai para perto de US$ 190 e praticamente empata com Texas e Chile. Além do Redata, entram uma redução de ICMS em discussão no Confaz, a autoprodução, o reaproveitamento de sites e o financiamento do BNDES.

*Números hipotéticos, apenas para ilustrar o mecanismo; não representam projeto, produto ou oferta existente.*

## O que o setor pode fazer

O Brasil não deve vencer a corrida pelos campi de gigawatts para treinar modelos, que dependem de escala, capital barato e impostos favoráveis. Mas pode competir na velocidade: entregar MW conectados em meses, com matriz elétrica 88% renovável e perto de um mercado de mais de 200 milhões de pessoas. O setor elétrico tem quatro alavancas:

1. **Regras claras para grandes cargas na distribuição.** A revisão em curso na ANEEL pode organizar a demanda sem fechar o atalho, por exemplo com tratamento rápido para quem reaproveita conexões existentes.
2. **Mapas públicos de espaço para consumo.** Já há mapas de margem para geração. As distribuidoras poderiam publicar também os de consumo, como a Cemig e a Invest Minas começaram a fazer para data centers.
3. **Sinal econômico para a flexibilidade.** Cargas que consomem quando sobra energia e saem da rede na rampa do fim da tarde merecem tarifas e programas de resposta da demanda que reconheçam esse valor.
4. **Parcerias entre geradores e consumidores.** A autoprodução por equiparação, em que o consumidor vira sócio da usina, pode transformar a energia cortada em contrato de longo prazo. Pela lei de 2025 (Lei 15.269/2025), ela exige ao menos 30 MW somados, unidades de pelo menos 3 MW e 30% do capital da usina.

Fora do setor elétrico, a peça que falta é a dos impostos. Sem resolver o ICMS sobre os equipamentos, o MW conectado continua sem GPU para alimentar: a tomada fica pronta, mas o aparelho não chega.

A janela é curta. A partir de 2028 entram os grandes campi já anunciados, e a escassez nos centros de consumo tende a diminuir. Até lá, a energia hoje cortada e as conexões hoje ociosas podem virar ativos valiosos da economia digital, desde que o setor elétrico decida tratá-las assim.

## Riscos e incertezas

1. **Demanda incerta:** a distância entre a previsão oficial de carga (cerca de 5,7 GW médios em 2030) e a do MME (cerca de 10 GW) mostra o tamanho da dúvida. Chips mais eficientes podem reduzir a necessidade de energia.
2. **Regulação em revisão:** as regras para grandes cargas na distribuição estão na agenda da ANEEL e podem restringir esse atalho.
3. **Impostos:** o Redata vale por cinco anos, e a redução de ICMS ainda depende do Confaz.
4. **Janela de tempo:** a entrada dos grandes campi a partir de 2028 pode reduzir a escassez e a vantagem de velocidade.
5. **Estimativas:** os custos de baterias, a comparação internacional e o custo total por kW são estimativas da Redação, sensíveis a câmbio, tarifas e premissas.

## Perguntas frequentes

### Por que data centers de IA consomem tanta energia?
Os chips de IA concentram muita potência por rack (o armário de servidores) e funcionam 24 horas por dia. Um único campus pode demandar centenas de megawatts, o consumo de uma cidade média.

### O Brasil tem energia sobrando para data centers?
Em algumas regiões e horários, sim: parte da geração eólica e solar chega a ser cortada. O gargalo é levar essa energia aos grandes centros de consumo, onde falta rede.

### O que é conectar pela distribuição em vez da Rede Básica?
Cargas de 5 a 20 MW podem se ligar às distribuidoras locais em meses. Grandes cargas precisam da Rede Básica, cujas obras costumam levar de 42 a 60 meses.

### O que é o Redata?
É o regime especial de tributação para data centers, criado por lei sancionada em setembro. Suspende por até cinco anos tributos federais sobre equipamentos importados, com exigências como baixo consumo de água. O ICMS, estadual, ficou de fora.

### Data centers podem ajudar o sistema elétrico?
Podem, se forem flexíveis: consumir quando sobra energia e reduzir o consumo no fim da tarde, quando a solar cai. Para isso, precisam de tarifas e programas que reconheçam esse valor.

## Fontes
- JLL — relatórios globais de data centers
- IEA — *Energy and AI* (2025)
- ONS — dados abertos de restrição de geração e acesso à Rede Básica; previsão de carga 2026–2030 (com EPE e CCEE)
- MME — PNAST (Decreto 12.772/2025) e Portaria MME 140/2026
- ANEEL — REN 1.000/2021 e agenda regulatória 2026–2027
- Lei 15.269/2025 e Lei 15.504/2026 (Redata)
- Cemig e Invest Minas — mapas de capacidade para data centers

---
*Energia & Capital é uma publicação mantida pela ZeroInvest, empresa que desenvolve projetos de energia. O conteúdo é educacional e informativo, não constitui oferta, recomendação ou solicitação de investimento em valores mobiliários. Retornos passados ou de terceiros não garantem resultados futuros.*
