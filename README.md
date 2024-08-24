---

# Projeto de Paradigmas de Aprendizagem de Máquina

## Descrição

Este projeto tem como objetivo desenvolver um modelo de aprendizagem não supervisionada para identificar substitutos ideais para jogadores de futebol. O modelo é projetado para sugerir substitutos em situações como lesões ou transferências, com base em dados extraídos do site [FBref](https://fbref.com/en/).

## Estrutura do Projeto

```
└── scrapping/                  # Pasta para realizar o scraping de dados
    ├── brazillian_players_stats.py  # Script para coleta de dados de jogadores brasileiros
    └── testing/               # Testes com o BeautifulSoup
        ├── bastos_test.py    # Testes específicos para scraping
        └── nba_test.py       # Testes adicionais para scraping
```
