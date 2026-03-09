from fastapi import APIRouter, BackgroundTasks
from src.schemas.alertmanager import AlertManager
from src.services.alerts_orchestrator import process_incoming_alerts_from_alertmanager

router = APIRouter()

@router.post("/alerts", status_code=202)
def receive_alerts(payload: AlertManager, background_tasks: BackgroundTasks):

    background_tasks.add_task(process_incoming_alerts_from_alertmanager,payload)

    return {
        "status": 202,
        "message": "alerts received"
    }