from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import os

current_path = os.path.join(os.path.abspath(os.curdir), 'scrapping')

url = "https://www.basketball-reference.com/playoffs/"

html = urlopen(url)
        
soup = BeautifulSoup(html, features="lxml")

# use getText()to extract the headers into a list
headers = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]

# get rows from table
rows = soup.findAll('tr')[2:]
rows_data = [[td.getText() for td in rows[i].findAll('td')]
                    for i in range(len(rows))]# if you print row_data here you'll see an empty row
# so, remove the empty row
rows_data.pop(20)# for simplicity subset the data for only 39 seasons
rows_data = rows_data[0:38]

# we're missing a column for years
# add the years into rows_data
last_year = 2020
for i in range(0, len(rows_data)):
    rows_data[i].insert(0, last_year)
    last_year -=1

# create the dataframe
nba_finals = pd.DataFrame(rows_data, columns = headers)# export dataframe to a CSV 
nba_finals.to_csv(os.path.join(current_path, "nba_finals_history.csv"), index=False)