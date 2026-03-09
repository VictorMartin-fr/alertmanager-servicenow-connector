from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class Alert(BaseModel):
    """
    AlertManager single alert class
    """
    status: str
    labels: Dict[str, str]
    annotations: Dict[str, str]
    startsAt: Optional[datetime]
    endsAt: Optional[datetime]
    generatorURL: Optional[str]
    fingerprint: str

class AlertManager(BaseModel):
    """
    AlertManager payload class
    """
    receiver: str
    status: str
    alerts: List[Alert]
    groupLabels: Optional[Dict[str, str]]
    commonLabels: Optional[Dict[str, str]]
    commonAnnotations: Optional[Dict[str, str]]
    externalURL: Optional[str]
    version: Optional[str]
    groupKey: Optional[str]