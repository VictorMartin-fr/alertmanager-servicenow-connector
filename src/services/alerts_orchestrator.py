from src.repositories.databases_function import AlertDatabase
from src.clients.servicenow_client import ServiceNowClient
from src.schemas.alertmanager import AlertManager
from src.core.config import settings
import logging

logger = logging.getLogger("alerts_orchestrator")

snow_client = ServiceNowClient(
    instance_id=settings.service_now.instance_id,
    username=settings.service_now.username,
    password=settings.service_now.password,
    in_progress_id=settings.service_now.state.in_progress,
    on_hold_id=settings.service_now.state.on_hold,
    on_hold_reason=settings.service_now.state.hold_reason,
)

alert_repo = AlertDatabase()

async def process_incoming_alerts_from_alertmanager(payload: AlertManager):
    support_team = payload.receiver

    for alert in payload.alerts:
        logger.info(f"alert received: {alert.labels['alertname']}, state: {alert.status}")

        #Alert status : FIRING
        if alert.status == "firing":
            existing_alert = {}
            try:
                existing_alert = await alert_repo.get_alert_by_fingerprint(alert.fingerprint)
                logger.debug(f"Alert is found in database: {existing_alert}")
            except Exception as e:
                logger.exception(f"Failed to get alert in database. Error: {e}")

            if existing_alert:
                if existing_alert["alertStatus"] == "resolved":
                    logger.info("Alert is in resolved state in database. Update status")
                    try:
                        await snow_client.set_incident_in_progress(alert,existing_alert["snowSysId"])
                        logger.debug("ServiceNow incident updated")
                    except Exception as e:
                        logger.exception(f"Failed to update ServiceNow incident. Error: {e}")
                    try:
                        await alert_repo.update_alert(alert)
                        logger.debug("Alert updated in database")
                    except Exception as e:
                        logger.exception(f"Failed to update Alert in database. Error: {e}")
            else:
                logger.debug("No alert found in database")
                new_incident = {}
                try:
                    new_incident = await snow_client.create_incident(alert,support_team,settings.service_now.caller_id)
                    logger.info(f"Incident created in ServiceNow. Reference: {new_incident["servicenow_ticket_number"]}")
                except Exception as e:
                    logger.exception(f"Failed to create incident in ServiceNow. Error: {e}")
                try:
                    await alert_repo.create_new_alert(alert, new_incident["servicenow_ticket_number"], new_incident["servicenow_sys_id"])
                    logger.debug("Alert created in database")
                except Exception as e:
                    logger.exception(f"Failed to create alert in database. Error: {e}")

        # Alert status : RESOLVED
        elif alert.status == "resolved":
            existing_alert = {}
            try:
                existing_alert = await alert_repo.get_alert_by_fingerprint(alert.fingerprint)
                logger.debug(f"Alert is found in database: {existing_alert}")
            except Exception as e:
                logger.exception(f"Failed to get alert in database. Error: {e}")

            if existing_alert:
                if existing_alert["alertStatus"] == "firing":
                    logger.info("Alert is in firing state in database. Update status")
                    try:
                        await snow_client.set_incident_on_hold(alert,existing_alert["snowSysId"])
                        logger.debug("ServiceNow incident updated")
                    except Exception as e:
                        logger.exception(f"Failed to update ServiceNow incident. Error: {e}")
                    try:
                        await alert_repo.update_alert(alert)
                        logger.debug("Alert updated in database")
                    except Exception as e:
                        logger.exception(f"Failed to update Alert in database. Error: {e}")
                else:
                    logger.debug("Alert is already in resolved state in database. Nothing to do")