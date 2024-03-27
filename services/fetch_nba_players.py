import requests
from models.player import Player
from config.database import players_collection

def fetch_nba_players():
    response = requests.get('https://api.sleeper.app/v1/players/nba')
    for player_id, player_data in response.json().items():
        try:
            if player_data['swish_id']:
                player = Player(
                    player_id=player_data['swish_id'],
                    rotowire_id=player_data['rotowire_id'],
                    position=player_data['position'],
                    first_name=player_data['first_name'],
                    last_name=player_data['last_name'],
                    team=player_data['team'],
                    height=player_data['height'],
                    weight=player_data['weight'],
                    age=player_data['age'],
                    depth_chart_order=player_data['depth_chart_order'],
                    injury_status=player_data['injury_status']
                )
                players_collection.update_one(
                    {"player_id": dict(player)["player_id"]},
                    {"$set": dict(player)},
                    upsert=True
                )
        except Exception as e:
            print(e)
