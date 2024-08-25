from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import os
import warnings

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
current_path = os.path.join(os.path.abspath(os.curdir), 'scrapping')

def find_table_by_id_starting_with(soup, prefix):
    for element in soup.find_all('table'):  # True significa encontrar todas as tags
        if element.has_attr('id') and element['id'].startswith(prefix):
            return element
    return None

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
    headers.append('url')

    # Encontrar as linhas da tabela
    for _, row in enumerate(table.find_all('tr')):
        columns = row.find_all('td')
        if columns:
            th = row.find_all('th')[0]

            a = th.find('a')
            
            indexes.append([th.text.strip() for th in row.find_all('th')][0] if row else '-')

            rows_to_append = [col.text.strip() for col in columns]
            rows_to_append.append('https://fbref.com' + a['href'])

            rows.append(rows_to_append)
            

    df = pd.DataFrame(rows, columns=headers[1:], index=indexes)
    df.index.name = headers[0]

    df = df.loc[:, ~df.columns.duplicated(keep='first')]

    df = df[(df['Camp.'] == 'Campeonato Brasileiro Série A') | (df['Camp.'] == 'Campeonato Brasileiro Série B')]

    return df

def get_players_stats_from_club_df(players_df: pd.DataFrame):
    players_stats_from_club_df = pd.DataFrame()

    for index, row in players_df.iterrows():
        print(index)

        url = row['url']

        nome = '-'.join(row['Jogador'].split(' '))
        print(nome)
        url = '/'.join(url.split('/')[0:6]) + f'/scout/365_m2/Relatorio-de-Observacao-de-{nome}'

        html = urlopen(url)
            
        soup = BeautifulSoup(html, "html.parser")

        table = find_table_by_id_starting_with(soup, "scout_full")

        if table is None:
            print(nome, 'blz')
            continue

        thead = table.find('thead')

        headers = []
        rows = []
        indexes = []

        headers = [th.text.strip() for th in thead.find_all('th')] if thead else []

        # Encontrar as linhas da tabela
        for i, row_ in enumerate(table.find_all('tr')):
            columns = row_.find_all('td')
            if columns:
                index_ = [th.text.strip() for th in row_.find_all('th')][0] if row_ else '-'
                indexes.append(index_)                
                rows.append([col.text.strip() for col in columns])

        # # Criar o DataFrame
        df = pd.DataFrame(rows, columns=headers[2:], index=indexes)
        df.index.name = headers[1]

        df = df[df['Por 90'] != '']

        flat_df = pd.DataFrame()
        for index_, row_ in df.iterrows():
            flat_df[f'{index_}_por_90'] = [row_['Por 90']]
            flat_df[f'{index_}_percentil'] = row_['Percentil']
    
        df = pd.concat([row.to_frame().T, flat_df], axis=1)
        df.to_csv(f'{nome}.csv')

        players_stats_from_club_df = pd.concat([players_stats_from_club_df, df], axis=0)


    return players_stats_from_club_df



def get_players_stats_df(clubs_df: pd.DataFrame):
    player_stats_df = pd.DataFrame()

    for index, row in clubs_df.iloc[1:2].iterrows():
        clube = index
        url = row['url']

        html = urlopen(url)
                
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find('table', {'id': 'comps_fa_club_league'})

        # Encontrar os cabeçalhos da tabela
        thead = table.find('tbody')
        tr = thead.find('tr')
        td = tr.find('td')
        a = td.find('a')

        url_team = 'https://fbref.com' + a['href']

        html = urlopen(url_team)
                
        soup = BeautifulSoup(html, "html.parser")

        table = find_table_by_id_starting_with(soup, 'stats_standard')

        thead = table.find('thead')
        tbody = table.find('tbody')
        tr = thead.find_all('tr')[-1]

        headers = []    
        rows = []
        indexes = []

        # Encontrar os cabeçalhos da tabela
        headers = [th.text.strip() for th in tr.find_all('th')] if thead else []
        headers.append('url')

        for _, row in enumerate(tbody.find_all('tr')):
            columns = row.find_all('td')
            if columns:
                th = row.find_all('th')[0]

                a = th.find('a')
                
                indexes.append([th.text.strip() for th in row.find_all('th')][0] if row else '-')

                rows_to_append = [col.text.strip() for col in columns]
                rows_to_append.append('https://fbref.com' + a['href'])

                rows.append(rows_to_append)

        df = pd.DataFrame(rows, columns=headers[1:], index=indexes)
        df.index.name = headers[0]

        df = df.loc[:, ~df.columns.duplicated(keep='first')]

        df = df[['Nação', 'Pos.', 'Idade', 'url']]
        df = df.reset_index()
        df['clube'] = clube

        players_stats_from_club_df = get_players_stats_from_club_df(df)

        player_stats_df = pd.concat([player_stats_df, players_stats_from_club_df], axis=0)


        break
    
    return player_stats_df

clubs_df = get_clubs_df()

player_stats_df = get_players_stats_df(clubs_df)

player_stats_df.to_csv('player_stats_df.csv', index=False)







