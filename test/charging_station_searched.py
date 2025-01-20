# test/charging_station_searched.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ChargingStationSearched:
    user_id: str
    search_query: str
    timestamp: datetime = datetime.now()