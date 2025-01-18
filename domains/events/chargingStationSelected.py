from dataclasses import dataclass
from datetime import datetime

@dataclass
class ChargingStationSelected:
    user_id: str
    station_id: str
    timestamp: datetime = datetime.now()