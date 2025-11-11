from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re
import json
from datetime import datetime
import os

class FootballHistoricalScraper:
    """Scraper completo de futebol - Premier League e Brasileirão"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        
        # Diretório de salvamento
        self.save_directory = r"C:\Users\migue\trabalho\análise de dados\selenium\FBrefScrappe\Data"
        
        # Criar diretório se não existir
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
            print(f"📁 Diretório criado: {self.save_directory}")
            
        # Configurações das ligas
        self.leagues = {
            "premier_league": {
                "name": "Premier League",
                "comp_id": "9",
                "seasons": ["2024-2025", "2023-2024", "2022-2023", "2021-2022", "2020-2021"],
                "season_urls": {
                    "2024-2025": "https://fbref.com/en/comps/9/2024-2025/",
                    "2023-2024": "https://fbref.com/en/comps/9/2023-2024/",
                    "2022-2023": "https://fbref.com/en/comps/9/2022-2023/",
                    "2021-2022": "https://fbref.com/en/comps/9/2021-2022/",
                    "2020-2021": "https://fbref.com/en/comps/9/2020-2021/"
                },
                "teams_by_season": {
                    "2024-2025": {
                        "Arsenal": "18bb7c10",
                        "Liverpool": "822bd0ba", 
                        "Manchester City": "b8fd03ef",
                        "Chelsea": "cff3d9bb",
                        "Manchester United": "19538871",
                        "Tottenham": "361ca564",
                        "Newcastle": "b2b47a98",
                        "Brighton": "d07537b9",
                        "Aston Villa": "8602292d",
                        "West Ham": "7c21e445",
                        "Crystal Palace": "47c64c55",
                        "Bournemouth": "4ba7cbea",
                        "Fulham": "fd962109",
                        "Wolverhampton": "8cec06e1",
                        "Everton": "d3fd31cc",
                        "Brentford": "cd051869",
                        "Nottingham Forest": "e4a775cb",
                        "Leicester City": "a2d435b3",
                        "Ipswich Town": "b74092de",
                        "Southampton": "33c895d4"
                    },
                    "2023-2024": {
                        "Arsenal": "18bb7c10",
                        "Liverpool": "822bd0ba",
                        "Manchester City": "b8fd03ef", 
                        "Chelsea": "cff3d9bb",
                        "Manchester United": "19538871",
                        "Tottenham": "361ca564",
                        "Newcastle": "b2b47a98",
                        "Brighton": "d07537b9",
                        "Aston Villa": "8602292d",
                        "West Ham": "7c21e445",
                        "Crystal Palace": "47c64c55",
                        "Bournemouth": "4ba7cbea",
                        "Fulham": "fd962109",
                        "Wolverhampton": "8cec06e1",
                        "Everton": "d3fd31cc",
                        "Brentford": "cd051869",
                        "Nottingham Forest": "e4a775cb",
                        "Sheffield United": "1df6b87e",
                        "Burnley": "943e8050",
                        "Luton Town": "e297cd13"
                    },
                    "2022-2023": {
                        "Arsenal": "18bb7c10",
                        "Liverpool": "822bd0ba",
                        "Manchester City": "b8fd03ef",
                        "Chelsea": "cff3d9bb", 
                        "Manchester United": "19538871",
                        "Tottenham": "361ca564",
                        "Newcastle": "b2b47a98",
                        "Brighton": "d07537b9",
                        "Aston Villa": "8602292d",
                        "West Ham": "7c21e445",
                        "Crystal Palace": "47c64c55",
                        "Bournemouth": "4ba7cbea",
                        "Fulham": "fd962109",
                        "Wolverhampton": "8cec06e1",
                        "Everton": "d3fd31cc",
                        "Brentford": "cd051869",
                        "Nottingham Forest": "e4a775cb",
                        "Leeds United": "5bfb9659",
                        "Leicester City": "a2d435b3",
                        "Southampton": "33c895d4"
                    },
                    "2021-2022": {
                        "Arsenal": "18bb7c10",
                        "Liverpool": "822bd0ba",
                        "Manchester City": "b8fd03ef",
                        "Chelsea": "cff3d9bb",
                        "Manchester United": "19538871",
                        "Tottenham": "361ca564",
                        "Newcastle": "b2b47a98",
                        "Brighton": "d07537b9",
                        "Aston Villa": "8602292d",
                        "West Ham": "7c21e445",
                        "Crystal Palace": "47c64c55",
                        "Wolverhampton": "8cec06e1",
                        "Everton": "d3fd31cc",
                        "Brentford": "cd051869",
                        "Leeds United": "5bfb9659",
                        "Leicester City": "a2d435b3",
                        "Southampton": "33c895d4",
                        "Watford": "2abfe087",
                        "Burnley": "943e8050",
                        "Norwich City": "1c781004"
                    },
                    "2020-2021": {
                        "Arsenal": "18bb7c10",
                        "Liverpool": "822bd0ba",
                        "Manchester City": "b8fd03ef",
                        "Chelsea": "cff3d9bb",
                        "Manchester United": "19538871",
                        "Tottenham": "361ca564",
                        "Brighton": "d07537b9",
                        "Aston Villa": "8602292d",
                        "West Ham": "7c21e445",
                        "Crystal Palace": "47c64c55",
                        "Wolverhampton": "8cec06e1",
                        "Everton": "d3fd31cc",
                        "Leeds United": "5bfb9659",
                        "Leicester City": "a2d435b3",
                        "Southampton": "33c895d4",
                        "Burnley": "943e8050",
                        "Sheffield United": "1df6b87e",
                        "Fulham": "fd962109",
                        "West Bromwich Albion": "60c6b05f"
                    }
                }
            },
            "brasileirao": {
                "name": "Brasileirão",
                "comp_id": "24",
                "seasons": ["2025", "2024", "2023", "2022", "2021", "2020"],
                "season_urls": {
                    "2025": "https://fbref.com/en/comps/24/2025/",
                    "2024": "https://fbref.com/en/comps/24/2024/",
                    "2023": "https://fbref.com/en/comps/24/2023/", 
                    "2022": "https://fbref.com/en/comps/24/2022/",
                    "2021": "https://fbref.com/en/comps/24/2021/",
                    "2020": "https://fbref.com/en/comps/24/2020/"
                },
                "teams_by_season": {
                    "2025": {  
                        "Palmeiras": "abdce579",
                        "Botafogo": "d9fdd9d9", 
                        "Fortaleza": "a9d0ab0e",
                        "Flamengo": "639950ae",
                        "São Paulo": "5f232eb1",
                        "Bahia": "157b7fee",
                        "Cruzeiro": "03ff5eeb",
                        "Vasco da Gama": "83f55dbe",
                        "Atlético-MG": "422bb734",
                        "Internacional": "6f7e1f03",
                        "Bragantino": "f98930d1",
                        "Juventude": "d081b697",
                        "Grêmio": "d5ae3703",
                        "Fluminense": "84d9701c",
                        "Corinthians": "bf4acd28",
                        "Vitória": "33f95fe0",
                        "Santos": "712c528f",
                        "Mirassol": "289e8847",
                        "Ceará": "2f335e17",
                        "Sport": "ece66b78",
                        
                    },
                    "2024": {
                        "Palmeiras": "abdce579",
                        "Botafogo": "d9fdd9d9", 
                        "Fortaleza": "a9d0ab0e",
                        "Flamengo": "639950ae",
                        "São Paulo": "5f232eb1",
                        "Bahia": "157b7fee",
                        "Cruzeiro": "03ff5eeb",
                        "Vasco da Gama": "83f55dbe",
                        "Atlético-MG": "422bb734",
                        "Internacional": "6f7e1f03",
                        "Bragantino": "f98930d1",
                        "Juventude": "d081b697",
                        "Criciúma": "3f7595bb",
                        "Athletico-PR": "2091c619",
                        "Grêmio": "d5ae3703",
                        "Fluminense": "84d9701c",
                        "Corinthians": "bf4acd28",
                        "Vitória": "33f95fe0",
                        "Cuiabá": "f0e6fb14",
                        "Atlético-GO": "32d508ca"
                    },
                    "2023": {
                        "Palmeiras": "abdce579",
                        "Grêmio": "d5ae3703", 
                        "Flamengo": "639950ae",
                        "Atlético-MG": "422bb734",
                        "Botafogo": "d9fdd9d9",
                        "Bragantino": "f98930d1",
                        "Fluminense": "84d9701c",
                        "Internacional": "6f7e1f03",
                        "Fortaleza": "a9d0ab0e",
                        "São Paulo": "5f232eb1",
                        "Cuiabá": "f0e6fb14",
                        "Corinthians": "bf4acd28",
                        "Athletico-PR": "2091c619",
                        "Bahia": "157b7fee",
                        "Santos": "712c528f",
                        "Goiás": "78c617cc",
                        "Vasco da Gama": "83f55dbe",
                        "Coritiba": "d680d257",
                        "América-MG": "1f68d780",
                        "Cruzeiro": "03ff5eeb"
                    },
                    "2022": {
                        "Palmeiras": "abdce579",
                        "Internacional": "6f7e1f03",
                        "Fluminense": "84d9701c",
                        "Corinthians": "bf4acd28",
                        "Flamengo": "639950ae",
                        "Athletico-PR": "2091c619",
                        "Atlético-MG": "422bb734",
                        "Fortaleza": "a9d0ab0e",
                        "São Paulo": "5f232eb1",
                        "América-MG": "1f68d780",
                        "Botafogo": "d9fdd9d9",
                        "Santos": "712c528f",
                        "Goiás": "78c617cc",
                        "Bragantino": "f98930d1",
                        "Coritiba": "d680d257",
                        "Cuiabá": "f0e6fb14",
                        "Ceará": "2f335e17",
                        "Atlético-GO": "32d508ca",
                        "Avaí": "f205258a",
                        "Juventude": "d081b697"
                    },
                    "2021": {
                        "Atlético-MG": "422bb734",
                        "Flamengo": "639950ae",
                        "Palmeiras": "abdce579",
                        "Fortaleza": "a9d0ab0e",
                        "Corinthians": "bf4acd28",
                        "Bragantino": "f98930d1",
                        "Fluminense": "84d9701c",
                        "América-MG": "1f68d780",
                        "Atlético-GO": "32d508ca",
                        "Santos": "712c528f",
                        "Ceará": "2f335e17",
                        "Internacional": "6f7e1f03",
                        "São Paulo": "5f232eb1",
                        "Athletico-PR": "2091c619",
                        "Cuiabá": "f0e6fb14",
                        "Juventude": "d081b697",
                        "Grêmio": "d5ae3703",
                        "Bahia": "157b7fee",
                        "Sport": "ece66b78",
                        "Chapecoense": "baa296ad"
                    },
                    "2020": {
                        "Flamengo": "639950ae",
                        "Internacional": "6f7e1f03",
                        "Atlético-MG": "422bb734",
                        "São Paulo": "5f232eb1",
                        "Fluminense": "84d9701c",
                        "Grêmio": "d5ae3703",
                        "Palmeiras": "abdce579",
                        "Santos": "712c528f",
                        "Athletico-PR": "2091c619",
                        "Ceará": "2f335e17",
                        "Bahia": "157b7fee",
                        "Bragantino": "f98930d1",
                        "Fortaleza": "a9d0ab0e",
                        "Sport": "ece66b78",
                        "Vasco da Gama": "83f55dbe",
                        "Goiás": "78c617cc",
                        "Corinthians": "bf4acd28",
                        "Atlético-GO": "32d508ca",
                        "Coritiba": "d680d257",
                        "Botafogo": "d9fdd9d9"
                    }
                }
            }
        }
        
      
        self.current_league = None
        self.selected_seasons = []
        
    def setup_driver(self):
        """Setup otimizado do WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)
        return self.driver
    
    def safe_int(self, value):
        """Conversão segura para inteiro"""
        try:
            if not value or value == '' or value == '-':
                return 0
            clean_value = re.sub(r'[,\s]', '', str(value))
            return int(float(clean_value))
        except:
            return 0
    
    def safe_float(self, value):
        """Conversão segura para float"""
        try:
            if not value or value == '' or value == '-':
                return 0.0
            clean_value = re.sub(r'[,\s]', '', str(value))
            return float(clean_value)
        except:
            return 0.0
    
    def get_player_table_mappings(self):
        """Retorna mapeamento das tabelas de jogadores baseado na liga"""
        comp_id = self.current_league["comp_id"]
        return {
            'standard': f'stats_standard_{comp_id}',
            'keeper': f'stats_keeper_{comp_id}',
            'keeper_adv': f'stats_keeper_adv_{comp_id}',
            'shooting': f'stats_shooting_{comp_id}',
            'passing': f'stats_passing_{comp_id}',
            'passing_types': f'stats_passing_types_{comp_id}',
            'gca': f'stats_gca_{comp_id}',
            'defense': f'stats_defense_{comp_id}',
            'possession': f'stats_possession_{comp_id}',
            'playing_time': f'stats_playing_time_{comp_id}',
            'misc': f'stats_misc_{comp_id}'
        }
    
    def extract_standard_stats(self, row):
        """Extrai estatísticas padrão"""
        dados = {}
        
        try:
            try:
                name_cell = row.find_element(By.TAG_NAME, "th")
                dados['nome'] = name_cell.text.strip()
            except:
                return dados
            
            cells = row.find_elements(By.TAG_NAME, "td")
            
            if len(cells) >= 20:
                dados['nacionalidade'] = cells[0].text.strip() if len(cells) > 0 else ''
                dados['posicao'] = cells[1].text.strip() if len(cells) > 1 else ''
                dados['idade'] = cells[2].text.strip() if len(cells) > 2 else ''
                dados['jogos'] = self.safe_int(cells[3].text.strip()) if len(cells) > 3 else 0
                dados['jogos_titularidade'] = self.safe_int(cells[4].text.strip()) if len(cells) > 4 else 0
                dados['minutos'] = self.safe_int(cells[5].text.strip()) if len(cells) > 5 else 0
                dados['minutos_90s'] = self.safe_float(cells[6].text.strip()) if len(cells) > 6 else 0.0
                dados['gols'] = self.safe_int(cells[7].text.strip()) if len(cells) > 7 else 0
                dados['assistencias'] = self.safe_int(cells[8].text.strip()) if len(cells) > 8 else 0
                dados['gols_assistencias'] = self.safe_int(cells[9].text.strip()) if len(cells) > 9 else 0
                dados['gols_sem_penalti'] = self.safe_int(cells[10].text.strip()) if len(cells) > 10 else 0
                dados['penaltis_marcados'] = self.safe_int(cells[11].text.strip()) if len(cells) > 11 else 0
                dados['penaltis_tentados'] = self.safe_int(cells[12].text.strip()) if len(cells) > 12 else 0
                dados['cartoes_amarelos'] = self.safe_int(cells[13].text.strip()) if len(cells) > 13 else 0
                dados['cartoes_vermelhos'] = self.safe_int(cells[14].text.strip()) if len(cells) > 14 else 0
                dados['xg'] = self.safe_float(cells[15].text.strip()) if len(cells) > 15 else 0.0
                dados['npxg'] = self.safe_float(cells[16].text.strip()) if len(cells) > 16 else 0.0
                dados['xa'] = self.safe_float(cells[17].text.strip()) if len(cells) > 17 else 0.0
                dados['npxg_xa'] = self.safe_float(cells[18].text.strip()) if len(cells) > 18 else 0.0
                dados['carries_progressivos'] = self.safe_int(cells[19].text.strip()) if len(cells) > 19 else 0
                dados['passes_progressivos'] = self.safe_int(cells[20].text.strip()) if len(cells) > 20 else 0
                dados['recepcoes_progressivas'] = self.safe_int(cells[21].text.strip()) if len(cells) > 21 else 0
                
        except Exception as e:
            print(f"     ⚠️ Erro na extração standard: {e}")
        
        return dados
    
    def extract_keeper_stats(self, row):
        """Extrai estatísticas de goleiro"""
        dados = {}
        
        try:
            name_cell = row.find_element(By.TAG_NAME, "th")
            dados['nome'] = name_cell.text.strip()
            
            cells = row.find_elements(By.TAG_NAME, "td")
            
            if len(cells) >= 15:
                dados['gols_sofridos'] = self.safe_int(cells[4].text.strip()) if len(cells) > 4 else 0
                dados['gols_sofridos_por_90'] = self.safe_float(cells[5].text.strip()) if len(cells) > 5 else 0.0
                dados['chutes_enfrentados'] = self.safe_int(cells[6].text.strip()) if len(cells) > 6 else 0
                dados['defesas'] = self.safe_int(cells[7].text.strip()) if len(cells) > 7 else 0
                dados['defesas_percentual'] = self.safe_float(cells[8].text.strip()) if len(cells) > 8 else 0.0
                dados['clean_sheets'] = self.safe_int(cells[9].text.strip()) if len(cells) > 9 else 0
                dados['clean_sheets_percentual'] = self.safe_float(cells[10].text.strip()) if len(cells) > 10 else 0.0
                dados['penaltis_enfrentados'] = self.safe_int(cells[11].text.strip()) if len(cells) > 11 else 0
                dados['penaltis_permitidos'] = self.safe_int(cells[12].text.strip()) if len(cells) > 12 else 0
                dados['penaltis_salvos'] = self.safe_int(cells[13].text.strip()) if len(cells) > 13 else 0
                dados['penaltis_perdidos'] = self.safe_int(cells[14].text.strip()) if len(cells) > 14 else 0
                
        except Exception as e:
            print(f"     ⚠️ Erro na extração keeper: {e}")
        
        return dados
    
    def extract_keeper_adv_stats(self, row):
        """Extrai estatísticas avançadas de goleiro"""
        dados = {}
        
        try:
            name_cell = row.find_element(By.TAG_NAME, "th")
            dados['nome'] = name_cell.text.strip()
            
            cells = row.find_elements(By.TAG_NAME, "td")
            
            if len(cells) >= 15:
                dados['psxg'] = self.safe_float(cells[4].text.strip()) if len(cells) > 4 else 0.0
                dados['psxg_sot'] = self.safe_float(cells[5].text.strip()) if len(cells) > 5 else 0.0
                dados['psxg_minus_ga'] = self.safe_float(cells[6].text.strip()) if len(cells) > 6 else 0.0
                dados['psxg_minus_ga_por_90'] = self.safe_float(cells[7].text.strip()) if len(cells) > 7 else 0.0
                dados['passes_lancados_completos'] = self.safe_int(cells[8].text.strip()) if len(cells) > 8 else 0
                dados['passes_lancados_tentados'] = self.safe_int(cells[9].text.strip()) if len(cells) > 9 else 0
                dados['passes_lancados_percentual'] = self.safe_float(cells[10].text.strip()) if len(cells) > 10 else 0.0
                dados['acoes_fora_area'] = self.safe_int(cells[11].text.strip()) if len(cells) > 11 else 0
                dados['acoes_fora_area_por_90'] = self.safe_float(cells[12].text.strip()) if len(cells) > 12 else 0.0
                dados['distancia_media_acoes'] = self.safe_float(cells[13].text.strip()) if len(cells) > 13 else 0.0
                
        except Exception as e:
            print(f"     ⚠️ Erro na extração keeper_adv: {e}")
        
        return dados
    
    def extract_shooting_stats(self, row):
        """Extrai estatísticas de finalização"""
        dados = {}
        
        try:
            name_cell = row.find_element(By.TAG_NAME, "th")
            dados['nome'] = name_cell.text.strip()
            
            cells = row.find_elements(By.TAG_NAME, "td")
            
            if len(cells) >= 15:
                dados['chutes_total'] = self.safe_int(cells[4].text.strip()) if len(cells) > 4 else 0
                dados['chutes_no_gol'] = self.safe_int(cells[5].text.strip()) if len(cells) > 5 else 0
                dados['chutes_precisao'] = self.safe_float(cells[6].text.strip()) if len(cells) > 6 else 0.0
                dados['chutes_por_90'] = self.safe_float(cells[7].text.strip()) if len(cells) > 7 else 0.0
                dados['chutes_gol_por_90'] = self.safe_float(cells[8].text.strip()) if len(cells) > 8 else 0.0
                dados['gols_por_chute'] = self.safe_float(cells[9].text.strip()) if len(cells) > 9 else 0.0
                dados['gols_por_chute_gol'] = self.safe_float(cells[10].text.strip()) if len(cells) > 10 else 0.0
                dados['distancia_media_chute'] = self.safe_float(cells[11].text.strip()) if len(cells) > 11 else 0.0
                dados['chutes_tiro_livre'] = self.safe_int(cells[12].text.strip()) if len(cells) > 12 else 0
                dados['penaltis_marcados_shooting'] = self.safe_int(cells[13].text.strip()) if len(cells) > 13 else 0
                dados['penaltis_tentados_shooting'] = self.safe_int(cells[14].text.strip()) if len(cells) > 14 else 0
                
        except Exception as e:
            print(f"     ⚠️ Erro na extração shooting: {e}")
        
        return dados
    
    def extract_passing_stats(self, row):
        """Extrai estatísticas de passe"""
        dados = {}
        
        try:
            name_cell = row.find_element(By.TAG_NAME, "th")
            dados['nome'] = name_cell.text.strip()
            
            cells = row.find_elements(By.TAG_NAME, "td")
            
            if len(cells) >= 20:
                dados['passes_completos'] = self.safe_int(cells[4].text.strip()) if len(cells) > 4 else 0
                dados['passes_tentados'] = self.safe_int(cells[5].text.strip()) if len(cells) > 5 else 0
                dados['passes_precisao'] = self.safe_float(cells[6].text.strip()) if len(cells) > 6 else 0.0
                dados['distancia_total_passes'] = self.safe_int(cells[7].text.strip()) if len(cells) > 7 else 0
                dados['distancia_progressiva_passes'] = self.safe_int(cells[8].text.strip()) if len(cells) > 8 else 0
                dados['passes_curtos_completos'] = self.safe_int(cells[9].text.strip()) if len(cells) > 9 else 0
                dados['passes_curtos_tentados'] = self.safe_int(cells[10].text.strip()) if len(cells) > 10 else 0
                dados['passes_curtos_precisao'] = self.safe_float(cells[11].text.strip()) if len(cells) > 11 else 0.0
                dados['passes_medios_completos'] = self.safe_int(cells[12].text.strip()) if len(cells) > 12 else 0
                dados['passes_medios_tentados'] = self.safe_int(cells[13].text.strip()) if len(cells) > 13 else 0
                dados['passes_medios_precisao'] = self.safe_float(cells[14].text.strip()) if len(cells) > 14 else 0.0
                dados['passes_longos_completos'] = self.safe_int(cells[15].text.strip()) if len(cells) > 15 else 0
                dados['passes_longos_tentados'] = self.safe_int(cells[16].text.strip()) if len(cells) > 16 else 0
                dados['passes_longos_precisao'] = self.safe_float(cells[17].text.strip()) if len(cells) > 17 else 0.0
                
        except Exception as e:
            print(f"     ⚠️ Erro na extração passing: {e}")
        
        return dados
    
    def extract_passing_types_stats(self, row):
        """Extrai estatísticas de tipos de passe"""
        dados = {}
        
        try:
            name_cell = row.find_element(By.TAG_NAME, "th")
            dados['nome'] = name_cell.text.strip()
            
            cells = row.find_elements(By.TAG_NAME, "td")
            
            if len(cells) >= 15:
                dados['passes_live'] = self.safe_int(cells[4].text.strip()) if len(cells) > 4 else 0
                dados['passes_dead'] = self.safe_int(cells[5].text.strip()) if len(cells) > 5 else 0
                dados['passes_tiro_livre'] = self.safe_int(cells[6].text.strip()) if len(cells) > 6 else 0
                dados['passes_through'] = self.safe_int(cells[7].text.strip()) if len(cells) > 7 else 0
                dados['passes_switches'] = self.safe_int(cells[8].text.strip()) if len(cells) > 8 else 0
                dados['cruzamentos_passing'] = self.safe_int(cells[9].text.strip()) if len(cells) > 9 else 0
                dados['throw_ins'] = self.safe_int(cells[10].text.strip()) if len(cells) > 10 else 0
                dados['escanteios'] = self.safe_int(cells[11].text.strip()) if len(cells) > 11 else 0
                dados['escanteios_in'] = self.safe_int(cells[12].text.strip()) if len(cells) > 12 else 0
                dados['escanteios_out'] = self.safe_int(cells[13].text.strip()) if len(cells) > 13 else 0
                dados['escanteios_straight'] = self.safe_int(cells[14].text.strip()) if len(cells) > 14 else 0
                dados['passes_completos_passing_types'] = self.safe_int(cells[15].text.strip()) if len(cells) > 15 else 0
                dados['passes_impedimento'] = self.safe_int(cells[16].text.strip()) if len(cells) > 16 else 0
                dados['passes_bloqueados'] = self.safe_int(cells[17].text.strip()) if len(cells) > 17 else 0
                
        except Exception as e:
            print(f"     ⚠️ Erro na extração passing_types: {e}")
        
        return dados
    
    def extract_gca_stats(self, row):
        """Extrai estatísticas de criação de gols e chutes"""
        dados = {}
        
        try:
            name_cell = row.find_element(By.TAG_NAME, "th")
            dados['nome'] = name_cell.text.strip()
            
            cells = row.find_elements(By.TAG_NAME, "td")
            
            if len(cells) >= 15:
                dados['sca'] = self.safe_int(cells[4].text.strip()) if len(cells) > 4 else 0
                dados['sca_por_90'] = self.safe_float(cells[5].text.strip()) if len(cells) > 5 else 0.0
                dados['sca_passes_live'] = self.safe_int(cells[6].text.strip()) if len(cells) > 6 else 0
                dados['sca_passes_dead'] = self.safe_int(cells[7].text.strip()) if len(cells) > 7 else 0
                dados['sca_take_ons'] = self.safe_int(cells[8].text.strip()) if len(cells) > 8 else 0
                dados['sca_chutes'] = self.safe_int(cells[9].text.strip()) if len(cells) > 9 else 0
                dados['sca_faltas'] = self.safe_int(cells[10].text.strip()) if len(cells) > 10 else 0
                dados['sca_acoes_defensivas'] = self.safe_int(cells[11].text.strip()) if len(cells) > 11 else 0
                dados['gca'] = self.safe_int(cells[12].text.strip()) if len(cells) > 12 else 0
                dados['gca_por_90'] = self.safe_float(cells[13].text.strip()) if len(cells) > 13 else 0.0
                dados['gca_passes_live'] = self.safe_int(cells[14].text.strip()) if len(cells) > 14 else 0
                dados['gca_passes_dead'] = self.safe_int(cells[15].text.strip()) if len(cells) > 15 else 0
                dados['gca_take_ons'] = self.safe_int(cells[16].text.strip()) if len(cells) > 16 else 0
                dados['gca_chutes'] = self.safe_int(cells[17].text.strip()) if len(cells) > 17 else 0
                dados['gca_faltas'] = self.safe_int(cells[18].text.strip()) if len(cells) > 18 else 0
                dados['gca_acoes_defensivas'] = self.safe_int(cells[19].text.strip()) if len(cells) > 19 else 0
                
        except Exception as e:
            print(f"     ⚠️ Erro na extração gca: {e}")
        
        return dados
    
    def extract_defense_stats(self, row):
        """Extrai estatísticas defensivas"""
        dados = {}
        
        try:
            name_cell = row.find_element(By.TAG_NAME, "th")
            dados['nome'] = name_cell.text.strip()
            
            cells = row.find_elements(By.TAG_NAME, "td")
            
            if len(cells) >= 15:
                dados['tackles_total'] = self.safe_int(cells[4].text.strip()) if len(cells) > 4 else 0
                dados['tackles_ganhos'] = self.safe_int(cells[5].text.strip()) if len(cells) > 5 else 0
                dados['tackles_def_terco'] = self.safe_int(cells[6].text.strip()) if len(cells) > 6 else 0
                dados['tackles_meio_terco'] = self.safe_int(cells[7].text.strip()) if len(cells) > 7 else 0
                dados['tackles_att_terco'] = self.safe_int(cells[8].text.strip()) if len(cells) > 8 else 0
                dados['dribles_contra_tentados'] = self.safe_int(cells[9].text.strip()) if len(cells) > 9 else 0
                dados['dribles_contra_sucesso'] = self.safe_int(cells[10].text.strip()) if len(cells) > 10 else 0
                dados['dribles_contra_precisao'] = self.safe_float(cells[11].text.strip()) if len(cells) > 11 else 0.0
                dados['dribles_contra_perdidos'] = self.safe_int(cells[12].text.strip()) if len(cells) > 12 else 0
                dados['bloqueios_total'] = self.safe_int(cells[13].text.strip()) if len(cells) > 13 else 0
                dados['chutes_bloqueados'] = self.safe_int(cells[14].text.strip()) if len(cells) > 14 else 0
                dados['passes_bloqueados'] = self.safe_int(cells[15].text.strip()) if len(cells) > 15 else 0
                dados['interceptacoes'] = self.safe_int(cells[16].text.strip()) if len(cells) > 16 else 0
                dados['tackles_interceptacoes'] = self.safe_int(cells[17].text.strip()) if len(cells) > 17 else 0
                dados['cortes'] = self.safe_int(cells[18].text.strip()) if len(cells) > 18 else 0
                
        except Exception as e:
            print(f"     ⚠️ Erro na extração defense: {e}")
        
        return dados
    
    def extract_possession_stats(self, row):
        """Extrai estatísticas de posse"""
        dados = {}
        
        try:
            name_cell = row.find_element(By.TAG_NAME, "th")
            dados['nome'] = name_cell.text.strip()
            
            cells = row.find_elements(By.TAG_NAME, "td")
            
            if len(cells) >= 20:
                dados['toques_total'] = self.safe_int(cells[4].text.strip()) if len(cells) > 4 else 0
                dados['toques_def_pen'] = self.safe_int(cells[5].text.strip()) if len(cells) > 5 else 0
                dados['toques_def_terco'] = self.safe_int(cells[6].text.strip()) if len(cells) > 6 else 0
                dados['toques_meio_terco'] = self.safe_int(cells[7].text.strip()) if len(cells) > 7 else 0
                dados['toques_att_terco'] = self.safe_int(cells[8].text.strip()) if len(cells) > 8 else 0
                dados['toques_att_pen'] = self.safe_int(cells[9].text.strip()) if len(cells) > 9 else 0
                dados['toques_live'] = self.safe_int(cells[10].text.strip()) if len(cells) > 10 else 0
                dados['dribles_tentados'] = self.safe_int(cells[11].text.strip()) if len(cells) > 11 else 0
                dados['dribles_sucesso'] = self.safe_int(cells[12].text.strip()) if len(cells) > 12 else 0
                dados['dribles_precisao'] = self.safe_float(cells[13].text.strip()) if len(cells) > 13 else 0.0
                dados['dribles_perdidos'] = self.safe_int(cells[14].text.strip()) if len(cells) > 14 else 0
                dados['carries_total'] = self.safe_int(cells[16].text.strip()) if len(cells) > 16 else 0
                dados['carries_distancia'] = self.safe_int(cells[17].text.strip()) if len(cells) > 17 else 0
                dados['carries_distancia_progressiva'] = self.safe_int(cells[18].text.strip()) if len(cells) > 18 else 0
                dados['carries_progressivos_num'] = self.safe_int(cells[19].text.strip()) if len(cells) > 19 else 0
                dados['carries_terco_final'] = self.safe_int(cells[20].text.strip()) if len(cells) > 20 else 0
                dados['carries_area_penal'] = self.safe_int(cells[21].text.strip()) if len(cells) > 21 else 0
                dados['miscontrols'] = self.safe_int(cells[22].text.strip()) if len(cells) > 22 else 0
                dados['dispossessed'] = self.safe_int(cells[23].text.strip()) if len(cells) > 23 else 0
                dados['recepcoes'] = self.safe_int(cells[24].text.strip()) if len(cells) > 24 else 0
                dados['recepcoes_progressivas'] = self.safe_int(cells[25].text.strip()) if len(cells) > 25 else 0
                
        except Exception as e:
            print(f"     ⚠️ Erro na extração possession: {e}")
        
        return dados
    
    def extract_playing_time_stats(self, row):
        """Extrai estatísticas de tempo de jogo"""
        dados = {}
        
        try:
            name_cell = row.find_element(By.TAG_NAME, "th")
            dados['nome'] = name_cell.text.strip()
            
            cells = row.find_elements(By.TAG_NAME, "td")
            
            if len(cells) >= 15:
                dados['minutos_por_jogo'] = self.safe_float(cells[4].text.strip()) if len(cells) > 4 else 0.0
                dados['minutos_percentual'] = self.safe_float(cells[5].text.strip()) if len(cells) > 5 else 0.0
                dados['minutos_por_titularidade'] = self.safe_float(cells[6].text.strip()) if len(cells) > 6 else 0.0
                dados['titularidades_completas'] = self.safe_int(cells[7].text.strip()) if len(cells) > 7 else 0
                dados['substituicoes'] = self.safe_int(cells[8].text.strip()) if len(cells) > 8 else 0
                dados['minutos_por_substituicao'] = self.safe_float(cells[9].text.strip()) if len(cells) > 9 else 0.0
                dados['substituicoes_nao_utilizadas'] = self.safe_int(cells[10].text.strip()) if len(cells) > 10 else 0
                dados['pontos_por_jogo'] = self.safe_float(cells[11].text.strip()) if len(cells) > 11 else 0.0
                dados['gols_no_campo'] = self.safe_int(cells[12].text.strip()) if len(cells) > 12 else 0
                dados['gols_contra_no_campo'] = self.safe_int(cells[13].text.strip()) if len(cells) > 13 else 0
                dados['plus_minus'] = self.safe_int(cells[14].text.strip()) if len(cells) > 14 else 0
                dados['plus_minus_por_90'] = self.safe_float(cells[15].text.strip()) if len(cells) > 15 else 0.0
                dados['plus_minus_wowy'] = self.safe_float(cells[16].text.strip()) if len(cells) > 16 else 0.0
                dados['xg_no_campo'] = self.safe_float(cells[17].text.strip()) if len(cells) > 17 else 0.0
                dados['xga_no_campo'] = self.safe_float(cells[18].text.strip()) if len(cells) > 18 else 0.0
                dados['xg_plus_minus'] = self.safe_float(cells[19].text.strip()) if len(cells) > 19 else 0.0
                dados['xg_plus_minus_por_90'] = self.safe_float(cells[20].text.strip()) if len(cells) > 20 else 0.0
                dados['xg_plus_minus_wowy'] = self.safe_float(cells[21].text.strip()) if len(cells) > 21 else 0.0
                
        except Exception as e:
            print(f"     ⚠️ Erro na extração playing_time: {e}")
        
        return dados
    
    def extract_misc_stats(self, row):
        """Extrai estatísticas diversas"""
        dados = {}
        
        try:
            name_cell = row.find_element(By.TAG_NAME, "th")
            dados['nome'] = name_cell.text.strip()
            
            cells = row.find_elements(By.TAG_NAME, "td")
            
            if len(cells) >= 15:
                dados['cartoes_amarelos_misc'] = self.safe_int(cells[4].text.strip()) if len(cells) > 4 else 0
                dados['cartoes_vermelhos_misc'] = self.safe_int(cells[5].text.strip()) if len(cells) > 5 else 0
                dados['segundo_amarelo'] = self.safe_int(cells[6].text.strip()) if len(cells) > 6 else 0
                dados['faltas_cometidas'] = self.safe_int(cells[7].text.strip()) if len(cells) > 7 else 0
                dados['faltas_sofridas'] = self.safe_int(cells[8].text.strip()) if len(cells) > 8 else 0
                dados['impedimentos'] = self.safe_int(cells[9].text.strip()) if len(cells) > 9 else 0
                dados['cruzamentos'] = self.safe_int(cells[10].text.strip()) if len(cells) > 10 else 0
                dados['interceptacoes_misc'] = self.safe_int(cells[11].text.strip()) if len(cells) > 11 else 0
                dados['tackles_ganhos_misc'] = self.safe_int(cells[12].text.strip()) if len(cells) > 12 else 0
                dados['penaltis_ganhos'] = self.safe_int(cells[13].text.strip()) if len(cells) > 13 else 0
                dados['penaltis_concedidos'] = self.safe_int(cells[14].text.strip()) if len(cells) > 14 else 0
                dados['gols_contra'] = self.safe_int(cells[15].text.strip()) if len(cells) > 15 else 0
                dados['recuperacoes'] = self.safe_int(cells[16].text.strip()) if len(cells) > 16 else 0
                dados['duelos_aereos_ganhos'] = self.safe_int(cells[17].text.strip()) if len(cells) > 17 else 0
                dados['duelos_aereos_perdidos'] = self.safe_int(cells[18].text.strip()) if len(cells) > 18 else 0
                dados['duelos_aereos_precisao'] = self.safe_float(cells[19].text.strip()) if len(cells) > 19 else 0.0
                
        except Exception as e:
            print(f"     ⚠️ Erro na extração misc: {e}")
        
        return dados
    
    def extract_table_data(self, table, table_type):
        """Extrai dados de uma tabela baseado no tipo"""
        extraction_methods = {
            'standard': self.extract_standard_stats,
            'keeper': self.extract_keeper_stats,
            'keeper_adv': self.extract_keeper_adv_stats,
            'shooting': self.extract_shooting_stats,
            'passing': self.extract_passing_stats,
            'passing_types': self.extract_passing_types_stats,
            'gca': self.extract_gca_stats,
            'defense': self.extract_defense_stats,
            'possession': self.extract_possession_stats,
            'playing_time': self.extract_playing_time_stats,
            'misc': self.extract_misc_stats
        }
        
        players_data = []
        
        try:
            tbody = table.find_element(By.TAG_NAME, "tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")
            
            for row in rows:
                try:
                    row_class = row.get_attribute("class") or ""
                    if "thead" in row_class or "spacer" in row_class:
                        continue
                    
                    extraction_method = extraction_methods.get(table_type)
                    if extraction_method:
                        player_data = extraction_method(row)
                        
                        if (player_data.get('nome') and 
                            player_data['nome'] != '' and 
                            player_data['nome'] != 'Player' and
                            not player_data['nome'].startswith('Squad Total')):
                            
                            players_data.append(player_data)
                            
                except Exception as e:
                    continue
            
        except Exception as e:
            print(f"     ⚠️ Erro ao extrair dados da tabela {table_type}: {e}")
        
        return players_data
    
    def find_table_by_id(self, table_id):
        """Encontra tabela pelo ID"""
        try:
            table = self.driver.find_element(By.ID, table_id)
            if table.is_displayed() and table.size['height'] > 50:
                return table
        except:
            pass
        return None
    
    def scrape_team_season(self, team_name, team_id, season):
        """Scraping de um time em uma temporada específica"""
        print(f"\n🏈 Coletando {team_name} - {season}")
        
        # Construir URL do time
        url = f"https://fbref.com/en/squads/{team_id}/{season}/{team_name.replace(' ', '-')}-Stats"
        
        all_players_data = {}
        
        try:
            self.driver.get(url)
            time.sleep(4)
        
            player_table_mappings = self.get_player_table_mappings()
            
            for table_type, table_id in player_table_mappings.items():
                print(f"   📊 Coletando {table_type}...")
                
                table = self.find_table_by_id(table_id)
                if table:
                    table_data = self.extract_table_data(table, table_type)
                    
                    if table_type == 'standard':
                     
                        for player_data in table_data:
                            player_name = player_data['nome']
                            player_data['clube'] = team_name
                            player_data['temporada'] = season
                            player_data['liga'] = self.current_league["name"]
                            all_players_data[player_name] = player_data
                        print(f"   ✅ {len(table_data)} jogadores encontrados")
                    else:
                      
                        for player_data in table_data:
                            player_name = player_data.get('nome', '')
                            if player_name in all_players_data:
                                all_players_data[player_name].update(player_data)
                        print(f"   ✅ {table_type} dados mesclados")
                else:
                    print(f"   ⚠️ Tabela {table_type} não encontrada")
            
            final_data = list(all_players_data.values())
            print(f"✅ {team_name} {season}: {len(final_data)} jogadores processados")
            return final_data
            
        except Exception as e:
            print(f"❌ Erro ao processar {team_name} {season}: {e}")
            return []
    
    def select_league(self):
        """Interface para seleção da liga"""
        print("\n🏆 SELEÇÃO DE LIGA")
        print("=" * 40)
        print("1. Premier League (Inglaterra)")
        print("2. Brasileirão (Brasil)")
        
        while True:
            try:
                escolha = input("\nEscolha a liga (1 ou 2): ").strip()
                
                if escolha == "1":
                    self.current_league = self.leagues["premier_league"]
                    print(f"✅ Liga selecionada: {self.current_league['name']}")
                    break
                elif escolha == "2":
                    self.current_league = self.leagues["brasileirao"]
                    print(f"✅ Liga selecionada: {self.current_league['name']}")
                    break
                else:
                    print("❌ Opção inválida. Digite 1 ou 2.")
            except KeyboardInterrupt:
                print("\n❌ Operação cancelada.")
                return False
        
        return True
    
    def select_seasons(self):
        """Interface para seleção das temporadas"""
        print(f"\n📅 SELEÇÃO DE TEMPORADAS - {self.current_league['name']}")
        print("=" * 50)
        
        available_seasons = self.current_league["seasons"]
        
        print("Temporadas disponíveis:")
        for i, season in enumerate(available_seasons, 1):
            print(f"{i}. {season}")
        print(f"{len(available_seasons) + 1}. Todas as temporadas")
        
        while True:
            try:
                escolha = input(f"\nEscolha as temporadas (ex: 1,2,3 ou {len(available_seasons) + 1} para todas): ").strip()
                
                if escolha == str(len(available_seasons) + 1):
                    # Todas as temporadas
                    self.selected_seasons = available_seasons.copy()
                    print(f"✅ Selecionadas todas as temporadas: {', '.join(self.selected_seasons)}")
                    break
                else:
                    # Temporadas específicas
                    indices = [int(x.strip()) for x in escolha.split(',')]
                    selected = []
                    
                    for idx in indices:
                        if 1 <= idx <= len(available_seasons):
                            selected.append(available_seasons[idx - 1])
                        else:
                            print(f"❌ Índice {idx} inválido.")
                            break
                    else:
                        self.selected_seasons = selected
                        print(f"✅ Temporadas selecionadas: {', '.join(self.selected_seasons)}")
                        break
                        
            except (ValueError, KeyboardInterrupt):
                print("❌ Entrada inválida. Use números separados por vírgula.")
        
        return True
    
    def salvar_dados_por_temporada(self, season_data, season):
        """Salva dados de uma temporada específica no diretório especificado"""
        if not season_data:
            print(f"❌ Nenhum dado para salvar da temporada {season}")
            return None
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M')
            league_name = self.current_league['name'].replace(' ', '_').lower()
            
            # Nome do arquivo por temporada
            filename = f"{league_name}_{season}_{timestamp}.xlsx"
            # Caminho completo
            excel_filepath = os.path.join(self.save_directory, filename)
            
            df_season = pd.DataFrame(season_data)
            df_season = df_season.sort_values(['clube', 'minutos'], ascending=[True, False])
            
            print(f"💾 Salvando temporada {season} em: {excel_filepath}")
            
            with pd.ExcelWriter(excel_filepath, engine='openpyxl') as writer:
                # Aba principal da temporada
                df_season.to_excel(writer, sheet_name=f'Temporada_{season}', index=False)
                
                # Abas por categoria
                stat_categories = {
                    'Ofensivos': ['nome', 'clube', 'posicao', 'idade', 'minutos', 
                                 'gols', 'assistencias', 'xg', 'xa', 'chutes_total', 'chutes_no_gol'],
                    'Defensivos': ['nome', 'clube', 'posicao', 'idade', 'minutos',
                                  'tackles_total', 'tackles_ganhos', 'interceptacoes', 'bloqueios_total'],
                    'Goleiros': ['nome', 'clube', 'posicao', 'idade', 'minutos',
                                'gols_sofridos', 'defesas', 'clean_sheets', 'psxg'],
                    'Passes': ['nome', 'clube', 'posicao', 'idade', 'minutos',
                              'passes_completos', 'passes_tentados', 'passes_precisao'],
                    'Posse': ['nome', 'clube', 'posicao', 'idade', 'minutos',
                             'toques_total', 'dribles_tentados', 'dribles_sucesso', 'carries_total']
                }
                
                for category, columns in stat_categories.items():
                    available_cols = [col for col in columns if col in df_season.columns]
                    if len(available_cols) > 6:
                        category_df = df_season[available_cols].copy()
                        category_df.to_excel(writer, sheet_name=category, index=False)
                
                # Rankings da temporada
                rankings = [
                    ('gols', 'Top_Gols'),
                    ('assistencias', 'Top_Assistencias'),
                    ('xg', 'Top_xG'),
                    ('minutos', 'Top_Minutos')
                ]
                
                for metric, sheet_name in rankings:
                    if metric in df_season.columns:
                        top_df = df_season.nlargest(20, metric)[
                            ['nome', 'clube', 'posicao', metric, 'minutos']
                        ].reset_index(drop=True)
                        top_df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            print(f"✅ Temporada {season} salva: {filename}")
            print(f"📊 {len(df_season)} jogadores, {df_season['clube'].nunique()} times")
            print(f"📁 Local: {excel_filepath}")
            
            return excel_filepath
            
        except Exception as e:
            print(f"❌ Erro ao salvar temporada {season}: {e}")
            return None

    def coletar_dados_selecionados(self):
        """Coleta dados com salvamento automático por temporada"""
        print(f"\n🚀 INICIANDO COLETA COM SALVAMENTO AUTOMÁTICO")
        print(f"📊 Liga: {self.current_league['name']}")
        print(f"📅 Temporadas: {', '.join(self.selected_seasons)}")
        print("💾 Salvamento: Automático após cada temporada")
        print("=" * 60)
        
        all_files_info = []
        total_teams = 0
        
        try:
            self.setup_driver()
            
            for season_idx, season in enumerate(self.selected_seasons):
                print(f"\n{'='*50}")
                print(f"📅 TEMPORADA {season} ({season_idx + 1}/{len(self.selected_seasons)})")
                print(f"{'='*50}")
                
                season_players_data = []
                teams_in_season = self.current_league["teams_by_season"].get(season, {})
                teams_processed = 0
                
                for team_name, team_id in teams_in_season.items():
                    try:
                        print(f"\n[{teams_processed + 1}/{len(teams_in_season)}] {team_name}...")
                        
                        team_data = self.scrape_team_season(team_name, team_id, season)
                        
                        if team_data:
                            season_players_data.extend(team_data)
                            teams_processed += 1
                            total_teams += 1
                            print(f"✅ {team_name} concluído - {len(team_data)} jogadores")
                        else:
                            print(f"❌ Falha ao coletar {team_name}")
                        
                        # Pausa entre times
                        time.sleep(2)
                        
                    except Exception as e:
                        print(f"❌ Erro ao processar {team_name}: {e}")
                        continue
                
                # SALVAR TEMPORADA IMEDIATAMENTE
                print(f"\n💾 SALVANDO TEMPORADA {season}...")
                excel_file = self.salvar_dados_por_temporada(season_players_data, season)
                
                file_info = {
                    'season': season,
                    'file': excel_file,
                    'success': excel_file is not None,
                    'players_count': len(season_players_data),
                    'teams_count': teams_processed,
                    'data': season_players_data if excel_file else []
                }
                all_files_info.append(file_info)
                
                print(f"\n📊 RESUMO {season}:")
                print(f"   ✅ Times processados: {teams_processed}/{len(teams_in_season)}")
                print(f"   👥 Jogadores coletados: {len(season_players_data)}")
                print(f"   💾 Arquivo salvo: {'✅' if excel_file else '❌'}")
                
                # Pausa entre temporadas
                time.sleep(3)
            
            return all_files_info
            
        except Exception as e:
            print(f"❌ Erro geral: {e}")
            return []
        
        finally:
            if self.driver:
                print("\n🔒 Fechando navegador...")
                self.driver.quit()

    def executar_coleta_interativa(self):
        """Executa coleta com salvamento automático no diretório especificado"""
        try:
            print("🏆 FOOTBALL HISTORICAL SCRAPER")
            print("📊 Scraper com salvamento automático por temporada")
            print("🎯 Suporte: Premier League e Brasileirão")
            print(f"📁 Diretório de salvamento: {self.save_directory}")
            print("=" * 80)
            
            # Verificar se o diretório existe e é acessível
            if not os.path.exists(self.save_directory):
                print(f"❌ Diretório não encontrado: {self.save_directory}")
                return
            
            if not os.access(self.save_directory, os.W_OK):
                print(f"❌ Sem permissão de escrita no diretório: {self.save_directory}")
                return
            
            print(f"✅ Diretório verificado e acessível")
            
            if not self.select_league():
                return
               
            if not self.select_seasons():
                return
            
        
            print(f"\n📋 RESUMO DA COLETA:")
            print(f"🏆 Liga: {self.current_league['name']}")
            print(f"📅 Temporadas: {', '.join(self.selected_seasons)}")
            print(f"📁 Salvamento: {self.save_directory}")
            
            total_teams = sum(len(self.current_league['teams_by_season'].get(season, {})) 
                            for season in self.selected_seasons)
            print(f"🏈 Times estimados: {total_teams}")
            print(f"👥 Jogadores estimados: {total_teams * 25} - {total_teams * 35}")
            
            estimated_time = len(self.selected_seasons) * 30
            print(f"⏱️ Tempo estimado: {estimated_time} - {estimated_time + 20} minutos")
            print(f"💾 Salvamento: Automático após cada temporada")
            
            confirmar = input("\nDeseja continuar com a coleta? (s/n): ").strip().lower()
            if confirmar != 's':
                print("❌ Coleta cancelada pelo usuário.")
                return
            
           
            files_info = self.coletar_dados_selecionados()
            
            if files_info:
                successful_files = [f for f in files_info if f['success']]
                
                if successful_files:
                    print(f"\n🎉 COLETA FINALIZADA!")
                    print(f"✅ {len(successful_files)}/{len(files_info)} temporadas salvas com sucesso")
                    print(f"📁 Todos os arquivos salvos em: {self.save_directory}")
                    print(f"🔒 Dados seguros mesmo se houver interrupção")
                    
                   
                    print(f"\n📂 ARQUIVOS CRIADOS:")
                    for file_info in files_info:
                        if file_info['success']:
                            filename = os.path.basename(file_info['file'])
                            print(f"   ✅ {filename}")
                else:
                    print(f"❌ Nenhuma temporada foi salva com sucesso.")
            else:
                print(f"❌ Nenhum dado foi coletado.")
                
        except KeyboardInterrupt:
            print("\n\n⏹️ Coleta interrompida pelo usuário.")
            print(f"💾 Dados das temporadas já processadas foram salvos em: {self.save_directory}")
        except Exception as e:
            print(f"\n❌ Erro na execução: {e}")
            print(f"💾 Verificar arquivos salvos em: {self.save_directory}")

def main():
    """Função principal"""
    scraper = FootballHistoricalScraper()
    scraper.executar_coleta_interativa()

if __name__ == "__main__":
    main()