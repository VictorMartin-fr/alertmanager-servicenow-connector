from typing import Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, YamlConfigSettingsSource

import logging

class ServiceNowStateConfig(BaseModel):
    in_progress: Optional[int]
    on_hold: Optional[int]
    hold_reason: Optional[int]

class ServiceNowConfig(BaseModel):
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

class Settings(BaseSettings):
    service_now: ServiceNowConfig
    mongodb: MongoDbConfig
    zulip: NotifierZulipConfig

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