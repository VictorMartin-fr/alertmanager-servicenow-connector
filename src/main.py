from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.core.database import connect_to_mongo,close_mongo_connection
from src.core.config import settings
from src.clients.zulip_client import ZulipClient
from src.clients.slack_client import SlackClient
from src.clients.servicenow_client import ServiceNowClient
from src.services.notification_manager import notify
from src.services.incident_manager import ticketing
from src.services.background_jobs import clean_resolved_alerts
from src.api import webhook

import logging

#Logging configuration

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger('main')

#Scheduler initialization
scheduler = AsyncIOScheduler()

async def lifespan(app: FastAPI):
    print("ASC API starting...")
    #Database connection initialization
    await connect_to_mongo()

    #Scheduler setup
    scheduler.start()
    scheduler.add_job(clean_resolved_alerts, 'interval', hours=settings.general.scheduled_task.scheduler_interval)

    #Ticketing connector initialization
    ##ServiceNow : Incident
    if settings.service_now.enabled and settings.service_now.module == "incident":
        logger.info("[Module] enabling ServiceNow as Incident mode")
        snow_incident = ServiceNowClient(
            instance_id=settings.service_now.instance_id,
            username=settings.service_now.username,
            password=settings.service_now.password,
            caller_id=settings.service_now.caller_id,
            on_hold_id=settings.service_now.state.on_hold,
            on_hold_reason=settings.service_now.state.hold_reason,
            in_progress_id=settings.service_now.state.in_progress
        )
        ticketing.register_provider(snow_incident)

    #Notification connector initialization
    ##Slack
    if settings.slack.enabled:
        logger.info("[Module] enabling Slack")
        slack = SlackClient(
            webhook_url=settings.slack.webhook_url
        )
        notify.register_notifier(slack)
    ##Zulip
    if settings.zulip.enabled:
        logger.info("[Module] enabling Zulip")
        zulip = ZulipClient(
            instance_url=settings.zulip.instance_url,
            email=settings.zulip.email,
            api_key=settings.zulip.api_key,
            channel=settings.zulip.channel
        )
        notify.register_notifier(zulip)

    yield

    print("ASC API ending...")
    scheduler.shutdown()
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