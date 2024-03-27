from fastapi import APIRouter
from models.player_gamelog import PlayerGamelog
from config.database import player_gamelogs_collection
from schemas.serialize_player_gamelogs import serialize_player_gamelogs
from bson import ObjectId

player_gamelogs_router = APIRouter()

@player_gamelogs_router.get("/api/v1/players/gamelogs")
async def get_players_gamelogs():
    players_gamelogs = serialize_player_gamelogs(player_gamelogs_collection.find())
    return players_gamelogs

@player_gamelogs_router.post("/api/v1/players/gamelogs")
async def add_player_gamelog(player_gamelog: PlayerGamelog):
    player_gamelogs_collection.update_one(
        {"player_id": dict(player_gamelog)["player_id"], "date": dict(player_gamelog)["date"]},
        {"$set": dict(player_gamelog)},
        upsert=True
    )