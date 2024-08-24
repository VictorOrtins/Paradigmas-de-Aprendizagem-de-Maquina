from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import os

current_path = os.path.join(os.path.abspath(os.curdir), 'scrapping')

def get_clubs_df():
    url = "https://fbref.com/pt/pais/clubes/BRA/Clubes-de-Futebol-de-Brazil"

    html = urlopen(url)
            
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find('table', {'id': 'clubs'})

    # Listas para armazenar os dados
    headers = []
    rows = []
    indexes = []

    # Encontrar os cabeçalhos da tabela
    thead = table.find('thead')
    headers = [th.text.strip() for th in thead.find_all('th')] if thead else []

    # Encontrar as linhas da tabela
    for _, row in enumerate(table.find_all('tr')):
        columns = row.find_all('td')
        if columns:
            indexes.append([th.text.strip() for th in row.find_all('th')][0] if row else '-')
            rows.append([col.text.strip() for col in columns])

    df = pd.DataFrame(rows, columns=headers[1:], index=indexes)
    df.index.name = headers[0]

    df = df.loc[:, ~df.columns.duplicated(keep='first')]

    df = df[(df['Camp.'] == 'Campeonato Brasileiro Série A') | (df['Camp.'] == 'Campeonato Brasileiro Série B')]

    return df

clubs_df = get_clubs_df()

print(clubs_df.head())


