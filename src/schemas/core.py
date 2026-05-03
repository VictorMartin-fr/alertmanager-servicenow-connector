from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class CoreAlert(BaseModel):
    """
    CoreAlert class (internal object)
    """
    fingerprint: str
    name: str
    status: str
    startedAt: Optional[datetime]
    endedAt: Optional[datetime]
    tags: Dict[str, str]
    description: str
    source: str
    support_team: str