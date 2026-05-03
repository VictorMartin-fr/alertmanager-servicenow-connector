from fastapi import APIRouter, BackgroundTasks

from src.schemas.healthcheck import HealthCheck
from src.schemas.alertmanager import AlertManager
from src.services.alerts_orchestrator import process_incoming_alerts_from_alertmanager, process_incoming_ping_from_healthcheck

router = APIRouter()

@router.post("/alertmanager/alerts", status_code=202)
def receive_alerts(payload: AlertManager, background_tasks: BackgroundTasks):

    background_tasks.add_task(process_incoming_alerts_from_alertmanager,payload)

    return {
        "status": 202,
        "message": "alerts received"
    }

@router.post("/healthcheck/ping/{tenant_name}", status_code=202)
def receive_ping(tenant_name: str, payload: HealthCheck, background_tasks: BackgroundTasks):

    background_tasks.add_task(process_incoming_ping_from_healthcheck,payload,tenant_name)
    return {
        "status": 202,
        "message": "ping received"
    }