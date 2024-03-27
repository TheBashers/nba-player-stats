from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from services.webscrape_gamelogs import webscrape_gamelogs
from routes.player_gamelogs import player_gamelogs_router
from routes.players import players_router
from services.fetch_nba_players import fetch_nba_players

app = FastAPI()

@app.get("/")
async def get_root():
    return "Draftbash player statistics API"

#scheduler = BackgroundScheduler()
#scheduler.start()

#scheduler.add_job(webscrape_gamelogs, "interval", seconds=5)

app.include_router(player_gamelogs_router)

app.include_router(players_router)