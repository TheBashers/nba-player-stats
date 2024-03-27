from pydantic import BaseModel

# A percentile between 0 and 33 would be considered below average, 33 and 66 average, and 66 and 100 above average
class PlayerGamelog(BaseModel):
    season: int
    date: str
    team: str
    is_home_game: bool
    opponent_team: str
    player_team_score: int
    opponent_team_score: int
    player_id: int
    position: str
    is_starter: bool
    minutes_played: float
    points: int
    fieldgoals_made: int
    fieldgoals_attempted: int
    threes_made: int
    threes_attempted: int
    freethrows_made: int
    freethrows_attempted: int
    offensive_rebounds: int
    defensive_rebounds: int
    total_rebounds: int
    assists: int
    steals: int
    blocks: int
    turnovers: int
    fouls: int
    plus_minus: int