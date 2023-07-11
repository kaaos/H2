import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches

## ***Extração e Modelagem***

# Base de dados: clientesH2.csv

# Base de clientes H2
clientesH2 = pd.read_csv(r'/content/drive/MyDrive/Colab Notebooks/H2/clientesH2.csv')
print(clientesH2.head(2))

type(clientesH2)

# Limpa colunas indesejadas
clientesH2 = clientesH2.drop(['data_cadastro', 'cidade'], axis=1)
print(clientesH2.head(2))

print(clientesH2['data_nascimento'].dtype)

# Formata a data_nascimento
clientesH2['data_nascimento'] = pd.to_datetime(clientesH2['data_nascimento'])
clientesH2 = clientesH2.dropna(subset=['data_nascimento']) 

# Dicionário para faixa de idade das gerações
gen_dict = {(1925, 1940): 'Veteranos',
            (1941, 1959): 'Baby Boomers',
            (1960, 1979): 'Geração X',
            (1980, 1995): 'Geração Y',
            (1996, 2009): 'Geração Z',
            (2010, 2025): 'Geração Alpha'}

# Mapeia ano de nascimento para geração
clientesH2['geracao'] = clientesH2['data_nascimento'].astype(str).str[:4].astype(int).apply(lambda year: next((v for k, v in gen_dict.items() if year in range(k[0], k[1]+1)), 'Outra geração'))

print(clientesH2.head(2))

# Ordena colunas
clientesH2 = clientesH2.loc[:, ['id', 'data_nascimento', 'sigla', 'geracao', 'sexo']]
print(clientesH2.head(2))

# Base de dados: resultados.csv

# Resultados B/R/W 
resultados = pd.read_csv(r'/content/drive/MyDrive/Colab Notebooks/H2/resultados.csv')
print(resultados.head(2))

type(resultados)

print(resultados['data_acesso'].dtype)

# Formata  data_acesso
resultados['data_acesso'] = pd.to_datetime(resultados['data_acesso'])
resultados = resultados.dropna(subset=['data_acesso']) 

# Ordena colunas
resultados = resultados.loc[:, ['clientes_id', 'data_acesso', 'buyin', 'rake', 'winning']]
print(resultados.head(2))

#Merge base de dados

# Merge dos dois dataframes com base em clientes_id e id
mergedf_CR = pd.merge(resultados, clientesH2, left_on='clientes_id', right_on='id')
print(mergedf_CR.head(2))

mergedf_CR = mergedf_CR.drop(['id'], axis=1)
print(mergedf_CR.head(3))

#mergedf_CR

# Cria mergedf_CR CSV
##mergedf_CR.to_csv('mergedf_CR.csv')

# ***Dataset***

# Define o Dataset como df_h2
df_h2 = mergedf_CR

df_h2 = df_h2.round(2)

# Check
#df_h2

# Cria CSV df_h2 CSV
#df_h2.to_csv('df_h2.csv')

# ***Buy-in por mês, ano e geração/ano***

# Formata buyin_dia_mes 

buyin_dia_mes = df_h2
buyin_dia_mes = df_h2.drop(['clientes_id', 'rake', 'winning', 'data_nascimento', 'sigla', 'geracao', 'sexo'], axis=1)

# Extrai ano e mes em colunas separadas
buyin_dia_mes['dia'] = buyin_dia_mes['data_acesso'].dt.day
buyin_dia_mes['mes'] = buyin_dia_mes['data_acesso'].dt.month
buyin_dia_mes['ano'] = buyin_dia_mes['data_acesso'].dt.year

# Check
print(buyin_dia_mes) 

# Calcula buyin por mês
buyin_mes = buyin_dia_mes.groupby(pd.Grouper(key='data_acesso', freq='M'))['buyin'].sum().round(2)
print(buyin_mes)

# Formata buyin_mes
buyin_mes = buyin_mes.reset_index()

# Extrai ano e mes em colunas separadas
buyin_mes['mes'] = buyin_mes['data_acesso'].dt.month
buyin_mes['ano'] = buyin_mes['data_acesso'].dt.year
#buyin_mes = buyin_mes.drop(['data_acesso'], axis=1)
# Check
print(buyin_mes) 

# Cria CSV buyin_por_mes
buyin_mes.to_csv('buyin_mes.csv')

# Calcula buyin por ano
buyin_ano = df_h2.groupby(pd.Grouper(key='data_acesso', freq='Y'))['buyin'].sum().round(2)

# Formata buyin_ano 
buyin_ano = buyin_ano.reset_index()

# Extrai ano e mes em colunas separadas
buyin_ano['ano'] = buyin_ano['data_acesso'].dt.year
#buyin_ano = buyin_ano.drop(['data_acesso'], axis=1)
# Check
print(buyin_ano)

# Cria CSV buyin_por_ano
buyin_ano.to_csv('buyin_ano.csv')

# Agrupa geração e ano, calcula soma do buyin
buyin_gen_ano = df_h2.groupby(['geracao', df_h2['data_acesso'].dt.year])['buyin'].sum()

# Exibir o resultado
print(buyin_gen_ano)

# Formata 
buyin_gen_ano = buyin_gen_ano.reset_index()
buyin_gen_ano = buyin_gen_ano.rename(columns={'data_acesso': 'ano'})

print(buyin_gen_ano)

# Cria CSV buyin_geração_por_ano
buyin_gen_ano.to_csv('buyin_gen_ano.csv')

# ***Rake por mês, ano e geração/ano***

# Formata rake_dia_mes 

rake_dia_mes = df_h2
rake_dia_mes = df_h2.drop(['clientes_id', 'buyin', 'winning', 'data_nascimento', 'sigla', 'geracao', 'sexo'], axis=1)

# Extrai ano e mes em colunas separadas
rake_dia_mes['dia'] = rake_dia_mes['data_acesso'].dt.day
rake_dia_mes['mes'] = rake_dia_mes['data_acesso'].dt.month
rake_dia_mes['ano'] = rake_dia_mes['data_acesso'].dt.year
#buyin_mes = buyin_mes.drop(['data_acesso'], axis=1)

# Check
print(rake_dia_mes) 

# Calcula rake por mês
rake_mes = df_h2.groupby(pd.Grouper(key='data_acesso', freq='M'))['rake'].sum().round(2)
#print(rake_mes)

# Formata rake_mes
rake_mes = rake_mes.reset_index()

# Extrai ano e mes em colunas separadas
rake_mes['mes'] = rake_mes['data_acesso'].dt.month
rake_mes['ano'] = rake_mes['data_acesso'].dt.year
#rake_mes = rake_mes.drop(['data_acesso'], axis=1)
# Check
print(rake_mes) 

# Cria rake_por_mes CSV
#rake_por_mes.to_csv('rake_por_mes.csv')

# Calcula rake por ano
rake_ano = df_h2.groupby(pd.Grouper(key='data_acesso', freq='Y'))['rake'].sum().round(2)
#print(rake_ano)

# Formata rake_ano
rake_ano = rake_ano.reset_index()

# Extrai ano 
rake_ano['ano'] = rake_ano['data_acesso'].dt.year
#rake_ano = rake_ano.drop(['data_acesso'], axis=1)

# Check
print(rake_ano)

# Cria rake_por_ano CSV
#rake_por_ano.to_csv('rake_por_ano.csv')

# Agrupa geração e ano, calcula soma do rake
rake_gen_ano = df_h2.groupby(['geracao', df_h2['data_acesso'].dt.year])['rake'].sum()


print(rake_gen_ano)

# Formata 
rake_gen_ano = rake_gen_ano.reset_index()
rake_gen_ano = rake_gen_ano.rename(columns={'data_acesso': 'ano'})
print(rake_gen_ano)

# ***Winning por mês, ano e geração/ano***

# Formata winning_dia_mes 

winning_dia_mes = df_h2
winning_dia_mes = df_h2.drop(['clientes_id', 'rake', 'buyin', 'data_nascimento', 'sigla', 'geracao', 'sexo'], axis=1)

# Extrai ano e mes em colunas separadas
winning_dia_mes['dia'] = winning_dia_mes['data_acesso'].dt.day
winning_dia_mes['mes'] = winning_dia_mes['data_acesso'].dt.month
winning_dia_mes['ano'] = winning_dia_mes['data_acesso'].dt.year

# Check
print(winning_dia_mes) 

# Calcula winning por mês
winning_mes = df_h2.groupby(pd.Grouper(key='data_acesso', freq='M'))['winning'].sum()

# Formata winning_mes
winning_mes = winning_mes.reset_index()

# Extrai ano e mes em colunas separadas
winning_mes['mes'] = winning_mes['data_acesso'].dt.month
winning_mes['ano'] = winning_mes['data_acesso'].dt.year
#winning_mes = winning_mes.drop(['data_acesso'], axis=1)

# Check
print(winning_mes)

# Cria CSV winning_por_mes
#winning_por_mes.to_csv('winning_por_mes.csv')

# Calcula winning por ano
winning_ano = df_h2.groupby(pd.Grouper(key='data_acesso', freq='Y'))['winning'].sum()

# Formata winning_ano
winning_ano = winning_ano.reset_index()

# Extrai ano 
winning_ano['ano'] = winning_ano['data_acesso'].dt.year
winning_ano = winning_ano.drop(['data_acesso'], axis=1)

# Check
print(winning_ano)

# Cria CSV winning_por_ano
#winning_por_ano.to_csv('winning_por_ano.csv')

# Agrupa geração e ano, calcula soma do winning
winning_geracao_ano = df_h2.groupby(['geracao', df_h2['data_acesso'].dt.year])['winning'].sum()

#print(winning_geracao_ano)

# Formata 
winning_geracao_ano = winning_geracao_ano.reset_index()
winning_geracao_ano = winning_geracao_ano.rename(columns={'data_acesso': 'ano'})
print(winning_geracao_ano)

# Cria CSV winning_por_geracao_por_ano
#winning_por_geracao_e_ano.to_csv('winning_por_geracao_por_ano.csv')

# ***Gráfico buy-in por ano e mês***

# Carrega e formata dado
df_buyin_ano = pd.DataFrame(buyin_mes, columns=['data_acesso', 'buyin'])
df_buyin_ano['data_acesso'] = pd.to_datetime(df_buyin_ano['data_acesso'])

# Canvas e eixos
fig, ax = plt.subplots(figsize=(12, 6))

# Agrupa data por ano
year_grouped = df_buyin_ano.groupby(df_buyin_ano['data_acesso'].dt.year)

# Define o mapa de cor
colors = {'2020': 'tab:red', '2021': 'tab:orange', '2022': 'tab:green', '2023': 'tab:blue'}

# Desenha barras
for name, group in year_grouped:
    ax.bar(group['data_acesso'], group['buyin'], width=20, color=colors[str(name)], alpha=0.7, label=f'{name} - R${group["buyin"].sum():,.2f}')

# Classifica etiquetas
ax.set_xlabel('Mês')
ax.set_ylabel('Buy-in total')

# Ajusta título
ax.set_title('Buy-in total por mês e ano')

# Legenda
ax.legend(fontsize='large', bbox_to_anchor=(0.3, 0.975))

# Set y-axis range to start at 0
ax.set_ylim(bottom=0)

# Edit the y-axis tick labels to show values in millions
import matplotlib.ticker as ticker
formatter = ticker.StrMethodFormatter('R${x:,.2f}')
ax.yaxis.set_major_formatter(formatter)

# Grid
ax.grid(axis='y')

# Display the plot
plt.show()
print(buyin_mes)

# ***Gráfico rake por ano e mês***

# Carrega e formata dado
df_rake_ano = pd.DataFrame(rake_mes, columns=['data_acesso', 'rake'])
df_rake_ano['data_acesso'] = pd.to_datetime(df_rake_ano['data_acesso'])

# Canvas e eixos
fig, ax = plt.subplots(figsize=(12, 6))

# Agrupa data por ano
year_grouped = df_rake_ano.groupby(df_rake_ano['data_acesso'].dt.year)

# Define o mapa de cor
colors = {'2020': 'tab:red', '2021': 'tab:orange', '2022': 'tab:green', '2023': 'tab:blue'}

# Desenha barras
for name, group in year_grouped:
    ax.bar(group['data_acesso'], group['rake'], width=20, color=colors[str(name)], alpha=0.7, label=f'{name} - R${group["rake"].sum():,.2f}')

# Classifica etiquetas
ax.set_xlabel('Mês')
ax.set_ylabel('Rake total')

# Ajusta título
ax.set_title('Rake total por mês e ano')

# Legenda
ax.legend(fontsize='large', bbox_to_anchor=(0.3, 0.975))

# Set y-axis range to start at 0
ax.set_ylim(bottom=0)

# Edit the y-axis tick labels to show values in millions
import matplotlib.ticker as ticker
formatter = ticker.StrMethodFormatter('R${x:,.2f}')
ax.yaxis.set_major_formatter(formatter)

# Grid
ax.grid(axis='y')

# Display the plot
plt.show()
print()
print(rake_mes)

# ***Gráfico winning por ano e mês***

# Load and format data
df_win_ano = pd.DataFrame(winning_mes, columns=['data_acesso', 'winning'])
df_win_ano['data_acesso'] = pd.to_datetime(df_win_ano['data_acesso'])

# Canvas and axes
fig, ax = plt.subplots(figsize=(12, 6))

# Define the color map
colors = {'2020': 'tab:red', '2021': 'tab:orange', '2022': 'tab:green', '2023': 'tab:blue'}

# Group the data by year
year_grouped = df_win_ano.groupby(df_win_ano['data_acesso'].dt.year)

# Draw bars
for name, group in year_grouped:
    ax.bar(group['data_acesso'], group['winning'], width=20, color=colors[str(name)], alpha=0.7, label=f'{name} - R${group["winning"].sum():,.2f}')

# Format x-axis labels
ax.set_xlabel('Mês')
ax.set_xticks(df_win_ano['data_acesso'].unique())
ax.set_xticklabels(df_win_ano['data_acesso'].dt.strftime('%Y-%m-%d'))

# Rotate x-axis labels
plt.xticks(rotation=90)

# Format y-axis labels
ax.set_ylabel('Winning total')
formatter = ticker.StrMethodFormatter('R${x:,.2f}')
ax.yaxis.set_major_formatter(formatter)

# Set y-axis limits to show negative and positive values
ax.set_ylim(bottom=df_win_ano['winning'].min()*1.1, top=df_win_ano['winning'].max()*1.1)

# Set title and legend
ax.set_title('Winning total por mês e ano')
ax.legend(fontsize='large', bbox_to_anchor=(0.3, 0.28))

# Add grid
ax.grid(axis='y')

# Display the plot
plt.show()
print(winning_mes)

# ***Gráfico buy-in por geração/ano***

# Agrupa dataframe por geração e ano, calcula o buy-in the cada 
bpie_geracao_ano = buyin_gen_ano.groupby(['geracao', 'ano'])['buyin'].sum()

# Cria dicionário de dado para cada ano
ano_datab = {}

# Varre os grupos e popula o dicionário
for gen, ano in bpie_geracao_ano.index:
    buyin = bpie_geracao_ano[(gen, ano)]
    if ano not in ano_datab:
        ano_datab[ano] = {gen: buyin}
    else:
        ano_datab[ano][gen] = buyin

# Lista de cores para pie chart
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']

# Varre anos e cria pie chart para cada ano
for ano in ano_datab:
    datab = ano_datab[ano]
    values = list(datab.values())
    formatted_values = [f"R$ {value:,.2f}".replace(',', ';').replace('.', ',').replace(';', '.') for value in values]
    labels = list(datab.keys())
    legend_labels = [f"{label}: {formatted_values[i]}" for i, label in enumerate(labels)]
    plt.figure()
    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title(f'Buy-in total por geração em {ano}')
    plt.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1))
    plt.show()
#

## **Rake por geração/ano**

# Agrupa dataframe por geração e ano, calcula o buy-in the cada 
rpie_geracao_ano = rake_gen_ano.groupby(['geracao', 'ano'])['rake'].sum()

# Cria dicionário de dado para cada ano
ano_datar = {}

# Varre os grupos e popula o dicionário
for gen, ano in rpie_geracao_ano.index:
    buyin = rpie_geracao_ano[(gen, ano)]
    if ano not in ano_datar:
        ano_datar[ano] = {gen: rake}
    else:
        ano_datar[ano][gen] = rake

# Lista de cores para pie chart
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']

# Varre anos e cria pie chart para cada ano
for ano in ano_datar:
    datar = ano_datar[ano]
    values = list(datar.values())
    formatted_values = [f"R$ {value:,.2f}".replace(',', ';').replace('.', ',').replace(';', '.') for value in values]
    labels = list(datar.keys())
    legend_labels = [f"{label}: {formatted_values[i]}" for i, label in enumerate(labels)]
    plt.figure()
    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title(f'Rake total por geração em {ano}')
    plt.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1))
    plt.show()


# Agrupa dataframe por geração e ano, calcula o buy-in the cada 
rpie_geracao_ano = buyin_gen_ano.groupby(['geracao', 'ano'])['buyin'].sum()

# Cria dicionário de dado para cada ano
ano_data = {}

# Varre os grupos e popula o dicionário
for gen, ano in bpie_geracao_ano.index:
    buyin = bpie_geracao_ano[(gen, ano)]
    if ano not in ano_data:
        ano_data[ano] = {gen: buyin}
    else:
        ano_data[ano][gen] = buyin

# Lista de cores para pie chart
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']

# Varre anos e cria pie chart para cada ano
for ano in ano_data:
    data = ano_data[ano]
    values = list(data.values())
    formatted_values = [f"R$ {value:,.2f}".replace(',', ';').replace('.', ',').replace(';', '.') for value in values]
    labels = list(data.keys())
    legend_labels = [f"{label}: {formatted_values[i]}" for i, label in enumerate(labels)]
    plt.figure()
    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title(f'Buy-in total por geração em {ano}')
    plt.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1))
    plt.show()
