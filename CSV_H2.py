
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# @VSCODE@ carrega CSV
resultados = pd.read_csv(r'C:\Users\vraja\Documents\Dev\H2\resultado.csv')
clientesH2 = pd.read_csv(r'C:\Users\vraja\Documents\Dev\H2\clientes.csv')
merged_data_CR = pd.read_csv(r'C:\Users\vraja\Documents\Dev\H2\merged_data.csv')

# Base de clientes H2
#clientesH2 = pd.read_csv(r'/content/drive/MyDrive/Colab Notebooks/H2/clientesH2.csv')

#print(clientesH2.head())

# Resultados B/R/W dos clientes H2
resultados = pd.read_csv(r'/content/drive/MyDrive/Colab Notebooks/H2/resultados.csv')

#print(resultados.head())
 
# Dataframe com dados de clientes e resultados unidos
merged_data_CR = pd.read_csv(r'/content/drive/MyDrive/Colab Notebooks/H2/merged_data.csv')

#print(merged_data_CR.head())

# Limpeza de dados clientesH2
clientesH2 = clientesH2.drop(['data_cadastro', 'cidade'], axis=1)
clientesH2 = clientesH2.sort_values(['id', 'data_nascimento', 'sigla'])

# Limpeza de dados merged_data
merged_data_CR = merged_data_CR.drop(['Unnamed: 0', 'id', 'data_cadastro', 'cidade', 'sigla'], axis=1)
merged_data_CR = merged_data_CR.dropna()

# Formata a data de acesso
merged_data_CR['data_acesso'] = pd.to_datetime(merged_data_CR['data_acesso'])
merged_data_CR = merged_data_CR.dropna(subset=['data_acesso']) 

# Formata data_nascimento 
merged_data_CR['data_nascimento'] = pd.to_datetime(merged_data_CR['data_nascimento']) 
merged_data_CR = merged_data_CR.dropna(subset=['data_nascimento'])

# Criar nova coluna ano, mês e dia
merged_data_CR['ano_acesso'] = merged_data_CR['data_acesso'].dt.year
merged_data_CR['mes_acesso'] = merged_data_CR['data_acesso'].dt.month
merged_data_CR['dia_acesso'] = merged_data_CR['data_acesso'].dt.day

# Dicionário para faixa de idade das gerações
gen_dict = {(1925, 1940): 'Veteranos',
            (1941, 1959): 'Baby Boomers',
            (1960, 1979): 'Geração X',
            (1980, 1995): 'Geração Y',
            (1996, 2009): 'Geração Z',
            (2010, 2025): 'Geração Alpha'}

# Mapeia ano de nascimento para geração
merged_data_CR['geracao'] = merged_data_CR['data_nascimento'].astype(str).str[:4].astype(int).apply(lambda year: next((v for k, v in gen_dict.items() if year in range(k[0], k[1]+1)), 'Outra geração')) #!Verificar

# Calcula rake por mês
rake_por_mes = merged_data_CR.groupby(pd.Grouper(key='data_acesso', freq='M'))['rake'].sum().round(2)

print(rake_por_mes)

# Cria rake_por_mes CSV
rake_por_mes.to_csv('rake_por_mes.csv')

# Calcula rake por ano
rake_por_ano = merged_data_CR.groupby(pd.Grouper(key='data_acesso', freq='Y'))['rake'].sum().round(2)

print(rake_por_ano)

# Cria rake_por_ano CSV
rake_por_ano.to_csv('rake_por_ano.csv')

# check
print(merged_data_CR.head())
 
# Rake por ano e mês
rake_por_ano_e_mes = merged_data_CR.groupby([merged_data_CR['data_acesso'].dt.year, merged_data_CR['data_acesso'].dt.month])['rake'].sum().round(2)

# Cria CSV rake_por_ano_e_mes
rake_por_ano_e_mes.to_csv('rake_por_geracao_por_ano.csv')

# Agrupa geração e ano, calcula soma do rake
rake_por_geracao_e_ano = merged_data_CR.groupby(['geracao', 'ano_acesso'])['rake'].sum().round(2)


# Check

# Calcula buyin por mês
buyin_por_mes = merged_data_CR.groupby(pd.Grouper(key='data_acesso', freq='M'))['buyin'].sum().round(2)

# Cria CSV buyin_por_mes
buyin_por_mes.to_csv('buyin_por_mes.csv')

# Calcula buyin por ano
buyin_por_ano = merged_data_CR.groupby(pd.Grouper(key='data_acesso', freq='Y'))['buyin'].sum().round(2)

print(buyin_por_ano)

# Cria CSV buyin_por_ano
buyin_por_ano.to_csv('buyin_por_ano.csv')

# Buyin por ano e mês
buyin_por_ano_e_mes = merged_data_CR.groupby([merged_data_CR['data_acesso'].dt.year, merged_data_CR['data_acesso'].dt.month])['buyin'].sum().round(2)

# Agrupa geração e ano, calcula soma do buyin
buyin_por_geracao_por_ano = merged_data_CR.groupby(['geracao', 'ano_acesso'])['buyin'].sum().round(2)

# Exibir o resultado

# Cria CSV buyin_geração_por_ano
buyin_por_geracao_por_ano.to_csv('buyin_por_geracao_por_ano.csv')

# Calcula winning por mês
winning_por_mes = merged_data_CR.groupby(pd.Grouper(key='data_acesso', freq='M'))['winning'].sum().round(2)

# Cria CSV winning_por_mes
winning_por_mes.to_csv('winning_por_mes.csv')

# Calcula winning por ano
winning_por_ano = merged_data_CR.groupby(pd.Grouper(key='data_acesso', freq='Y'))['winning'].sum().round(2)

# Cria CSV winning_por_ano
winning_por_ano.to_csv('winning_por_ano.csv')

# Cria winning por ano e mês
winning_por_ano_e_mes = merged_data_CR.groupby([merged_data_CR['data_acesso'].dt.year, merged_data_CR['data_acesso'].dt.month])['winning'].sum().round(2)

# Agrupa geração e ano, calcula soma do winning
winning_por_geracao_por_ano = merged_data_CR.groupby(['geracao', 'ano_acesso'])['winning'].sum().round(2)
