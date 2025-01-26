from dataclasses import dataclass
from datetime import datetime

@dataclass
class AccountLoggedIn:
    user_id: str
    timestamp: datetime = datetime.now()
    