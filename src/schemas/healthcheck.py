from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class HealthCheck(BaseModel):
    """
    Healthcheck ping class
    """
    name: str
    status: str
    date: Optional[datetime]
    tags: Union[str, Dict[str, str]]
    support_team: str
    fingerprint: str

    @field_validator('tags',mode='before')
    @classmethod
    def parse_tags_to_dict(cls, v: Any) -> Dict[str, str]:
        if not isinstance(v, str):
            return {}

        parsed_labels = {}

        for tag in v.split():
            if ":" in tag:
                key, value = tag.split(":", 1)
                parsed_labels[key] = value
            else:
                parsed_labels[tag] = "true"

        return parsed_labels