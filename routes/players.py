from fastapi import APIRouter
from models.player_gamelog import PlayerGamelog
from config.database import players_collection
from schemas.serialize_players import serialize_players

players_router = APIRouter()

@players_router.get("/api/v1/players")
async def get_players_gamelogs():
    players = serialize_players(players_collection.find())
    return players