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