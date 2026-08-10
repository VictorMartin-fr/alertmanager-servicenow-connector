from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class HealthCheck(BaseModel):
    """
    Healthcheck ping class
    """
    name: str
    slug: Optional[str]
    tags: Optional[Union[str, Dict[str, str]]]
    desc: Optional[str]
    grace: int
    n_pings: int
    status: str
    started: bool
    last_ping: Optional[datetime]
    next_ping: Optional[datetime]
    manual_resume: bool
    methods: Optional[str]
    subject: Optional[str]
    subject_fail: Optional[str]
    start_kw: Optional[str]
    success_kw: Optional[str]
    failure_kw: Optional[str]
    filter_subject: bool
    filter_body: bool
    filter_http_body: bool
    filter_default_fail: bool
    badge_url: str
    uuid: str
    ping_url: str
    update_url: str
    pause_url: str
    resume_url: str
    channels: str
    timeout: int

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

class HealthcheckPayload(BaseModel):
    alert: HealthCheck