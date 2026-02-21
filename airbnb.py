#%%
import pandas as pd

df = pd.read_csv("listings.csv", sep=",", encoding= "UTF-8")
# %%
#número de variaveis e formato
df.info()

#%%Como license e neighbourhood_group se encontram vazias vou retirar do df

df = df.drop(["neighbourhood_group", "license"], axis=1)
#%% Como algumas variaveis mostram numero de observações diferentes, vamos dar uma olhada melhor em cada uma e ver se possuem valores NaN
df.isnull().sum()
#valores NaN: host_name =11, price = 4398, last_review 9186, reviews_per_month 9186

#%%Observando se as observações de last_review são nulas mesmo ou se realmente é por não ter sido tido nenhuma review
reviews = df[df["last_review"].isnull()]
reviews_verdadeiramente_nulos = reviews[reviews["number_of_reviews"] >= 1]
#Todos os last_review que sãi nulos não tiveram nenhuma review
#%%Agora observar os nulos de host_name
host_name = df[df["host_name"].isnull()]
#como são poucas valores vazios e em bairros ja representados por outras observações, vamos optar por excluir as linhas com valores de host_name faltantes
df.dropna(subset='host_name', inplace= True)
#%%Agora vamos observar os valores faltantes de price
price = df[df["price"].isnull()]
#todas as outras colunas estavam com valores corretos, e sei que retirando as linhas com price eu perco um total de 10,21% da minha base de dados. Mas para questão
#de praticidade e padranização esse valores serão retirados. Mesmo sendo possivel ainda fazer analises de outras variaveis com essas linhas, mas no final acredito que não irá influeciar muito.
df.dropna(subset='price', inplace= True)
#%% Agora com os dados padronizados vamos as analises iniciais.
df[["price", "minimum_nights", "number_of_reviews", "reviews_per_month", "calculated_host_listings_count", "availability_365", "number_of_reviews_ltm"]].describe()
#Por essa analise inicial conseguimos ver que por:
#Price: A média de preço foi de 717,65 reais por noite, sendo o minimo 30 reais e o maximo 500000 mil reais
#minimum_nights: teve a média de no minimo 3 a 4 noites no minimo por estadia, sendo o minimo 1 noite
#numero de reviews: A média do total de reviews é de 27,45 sendo o minimo 0 e o maximo 760 reviews
#review por mes: uma média de 1,2 reviews por mês sendo o minimo 0 e o maximo 15
#Calculated_host_listing_count: a média de anuncio por host é de 10,23 sendo no minimo 1 anuncio e no maximo 232 anuncios de um unico host.
#availability_365: Possui uma média de 206,90 dias disponiveis sendo o minimo 0 e o no maximo 365 dias disponiveis
#number_of_reviews_ltm: O numero de avaliações nos ultimos 12 meses teve uma média de 9.58 reviews sendo no minimo 0 e no maximo 163
#%% 
df[["price", "minimum_nights", "number_of_reviews", "reviews_per_month", "calculated_host_listings_count", "availability_365", "number_of_reviews_ltm"]].hist(bins=7, figsize=(15,10))
#%% Os apartamentos com preços de 500000 mil reais a diaria 
import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))
plt.boxplot(df['price'])
plt.ylabel('Preço')
plt.title('Boxplot - Distribuição de Preços')
plt.show()
#%% optou-se por definir um teto analítico baseado na observação de mercado atual e limitamos o valor a 60000 reais por noite.. Apartamentos com valores maiores não possuem review nos ultimos 12 meses
#dentro do valor de 50000 foi observado anuncios com até 15 reviews nos ultimos 12 meses então optamos por manter o teto em 60000
df_new = df[df['price'] <= 60000.0]

#%% A distribuição original apresentou forte assimetria à direita. Após aplicação de transformação logarítmica, observou-se comportamento aproximadamente normal, indicando que os preços seguem padrão log-normal, comum em mercados imobiliários.
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(8,5))
sns.histplot(np.log(df['price']), bins=50)
plt.title("Distribuição Log do Preço")
plt.show()
#%%
valores_log = [4,5,6,7,8,9,10,12]

for v in valores_log:
    print(f"log={v} → preço≈ {np.exp(v):.2f}")
    
 #o grafico concentrada entre ~5 e ~6.5 no log Com uma leve cauda à direita indicando que os valores mais comuns são de 148 a 403 reais
 
#%% os 10 maiores preços apartamento de luxo
df_new['price'].sort_values(ascending=False).head(10)
df_new['price'].sort_values(ascending=False).tail(10) # os 10 menores preços