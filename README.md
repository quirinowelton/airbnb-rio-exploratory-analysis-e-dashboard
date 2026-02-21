# Análise Exploratória --- Airbnb Rio de Janeiro

## Sobre a empresa

O Airbnb é uma plataforma digital que conecta pessoas que desejam alugar
imóveis por temporada a viajantes do mundo todo. O modelo de negócio é
baseado na economia compartilhada, permitindo que anfitriões anunciem
casas, apartamentos ou quartos e recebam hóspedes por períodos curtos.

O Inside Airbnb disponibiliza dados públicos extraídos da plataforma,
organizados por cidade. Esses dados permitem análises sobre preços,
localização, perfil dos anúncios e características das acomodações.

Fonte: https://insideairbnb.com/

![logo_airbnb](/airbnb.jpg)
------------------------------------------------------------------------

## Sobre a base de dados

Neste projeto utilizei a base referente ao Rio de Janeiro, contendo
informações sobre anúncios ativos na cidade.

O dataset inclui variáveis como:

-   `id` -- identificador do anúncio\
-   `name` -- nome do anúncio\
-   `host_id` -- identificador do anfitrião\
-   `neighbourhood_group` e `neighbourhood` -- localização do imóvel\
-   `latitude` e `longitude` -- coordenadas geográficas\
-   `room_type` -- tipo de acomodação (casa inteira, quarto privado,
    etc.)\
-   `price` -- preço por noite\
-   `minimum_nights` -- número mínimo de noites\
-   `number_of_reviews` -- quantidade de avaliações\
-   `availability_365` -- disponibilidade ao longo do ano

A base é composta majoritariamente por variáveis categóricas e
numéricas, permitindo análises de distribuição, comparação entre bairros
e avaliação de padrões de preço.

------------------------------------------------------------------------

## Objetivo da análise

A análise exploratória teve como foco:

-   Entender a distribuição de preços na cidade\
-   Identificar bairros com maior concentração de anúncios\
-   Comparar tipos de acomodação\
-   Avaliar a presença de outliers\
-   Explorar possíveis relações entre variáveis

O trabalho envolveu limpeza dos dados, tratamento de valores ausentes e
análise estatística descritiva, com visualizações para apoiar a
interpretação.
