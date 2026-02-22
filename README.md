
# Análise Exploratória --- Airbnb Rio de Janeiro

## Contexto

Este projeto apresenta uma análise exploratória dos dados públicos do
Inside Airbnb referentes à cidade do Rio de Janeiro. O objetivo foi
compreender o comportamento dos preços, a distribuição geográfica dos
anúncios e identificar padrões relevantes no mercado de locação por
temporada.

A base inclui informações como preço por noite, tipo de acomodação,
bairro, número de avaliações, disponibilidade ao longo do ano e
quantidade de anúncios por anfitrião.
![logo_airbnb](/airbnb.jpg)
------------------------------------------------------------------------

## Tratamento dos Dados

Antes das análises, foi realizada uma etapa de limpeza e padronização:

-   Remoção de colunas totalmente vazias.
-   Exclusão de registros com ausência de `host_name`, devido à baixa
    representatividade.
-   Remoção de aproximadamente 10% da base por ausência de preço.
-   Definição de um teto analítico de R\$60.000 para reduzir o impacto
    de outliers extremos.

A variável preço apresentou forte assimetria à direita, com valores
muito elevados. Após aplicação de transformação logarítmica, observou-se
comportamento próximo do normal, indicando um padrão log-normal ---
comum em mercados imobiliários.

------------------------------------------------------------------------

## Principais Insights

A maior concentração de anúncios está em Copacabana, seguida por Ipanema
e Barra da Tijuca. Quando analisamos apenas os imóveis na faixa mais
alta de preço (percentil 99--100%), bairros como Barra da Tijuca, Copacabana, Joá, São Conrado e Ipanema ganham maior relevância.

Cerca de 80% dos anúncios são de imóveis inteiros (casas ou
apartamentos), enquanto quartos privados representam a maior parte do
restante.

A análise de correlação mostrou relação forte entre número total de
avaliações, avaliações por mês e avaliações nos últimos 12 meses, como
esperado. Não foram identificadas correlações relevantes entre preço e
variáveis operacionais.

Na análise textual dos títulos dos anúncios, localização aparece como
principal fator estratégico. Termos ligados a bairros valorizados e
palavras como "praia", "vista" e "beach" são frequentemente utilizados
como diferencial competitivo.

Devido à presença de valores extremos, a mediana foi utilizada como
principal medida de tendência central para comparação entre bairros,
oferecendo uma visão mais robusta do comportamento típico dos preços.

------------------------------------------------------------------------

## Conclusão

O mercado de Airbnb no Rio de Janeiro apresenta forte concentração em
áreas turísticas, alta variação de preços e padrão de distribuição
compatível com mercados imobiliários. A localização permanece como
principal determinante estratégico na formação de valor dos anúncios.

------------------------------------------------------------------------

**Fonte dos dados:** https://insideairbnb.com/
