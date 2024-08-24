from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import os

current_path = os.path.join(os.path.abspath(os.curdir), 'scrapping')

url = "https://fbref.com/pt/jogadores/c01c66d9/scout/365_m2/Relatorio-de-Observacao-de-Bastos"

html = urlopen(url)
        
soup = BeautifulSoup(html, "html.parser")

# use getText()to extract the headers into a list
table = soup.find('table', {'id': 'scout_full_CB'})


# Listas para armazenar os dados
headers = []
rows = []
indexes = []

# Encontrar os cabeçalhos da tabela
thead = table.find('thead')
headers = [th.text.strip() for th in thead.find_all('th')] if thead else []

# Encontrar as linhas da tabela
for i, row in enumerate(table.find_all('tr')):
    columns = row.find_all('td')
    if columns:
        index = indexes.append([th.text.strip() for th in row.find_all('th')][0] if row else '-')
        rows.append([col.text.strip() for col in columns])
    

print(headers)
print(rows)
print(indexes)
print(len(rows))
print(len(indexes))

# # Criar o DataFrame
df = pd.DataFrame(rows, columns=headers[2:], index=indexes)
df.index.name = headers[1]

df = df[df['Por 90'] != '']

print(df.iloc[7:12].head())

flat_df = pd.DataFrame()
for index, row in df.iterrows():
    flat_df[f'{index}_por_90'] = [row['Por 90']]
    flat_df[f'{index}_percentil'] = row['Percentil']

flat_df.to_csv(os.path.join(current_path, 'bastos_summary.csv'))