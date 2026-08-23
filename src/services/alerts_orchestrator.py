from src.schemas.core import CoreAlert
from src.schemas.healthcheck import HealthCheck, HealthcheckPayload
from src.services.notification_manager import notify
from src.services.incident_manager import ticketing
from src.repositories.databases_function import alert_repo
from src.schemas.alertmanager import AlertManager
import logging

logger = logging.getLogger("alerts_orchestrator")

"""
AlertManager/Grafana alert orchestrator
"""

async def process_incoming_alerts_from_alertmanager(payload: AlertManager):

    for alert in payload.alerts:
        logger.info(f"alert received: {alert.labels['alertname']}, state: {alert.status}")

        core_alert = CoreAlert(
            fingerprint=alert.fingerprint,
            name=alert.labels["alertname"],
            status=alert.status,
            startedAt=alert.startsAt,
            endedAt=alert.endsAt,
            tags=alert.labels,
            description=alert.annotations['description'],
            source="alertmanager",
            support_team=payload.receiver
        )

        #Alert status : FIRING
        if alert.status == "firing":
            existing_alert = {}
            try:
                existing_alert = await alert_repo.get_alert_by_fingerprint(core_alert.fingerprint)
                logger.debug(f"Alert is found in database: {existing_alert}")
            except Exception as e:
                logger.exception(f"Failed to get alert in database. Error: {e}")
                continue

            if existing_alert:
                if existing_alert["alertStatus"] == "resolved":
                    logger.info("Alert is in resolved state in database. Update status")
                    try:
                        await ticketing.resume_ticket(core_alert, existing_alert["internal_id"])
                        logger.debug("ServiceNow incident updated")
                    except Exception as e:
                        logger.exception(f"Failed to update ServiceNow incident. Error: {e}")
                        continue
                    try:
                        await alert_repo.update_alert(core_alert)
                        logger.debug("Alert updated in database")
                    except Exception as e:
                        logger.exception(f"Failed to update Alert in database. Error: {e}")
                        continue
                    try:
                        await notify.notify_all(core_alert, is_flapping=True)
                        logger.debug("Notification sent in all application enabled")
                    except Exception as e:
                        logger.exception(f"Failed to notify an application. Error: {e}")
            else:
                logger.debug("No alert found in database")
                new_incident = {}
                try:
                    new_incident = await ticketing.create_ticket(core_alert)
                    logger.info(f"Incident created in ServiceNow. Reference: {new_incident["ticket_id"]}")
                except Exception as e:
                    logger.exception(f"Failed to create incident in ServiceNow. Error: {e}")
                    continue
                try:
                    await alert_repo.create_new_alert(core_alert, new_incident["ticket_id"], new_incident["internal_id"])
                    logger.debug("Alert created in database")
                except Exception as e:
                    logger.exception(f"Failed to create alert in database. Error: {e}")
                    continue
                try:
                    await notify.notify_all(core_alert, is_flapping=False)
                    logger.debug("Notification sent in all application enabled")
                except Exception as e:
                    logger.exception(f"Failed to notify an application. Error: {e}")

        # Alert status : RESOLVED
        elif alert.status == "resolved":
            existing_alert = {}
            try:
                existing_alert = await alert_repo.get_alert_by_fingerprint(core_alert.fingerprint)
                logger.debug(f"Alert is found in database: {existing_alert}")
            except Exception as e:
                logger.exception(f"Failed to get alert in database. Error: {e}")

            if existing_alert:
                if existing_alert["alertStatus"] == "firing":
                    logger.info("Alert is in firing state in database. Update status")
                    try:
                        await ticketing.pause_ticket(core_alert, existing_alert["internal_id"])
                        logger.debug("ServiceNow incident updated")
                    except Exception as e:
                        logger.exception(f"Failed to update ServiceNow incident. Error: {e}")
                    try:
                        await alert_repo.update_alert(core_alert)
                        logger.debug("Alert updated in database")
                    except Exception as e:
                        logger.exception(f"Failed to update Alert in database. Error: {e}")
                    try:
                        await notify.notify_all(core_alert, is_flapping=False)
                        logger.debug("Notification sent in all application enabled")
                    except Exception as e:
                        logger.exception(f"Failed to notify an application. Error: {e}")
                else:
                    logger.debug("Alert is already in resolved state in database. Nothing to do")

"""
Healthcheck ping orchestrator
"""

async def process_incoming_ping_from_healthcheck(payload: HealthcheckPayload, tenant_name: str):
    core_alert = CoreAlert(
        fingerprint=payload.alert.uuid,
        name=f"Healthcheck / Check: {payload.alert.name} / Tenant: {tenant_name}",
        status="firing" if payload.alert.status == "down" else "resolved",
        startedAt=payload.alert.last_ping if payload.alert.status == "down" else None,
        endedAt=payload.alert.last_ping if payload.alert.status == "up" else None,
        tags=payload.alert.tags,
        description=payload.alert.desc,
        source="healthcheck",
        support_team=payload.alert.tags["support_team"]
    )

    logger.info(f"Ping received from Healthcheck. Tenant: {tenant_name}, check: {payload.alert.name}, status: {payload.alert.status}")

    if core_alert.status == "firing":
        existing_alert = {}
        try:
            existing_alert = await alert_repo.get_alert_by_fingerprint(core_alert.fingerprint)
            logger.debug(f"Alert is found in database: {existing_alert}")
        except Exception as e:
            logger.exception(f"Failed to get alert in database. Error: {e}")
            return

        if existing_alert:
            if existing_alert["alertStatus"] == "resolved":
                logger.info("Alert is in state resolved in database. Update status")
                try:
                    await ticketing.resume_ticket(core_alert, existing_alert["internal_id"])
                    logger.debug("ServiceNow incident updated")
                except Exception as e:
                    logger.exception(f"Failed to update ServiceNow incident. Error: {e}")
                    return
                try:
                    await alert_repo.update_alert(core_alert)
                    logger.debug("Alert updated in database")
                except Exception as e:
                    logger.exception(f"Failed to update Alert in database. Error: {e}")
                    return
                try:
                    await notify.notify_all(core_alert, is_flapping=True)
                    logger.debug("Notification sent in all application enabled")
                except Exception as e:
                    logger.exception(f"Failed to notify an application. Error: {e}")
        else:
            logger.debug("No alert found in database")
            new_incident = {}
            try:
                new_incident = await ticketing.create_ticket(core_alert)
                logger.info(f"Incident created in ServiceNow. Reference: {new_incident["ticket_id"]}")
            except Exception as e:
                logger.exception(f"Failed to create incident in ServiceNow. Error: {e}")
                return
            try:
                await alert_repo.create_new_alert(core_alert, new_incident["ticket_id"], new_incident["internal_id"])
                logger.debug("Alert created in database")
            except Exception as e:
                logger.exception(f"Failed to create alert in database. Error: {e}")
                return
            try:
                await notify.notify_all(core_alert, is_flapping=False)
                logger.debug("Notification sent in all application enabled")
            except Exception as e:
                logger.exception(f"Failed to notify an application. Error: {e}")

    # Alert status : RESOLVED
    elif core_alert.status == "resolved":
        existing_alert = {}
        try:
            existing_alert = await alert_repo.get_alert_by_fingerprint(core_alert.fingerprint)
            logger.debug(f"Alert is found in database: {existing_alert}")
        except Exception as e:
            logger.exception(f"Failed to get alert in database. Error: {e}")
            return

        if existing_alert:
            if existing_alert["alertStatus"] == "firing":
                logger.info("Alert is in firing state in database. Update status")
                try:
                    await ticketing.pause_ticket(core_alert, existing_alert["internal_id"])
                    logger.debug("ServiceNow incident updated")
                except Exception as e:
                    logger.exception(f"Failed to update ServiceNow incident. Error: {e}")
                    return
                try:
                    await alert_repo.update_alert(core_alert)
                    logger.debug("Alert updated in database")
                except Exception as e:
                    logger.exception(f"Failed to update Alert in database. Error: {e}")
                    return
                try:
                    await notify.notify_all(core_alert, is_flapping=False)
                    logger.debug("Notification sent in all application enabled")
                except Exception as e:
                    logger.exception(f"Failed to notify an application. Error: {e}")
                    return
            else:
                logger.debug("Alert is already in resolved state in database. Nothing to do")

