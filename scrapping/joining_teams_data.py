import pandas as pd
import os

current_path = os.path.join(os.path.abspath(os.curdir), 'scrapping')

csv_dir = os.listdir(os.path.join(current_path, 'tables'))
csv_dir = [path for path in csv_dir if path.endswith('.csv')]

player_stats = pd.DataFrame()

for csv_path in csv_dir:
    team_df = pd.read_csv(os.path.join(current_path, 'tables', csv_path))
    player_stats = pd.concat([player_stats, team_df])

player_stats.drop(columns=['Unnamed: 0'], inplace=True)

print(len(player_stats.columns))

columns = player_stats.columns
first_columns = ['Jogador','Nação','Pos.','Idade','url','clube']
columns = list(set(set(columns) - set(first_columns)))

player_stats = player_stats[first_columns + columns]

print(len(player_stats.columns))

player_stats.to_csv(os.path.join(current_path, 'player_stats2.csv'))