# ⚽ Football Historical Data Scraper

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Selenium](https://img.shields.io/badge/Selenium-WebDriver-green)](https://selenium.dev)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-orange)](https://pandas.pydata.org)

## 🏆 Visão Geral

Sistema avançado de web scraping para coleta de dados históricos de futebol do **FBRef.com**. Especializado em **Premier League** e **Brasileirão**, capaz de extrair estatísticas detalhadas de jogadores de múltiplas temporadas com salvamento automático e análise abrangente.

### 🎯 Características Principais

- ⚽ **Duas Ligas Principais**: Premier League e Brasileirão
- �� **Dados Históricos**: 5+ temporadas por liga
- 📊 **11 Categorias de Estatísticas**: Standard, Goleiro, Finalização, Passes, Defesa, etc.
- 💾 **Salvamento Automático**: Por temporada para segurança
- 📈 **Análise Avançada**: Rankings, categorização e métricas especializadas
- 🔄 **Interface Interativa**: Seleção personalizada de ligas e temporadas

## 📊 Dados Coletados

### 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League
- **Temporadas**: 2020-2021 até 2024-2025
- **Times**: 20 por temporada (Arsenal, Liverpool, Manchester City, etc.)
- **Jogadores**: ~500-800 por temporada

### 🇧🇷 Brasileirão
- **Temporadas**: 2020 até 2025
- **Times**: 20 por temporada (Palmeiras, Flamengo, São Paulo, etc.)
- **Jogadores**: ~500-900 por temporada

## 📈 Categorias de Estatísticas

| Categoria | Métricas Principais | Jogadores Alvo |
|-----------|-------------------|----------------|
| **Standard** | Gols, Assistências, xG, xA | Todos |
| **Goleiro** | Defesas, Clean Sheets, PSxG | Goleiros |
| **Finalização** | Chutes, Precisão, Distância | Atacantes |
| **Passes** | Precisão, Distância, Progressivos | Meio-campistas |
| **Defesa** | Tackles, Interceptações, Bloqueios | Defensores |
| **Posse** | Dribles, Carries, Toques | Todos |
| **Tempo** | Minutos, Titularidades, +/- | Todos |
| **Criação** | SCA, GCA, Passes-chave | Criativos |
| **Tipos Passe** | Cruzamentos, Through balls | Especialistas |
| **Avançado GK** | PSxG, Ações fora da área | Goleiros |
| **Diversos** | Cartões, Faltas, Duelos aéreos | Todos |

## 🏗️ Arquitetura do Sistema
football-scraper/ ├── 📁 Data/ # Arquivos Excel gerados │ ├── premier_league_2024-2025_.xlsx │ ├── brasileirao_2024_.xlsx │ └── ... ├── main.py # Scraper principal ├── requirements.txt # Dependências ├── README.md # Documentação ├── .gitignore # Arquivos ignorados └── LICENSE # Licença MIT


## 🚀 Instalação e Uso

### Pré-requisitos
- Python 3.8+
- Google Chrome instalado
- Conexão estável com internet
- ~2GB espaço livre (dados completos)

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/football-scraper.git
cd football-scraper
```

2. Crie ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. Instale dependências
```bash
pip install -r requirements.txt
```

4. Execute o scraper
```bash
python scrapping_fbref.py
```

python main.py
🎮 Interface Interativa
1. Seleção de Liga
🏆 SELEÇÃO DE LIGA
==========================================
1. Premier League (Inglaterra)
2. Brasileirão (Brasil)

Escolha a liga (1 ou 2): 1
✅ Liga selecionada: Brasileirão
2. Seleção de Temporadas
📅 SELEÇÃO DE TEMPORADAS - Brasileirão
==================================================
Temporadas disponíveis:
1. 2025
2. 2024
3. 2023
4. 2022
5. 2021
6. 2020
7. Todas as temporadas

Escolha as temporadas (ex: 1,2,3 ou 7 para todas): 1
✅ Temporadas selecionadas: 2025
3. Coleta Automática
🚀 INICIANDO COLETA COM SALVAMENTO AUTOMÁTICO
📊 Liga: Brasileirão
📅 Temporada: 2025
💾 Salvamento: Automático após cada temporada
============================================================

📅 TEMPORADA 2024-2025 (1/2)
==================================================

🏈 Coletando Palmeiras - 2025
   📊 Coletando standard...
   ✅ 26 jogadores encontrados
   📊 Coletando keeper...
   ✅ keeper dados mesclados
   ...
✅ Arsenal 2025: 26 jogadores processados
📊 Exemplo de Saída
Estrutura do Excel Gerado
premier_league_2024-2025_20241111_1945.xlsx
├── 📋 Temporada_2025             # Dados completos
├── ⚽ Ofensivos                  # Gols, assistências, xG
├── 🛡️ Defensivos                 # Tackles, interceptações
├── 🥅 Goleiros                   # Defesas, clean sheets
├── 🎯 Passes                     # Precisão, progressivos
├── 💨 Posse                      # Dribles, carries
├── 🏆 Top_Gols                   # Ranking artilheiros
├── 🎭 Top_Assistencias           # Ranking assistências
├── 📊 Top_xG                     # Ranking xG
└── ⏱️ Top_Minutos                # Ranking tempo jogado
Dados por Jogador (Exemplo)
Nome	      Clube	  Posição	Idade	Minutos	Gols	Assistências	xG	xA
Vitor Roque	Palmeiras	FW	      20	  1812	 15	         3	       12  2.6
�� Funcionalidades Técnicas
🎯 Scraping Inteligente
Multi-tabela: 11 tipos diferentes de estatísticas
Navegação Robusta: URLs dinâmicas por time/temporada
Tratamento de Erros: Continuidade mesmo com falhas
Rate Limiting: Pausas inteligentes entre requisições
📊 Processamento de Dados
Limpeza Automática: Conversão segura de tipos
Mesclagem Inteligente: Combinação de múltiplas tabelas
Validação: Verificação de consistência dos dados
Normalização: Padronização de formatos
💾 Sistema de Salvamento
Salvamento Progressivo: Por temporada para segurança
Múltiplas Abas: Categorização automática
Rankings Automáticos: Top performers por métrica
Recuperação: Dados seguros mesmo com interrupção
📈 Performance e Escalabilidade
Métrica	Premier League	Brasileirão
Times por Temporada	20	20
Jogadores por Time	~25-30	~25-30
Estatísticas por Jogador	100+	100+
Tempo por Temporada	~25-30 min	~25-30 min
Tamanho Arquivo	~2-5 MB	~2-5 MB
��️ Tecnologias Utilizadas

selenium.dev
: Automação de navegador

pandas.pydata.org
: Manipulação e análise de dados

openpyxl.readthedocs.io
: Geração Excel avançada

github.com
: Gerenciamento automático de drivers
�� Casos de Uso
📊 Análise Esportiva
Scouting: Identificação de talentos jovens
Performance Analysis: Análise detalhada de jogadores
Comparação: Benchmarking entre ligas
Tendências: Evolução de métricas ao longo do tempo
🤖 Data Science
Machine Learning: Features para modelos preditivos
Clustering: Agrupamento de perfis de jogadores
Visualização: Dashboards e gráficos avançados
Estatística: Análises correlacionais
💼 Aplicações Comerciais
Fantasy Sports: Dados para fantasy leagues
Apostas Esportivas: Análise de probabilidades
Mídia Esportiva: Conteúdo baseado em dados
Clubes: Análise de mercado e scouting
⚙️ Configuração Avançada
Personalizar Diretório de Salvamento
python
Copiar

# No início do __init__()
```bash
scraper = FootballHistoricalScraper()
scraper.save_directory = r"C:\Seu\Diretorio\Personalizado"
```

Adicionar Nova Liga
# Adicionar no dicionário self.leagues
```bash
"nova_liga": {
    "name": "Nova Liga",
    "comp_id": "XX",
    "seasons": ["2024", "2023"],
    # ... configurações específicas
}
```

Modificar Estatísticas Coletadas
# Personalizar em get_player_table_mappings()
```bash
def get_player_table_mappings(self):
    return {
        'standard': f'stats_standard_{comp_id}',
        'custom_stat': f'stats_custom_{comp_id}',  # Nova estatística
        # ... outras estatísticas
    }
```



👨‍💻 Autor
Miguel Serea MiguelSerea

💼 LinkedIn: miguel serea
https://www.linkedin.com/in/miguel-serea-917168182/

linkedin.com
🐙 GitHub: MiguelSerea
https://github.com/MiguelSerea

�� Email: miguelserea01@gmail.com

⭐ Mostre seu apoio
Se este projeto foi útil para você, considere dar uma ⭐!
