def serialize_player_gamelog(player_gamelog) -> dict:
    return {
        "id": str(player_gamelog["_id"]),
        "season": player_gamelog["season"],
        "date": player_gamelog["date"],
        "team": player_gamelog["team"],
        "is_home_game": player_gamelog["is_home_game"],
        "opponent_team": player_gamelog["opponent_team"],
        "player_team_score": player_gamelog["player_team_score"],
        "opponent_team_score": player_gamelog["opponent_team_score"],
        "player_id": player_gamelog["player_id"],
        "position": player_gamelog["position"],
        "is_starter": player_gamelog["is_starter"],
        "minutes_played": player_gamelog["minutes_played"],
        "points": player_gamelog["points"],
        "fieldgoals_made": player_gamelog["fieldgoals_made"],
        "fieldgoals_attempted": player_gamelog["fieldgoals_attempted"],
        "threes_made": player_gamelog["threes_made"],
        "threes_attempted": player_gamelog["threes_attempted"],
        "freethrows_made": player_gamelog["freethrows_made"],
        "freethrows_attempted": player_gamelog["freethrows_attempted"],
        "offensive_rebounds": player_gamelog["offensive_rebounds"],
        "defensive_rebounds": player_gamelog["defensive_rebounds"],
        "total_rebounds": player_gamelog["total_rebounds"],
        "assists": player_gamelog["assists"],
        "steals": player_gamelog["steals"],
        "blocks": player_gamelog["blocks"],
        "turnovers": player_gamelog["turnovers"],
        "fouls": player_gamelog["fouls"],
        "plus_minus": player_gamelog["plus_minus"]
    }

def serialize_player_gamelogs(player_gamelog) -> list:
    return [serialize_player_gamelog(player_gamelog) for player_gamelog in player_gamelog]