from pymongo import MongoClient

client = MongoClient('mongodb+srv://stephenpfeddes:mODX3ExRlJAJwDko@cluster0.h6chsrl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

db = client.player_stats_db

player_gamelogs_collection = db['player_gamelogs']
players_collection = db['players']
