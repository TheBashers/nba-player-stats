from models.player_gamelog import PlayerGamelog
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from config.database import player_gamelogs_collection
from config.database import players_collection
from schemas.serialize_players import serialize_players
import time

def webscrape_gamelogs():

    players = {player['player_id']: player for player in serialize_players(players_collection.find())}

    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    current_season = None

    if current_month >= 10 and current_month <= 12:
        current_season = current_year+1
    elif current_month >= 1 and current_month <= 4:
        current_season = current_year

    seasons = [current_season-1, current_season]
    game_dates = []
    for season in seasons:
        start_date = datetime(season-1, 10, 1)
        end_date = datetime(season, 4, 30) 

        current_date = start_date
        while current_date <= end_date:
            game_dates.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)
            if current_date.month == 4 and current_date.day > 10:
                break

    for game_date in game_dates:
        time.sleep(.5)
        season = int(game_date.split('-')[0])
        month = int(game_date.split('-')[1]) 
        if month <= 4:
            season-=1
        matchups_response = requests.get(f'https://sportsdata.usatoday.com/basketball/nba/scores?season={season}&date={game_date}')
        soup = BeautifulSoup(matchups_response.text, 'html')
        boxscore_btns = soup.find_all(class_='class-ubgFKmr')
        game_ids = [game.find('a').get('href').split('/')[4] for game in boxscore_btns]
        for game_id in game_ids:
            try:
                time.sleep(.5)

                matchup_response = requests.get(f'https://sportsdata.usatoday.com/basketball/nba/scores/{game_id}')
                soup = BeautifulSoup(matchup_response.text, 'html')
                tables = soup.find(class_='class-rsiWjCO').find_all('tbody')
                home_starter_rows = [table.find_all('tr') for table in tables][0]
                away_starter_rows = [table.find_all('tr') for table in tables][1]
                home_bench_player_rows = [table.find_all('tr') for table in tables][2]
                away_bench_player_rows = [table.find_all('tr') for table in tables][3]

                home_team_abbreviation = soup.find(class_='class-77G4-Jb').find_all(class_='class-yNdnxnv')[0].text
                away_team_abbreviation = soup.find(class_='class-77G4-Jb').find_all(class_='class-yNdnxnv')[1].text
                team_abbreviations = {'home': home_team_abbreviation, 'away': away_team_abbreviation}

                player_roles = {
                    'starters': {'home': home_starter_rows, 'away': away_starter_rows}, 
                    'bench_players': {'home': home_bench_player_rows, 'away': away_bench_player_rows}
                }
                for player_role, teams in player_roles.items():
                    started_game = False
                    if player_role=='starters':
                        started_game = True

                    for team in teams.keys():
                        player_team = None
                        opposing_team = None
                        player_team_score = None
                        is_home_game = None
                        opposing_team_score = None

                        if team=='home':
                            player_team = team_abbreviations['home']
                            player_team_score = int(soup.find_all(class_='class-MPFG1-M')[0].text)
                            opposing_team_score = int(soup.find_all(class_='class-MPFG1-M')[1].text)
                            opposing_team = team_abbreviations['away']
                            is_home_game = True
                        else:
                            player_team = team_abbreviations['away']
                            player_team_score = int(soup.find_all(class_='class-MPFG1-M')[1].text)
                            opposing_team_score = int(soup.find_all(class_='class-MPFG1-M')[0].text)
                            opposing_team = team_abbreviations['home']
                            is_home_game = False

                        gamelogs = [player_data.find_all('td') for player_data in player_roles[player_role][team]]
                        for gamelog in gamelogs:
                            player_id = int(gamelog[0].find('a').get('href').split('/')[5])
                            if len(gamelog) == 15:
                                minutes_played = float(gamelog[1].text.split(':')[0]) + float(gamelog[1].text.split(':')[1])/60
                                points_scored = int(gamelog[2].text)
                                threes_made = int(gamelog[4].text.split('-')[0])
                                threes_attempted = int(gamelog[4].text.split('-')[1])
                                fieldgoals_made = int(gamelog[3].text.split('-')[0])
                                fieldgoals_attempted = int(gamelog[3].text.split('-')[1])
                                freethrows_made = float(gamelog[5].text.split('-')[0])
                                freethrows_attempted = float(gamelog[5].text.split('-')[1])
                                offensive_rebounds = int(gamelog[6].text)
                                defensive_rebounds = int(gamelog[7].text)
                                rebounds_total = int(gamelog[8].text)
                                assists = int(gamelog[9].text)
                                turnovers = int(gamelog[10].text)
                                steals = int(gamelog[11].text)
                                blocks = int(gamelog[12].text)
                                fouls = int(gamelog[13].text)
                                plus_minus = int(gamelog[14].text)
                                position = players[player_id]['position']

                                gamelog = PlayerGamelog(
                                    season=season,
                                    date=game_date,
                                    team=player_team,
                                    is_home_game=is_home_game,
                                    opponent_team=opposing_team,
                                    player_team_score=player_team_score,
                                    opponent_team_score=opposing_team_score,
                                    player_id=player_id,
                                    position=position,
                                    is_starter=started_game,
                                    minutes_played=minutes_played,
                                    points=points_scored,
                                    fieldgoals_made=fieldgoals_made,
                                    fieldgoals_attempted=fieldgoals_attempted,
                                    threes_made=threes_made,
                                    threes_attempted=threes_attempted,
                                    freethrows_made=freethrows_made,
                                    freethrows_attempted=freethrows_attempted,
                                    offensive_rebounds=offensive_rebounds,
                                    defensive_rebounds=defensive_rebounds,
                                    total_rebounds=rebounds_total,
                                    assists=assists,
                                    steals=steals,
                                    blocks=blocks,
                                    turnovers=turnovers,
                                    fouls=fouls,
                                    plus_minus=plus_minus
                                )
                                player_gamelogs_collection.update_one(
                                    {"player_id": dict(gamelog)["player_id"], "date": dict(gamelog)["date"]},
                                    {"$set": dict(gamelog)},
                                    upsert=True
                                )
                            else:
                                gamelog = PlayerGamelog(
                                    season=season,
                                    date=game_date,
                                    team=player_team,
                                    is_home_game=is_home_game,
                                    opponent_team=opposing_team,
                                    player_team_score=player_team_score,
                                    opponent_team_score=opposing_team_score,
                                    player_id=player_id,
                                    position=position,
                                    is_starter=False,
                                    minutes_played=0,
                                    points=0,
                                    fieldgoals_made=0,
                                    fieldgoals_attempted=0,
                                    threes_made=0,
                                    threes_attempted=0,
                                    freethrows_made=0,
                                    freethrows_attempted=0,
                                    offensive_rebounds=0,
                                    defensive_rebounds=0,
                                    total_rebounds=0,
                                    assists=0,
                                    steals=0,
                                    blocks=0,
                                    turnovers=0,
                                    fouls=0,
                                    plus_minus=0
                                )
                                player_gamelogs_collection.update_one(
                                    {"player_id": dict(gamelog)["player_id"], "date": dict(gamelog)["date"]},
                                    {"$set": dict(gamelog)},
                                    upsert=True
                                )
            except Exception as e: 
                print(e)