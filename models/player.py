from pydantic import BaseModel
from typing import Optional

# A percentile between 0 and 33 would be considered below average, 33 and 66 average, and 66 and 100 above average
class Player(BaseModel):
    player_id: int
    rotowire_id: Optional[int]
    position: str
    first_name: str
    last_name: str
    team: Optional[str]
    height: int
    weight: int
    age: int
    depth_chart_order: Optional[int]
    injury_status: Optional[str]
