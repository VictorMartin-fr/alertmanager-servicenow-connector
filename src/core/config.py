from typing import Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, YamlConfigSettingsSource

import logging

class SchedulerConfig(BaseModel):
    scheduler_interval: Optional[int] = Field(default=1)
    keep_alert_interval: Optional[int] = Field(default=24)

class GeneralConfig(BaseModel):
    scheduled_task: SchedulerConfig

class ServiceNowStateConfig(BaseModel):
    in_progress: Optional[int]
    on_hold: Optional[int]
    hold_reason: Optional[int]

class ServiceNowConfig(BaseModel):
    enabled: Optional[bool] = Field(default=False)
    module: Optional[str] = Field(default="incident")
    instance_id: Optional[str]
    username: Optional[str]
    password: Optional[str]
    caller_id: Optional[str]
    state: ServiceNowStateConfig

class MongoDbConfig(BaseModel):
    hostname: Optional[str]
    port: Optional[int]
    username: Optional[str]
    password: Optional[str]
    database: Optional[str]
    collection: Optional[str]

class NotifierZulipConfig(BaseModel):
    enabled: Optional[bool] = Field(default=False)
    instance_url: Optional[str]
    email: Optional[str]
    api_key: Optional[str]
    channel: Optional[str]

class NotifierSlackConfig(BaseModel):
    enabled: Optional[bool] = Field(default=False)
    webhook_url: Optional[str]

class JiraConfig(BaseModel):
    enabled: Optional[bool] = Field(default=False)
    module: Optional[str] = Field(default="incident")
    cloud_id: Optional[str]
    email: Optional[str]
    api_key: Optional[str]
    genie_key: Optional[str]

class Settings(BaseSettings):
    general: GeneralConfig
    service_now: ServiceNowConfig
    mongodb: MongoDbConfig
    zulip: NotifierZulipConfig
    slack: NotifierSlackConfig
    jira: JiraConfig

    model_config = SettingsConfigDict(
        env_prefix="ASC_",
        env_nested_delimiter="__"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,
            YamlConfigSettingsSource(settings_cls, "./config.yaml"),
            init_settings,
        )

settings = Settings()