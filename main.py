from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
#from services.webscrape_gamelogs import webscrape_gamelogs
from routes.player_gamelogs import player_gamelogs_router
from routes.players import players_router
from services.fetch_nba_players import webscrape_nba_players
from services.test import test

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the appropriate origin or use ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Adjust the allowed HTTP methods as needed
    allow_headers=["*"],  # Allow all headers or specify the required headers
)

@app.get("/")
async def get_root():
    return "Draftbash player statistics API"

#scheduler = BackgroundScheduler()
#scheduler.start()

#scheduler.add_job(webscrape_gamelogs, "interval", seconds=5)

app.include_router(player_gamelogs_router)

app.include_router(players_router)