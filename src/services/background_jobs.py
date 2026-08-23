import datetime
import logging
from src.repositories.databases_function import alert_repo

logger = logging.getLogger("alerts_orchestrator")

async def clean_resolved_alerts():
    """
    Scheduled job : Delete all resolved alerts
    """
    logger.info("[SCHEDULER] beginning deleting resolved alerts")
    limit_date = datetime.datetime.now() - datetime.timedelta(hours=24)
    try:
        result = await alert_repo.delete_alert(limit_date)
        logger.info(f"[SCHEDULER] {result["row_count"]} alerts deleted")
    except Exception as e:
        logger.exception(f"[SCHEDULER] Failed to clean old alerts. Error: {e}")