from fastapi import FastAPI
from src.core.database import connect_to_mongo,close_mongo_connection
from src.core.config import settings
from src.clients.zulip_client import ZulipClient
from src.services.notification_manager import notify
from src.api import webhook

import logging

#Logging configuration

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger('main')

async def lifespan(app: FastAPI):
    print("ASC API starting...")
    #Database connection initialization
    await connect_to_mongo()

    #Notification connector initialization
    ##Zulip
    if settings.zulip.enabled:
        zulip = ZulipClient(
            instance_url=settings.zulip.instance_url,
            email=settings.zulip.email,
            api_key=settings.zulip.api_key,
            channel=settings.zulip.channel
        )
        notify.register_notifier(zulip)

    yield

    print("ASC API ending...")
    close_mongo_connection()

app = FastAPI(
    title = "ASC",
    description = "API to connect AlertManager to ServiceNow while reduce noise",
    version = "0.0.1",
    lifespan=lifespan
)

app.include_router(webhook.router)

@app.get("/health", tags=["System"])
def health_check():
    """
    Health check endpoint
    """
    return {"status": "ok", "message": "Bridge is running"}