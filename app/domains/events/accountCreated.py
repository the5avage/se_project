from dataclasses import dataclass
from datetime import datetime

@dataclass
class AccountCreated:
    user_id: str
    timestamp: datetime = datetime.now()
    
