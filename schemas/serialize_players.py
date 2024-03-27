from models.player import Player

def serialize_player(player: Player) -> dict:
    return {
        "player_id": player["player_id"],
        "rotowire_id": player["rotowire_id"],
        "position": player["position"],
        "first_name": player["first_name"],
        "last_name": player["last_name"],
        "team": player["team"],
        "height": player["height"],
        "weight": player["weight"],
        "age": player["age"],
        "depth_chart_order": player["depth_chart_order"],
        "injury_status": player["injury_status"]
    }

def serialize_players(players) -> list:
    return [serialize_player(player) for player in players]