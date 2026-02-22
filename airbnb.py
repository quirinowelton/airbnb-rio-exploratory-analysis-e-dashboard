#%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from wordcloud import WordCloud, STOPWORDS
import re

df = pd.read_csv("listings.csv", sep=",", encoding="UTF-8")

# %%
# Número de variáveis e formato do DataFrame
df.info()

# %%
# Como as colunas "license" e "neighbourhood_group" estão vazias, serão removidas do DataFrame
df = df.drop(["neighbourhood_group", "license"], axis=1)

# %%
# Algumas variáveis apresentam número diferente de observações.
# Vamos verificar a presença de valores NaN
df.isnull().sum()

# Valores NaN:
# host_name = 11
# price = 4398
# last_review = 9186
# reviews_per_month = 9186

# %%
# Verificando se os valores nulos em last_review são realmente ausências
# ou se indicam que o anúncio nunca recebeu avaliações
reviews = df[df["last_review"].isnull()]
reviews_verdadeiramente_nulos = reviews[reviews["number_of_reviews"] >= 1]

# Todos os last_review nulos correspondem a anúncios sem avaliações

# %%
# Analisando valores nulos em host_name
host_name = df[df["host_name"].isnull()]

# Como são poucos valores ausentes e os bairros já estão representados por outros anúncios,
# optamos por excluir essas linhas
df.dropna(subset='host_name', inplace=True)

# %%
# Analisando valores nulos em price
price = df[df["price"].isnull()]

# As demais colunas estão corretas.
# Ao remover as linhas com price nulo, perdemos aproximadamente 10,21% da base.
# Por questão de padronização e consistência nas análises, esses registros serão removidos.
df.dropna(subset='price', inplace=True)

# %%
# Com os dados padronizados, iniciamos as análises exploratórias
df[["price", "minimum_nights", "number_of_reviews", "reviews_per_month",
    "calculated_host_listings_count", "availability_365",
    "number_of_reviews_ltm"]].describe()

# Análise inicial:
# Price: média de 717,65 reais por noite, mínimo de 30 reais e máximo de 500.000 reais.
# Minimum_nights: média entre 3 e 4 noites por estadia, mínimo de 1 noite.
# Number_of_reviews: média de 27,45 avaliações, mínimo de 0 e máximo de 760.
# Reviews_per_month: média de 1,2 avaliações por mês, mínimo de 0 e máximo de 15.
# Calculated_host_listings_count: média de 10,23 anúncios por host, mínimo de 1 e máximo de 232 anúncios de um único host.
# Availability_365: média de 206,9 dias disponíveis por ano, mínimo de 0 e máximo de 365 dias.
# Number_of_reviews_ltm: média de 9,58 avaliações nos últimos 12 meses, mínimo de 0 e máximo de 163.

# %%
df[["price", "minimum_nights", "number_of_reviews", "reviews_per_month",
    "calculated_host_listings_count", "availability_365",
    "number_of_reviews_ltm"]].hist(bins=7, figsize=(15,10))

# %%
# Boxplot para visualizar a distribuição de preços

plt.figure(figsize=(8,5))
plt.boxplot(df['price'])
plt.ylabel('Preço')
plt.title('Boxplot - Distribuição de Preços')
plt.show()

# %%
# Definiu-se um teto analítico com base na observação do mercado,
# limitando os valores a 60.000 reais por noite.
# Imóveis acima desse valor não possuem avaliações nos últimos 12 meses.
df_new = df[df['price'] <= 60000.0]

# %%
# A distribuição original apresentou forte assimetria à direita.
# Após aplicar transformação logarítmica, observou-se comportamento próximo ao normal,
# indicando padrão log-normal típico do mercado imobiliário.

plt.figure(figsize=(8,5))
sns.histplot(np.log(df['price']), bins=50)
plt.title("Distribuição Log do Preço")
plt.show()

# %%
valores_log = [4,5,6,7,8,9,10,12]

for v in valores_log:
    print(f"log={v} → preço≈ {np.exp(v):.2f}")

# O gráfico concentra-se entre ~5 e ~6.5 na escala log,
# com leve cauda à direita. Isso indica que os preços mais frequentes
# estão aproximadamente entre 148 e 403 reais.

# %%
# 10 maiores e 10 menores preços
df_new['price'].sort_values(ascending=False).head(10)
df_new['price'].sort_values(ascending=False).tail(10)

# %%
df_new['faixa_preco'] = pd.qcut(
    df_new['price'],
    q=[0, 0.25, 0.50, 0.75, 0.99, 1],
    labels=['Baixo', 'Médio', 'Alto', 'Muito Alto', 'Luxo Extremo']
)

df_new.groupby('faixa_preco')['price'].count()

# As faixas apresentam distribuição relativamente equilibrada,
# com exceção de "Luxo Extremo", que representa apenas pequena parcela dos anúncios.

# %%
df_new['room_type'].value_counts(normalize=True)

# Observa-se que aproximadamente 80,9% são imóveis inteiros
# e cerca de 18% correspondem a quartos privados, compartilhados ou de hotel.

# %%
# Top 10 bairros com maior número de anúncios
top_neighbourhood = (
    df_new['neighbourhood']
    .value_counts(normalize=True)
    .head(10)
)

plt.figure(figsize=(10,6))

ax = sns.barplot(
    x=top_neighbourhood.values,
    y=top_neighbourhood.index
)

for i, v in enumerate(top_neighbourhood.values):
    ax.text(v, i, f'{v*100:.1f}%', va='center')

plt.xlabel('Proporção')
plt.ylabel('Bairro')
plt.title('Top 10 Bairros por Proporção de Anúncios')

plt.show()

# %%
# Análise dos bairros com imóveis de luxo extremo
luxo_extremo = df_new[df_new['faixa_preco'] == 'Luxo Extremo']

top5_bairros_luxuosos = (
    luxo_extremo['neighbourhood']
    .value_counts(normalize=True)
    .head()
    .reset_index()
)

top5_bairros_luxuosos.columns = ['neighbourhood', 'proporcao']

plt.figure(figsize=(8,5))
ax = sns.barplot(data=top5_bairros_luxuosos, x='neighbourhood', y='proporcao')

for p in ax.patches:
    ax.annotate(f'{p.get_height():.2%}',
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='bottom')

plt.xticks(rotation=45)
plt.show()

# %%
# Mapa de correlação
# Observam-se correlações positivas relevantes entre:
# number_of_reviews_ltm, number_of_reviews e reviews_per_month,
# o que é esperado, pois todas estão relacionadas ao volume de avaliações.

corr = df_new.corr(numeric_only=True)

plt.figure(figsize=(12,8), dpi=600)
sns.heatmap(corr,
            cmap=plt.cm.coolwarm,
            vmax=1,
            vmin=-1,
            center=0,
            square=True,
            linewidths=.5,
            annot=True,
            fmt='.2f',
            annot_kws={'size':12},
            cbar_kws={"shrink":0.50})

plt.title('Matriz de Correlações', fontsize=14)
plt.tight_layout()
plt.xticks(rotation=45, ha='right')
plt.show()

# %%
# Nuvem de palavras da variável "name"

text = " ".join(df['name'].dropna().astype(str))
text = text.lower()
text = re.sub(r'[^a-zà-ú\s]', '', text)

stopwords = set(STOPWORDS)
stopwords.update(['rio', 'janeiro', 'apartment', 'apartamento', 'para', 'da','em','de'])

wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white',
    stopwords=stopwords
).generate(text)

plt.figure(figsize=(12,6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# A localização é o principal fator de marketing.
# Observa-se que bairros nobres aparecem com maior frequência nos títulos.
# Termos como "praia", "beach", "vista" e "posto" reforçam diferenciais competitivos.

# %%
# Palavras mais frequentes

words = text.split()
filtered_words = [w for w in words if w not in stopwords and len(w) > 3]

counter = Counter(filtered_words)
counter.most_common(20)

# %%
# Análise de preço máximo por bairro
bairros_max = df_new.groupby('neighbourhood')['price'].max().sort_values(ascending=False)

# Como há valores extremos elevados, utilizamos a mediana como medida de tendência central
bairros_median = df_new.groupby('neighbourhood')['price'].median().sort_values(ascending=False)

# Observa-se que, ao utilizar a mediana, os bairros mais caros mudam.
# Isso indica alta variabilidade nos preços em determinados bairros.