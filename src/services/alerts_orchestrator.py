from src.repositories.databases_function import AlertDatabase
from src.clients.servicenow_client import ServiceNowClient
from src.schemas.alertmanager import AlertManager
from src.core.config import settings

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
        print(f"Next alert: {alert.labels['alertname']}. Status: {alert.status}")

        #Alert status : FIRING
        if alert.status == "firing":
            existing_alert = await alert_repo.get_alert_by_fingerprint(alert.fingerprint)

            if existing_alert:
                #If firing alert is resolved on database side
                if existing_alert["alertStatus"] == "resolved":
                    await snow_client.set_incident_in_progress(alert,existing_alert["snowSysId"])
                    await alert_repo.update_alert(alert)
            else:
                new_incident = await snow_client.create_incident(alert,support_team,settings.service_now.caller_id)
                await alert_repo.create_new_alert(alert, new_incident["servicenow_ticket_number"], new_incident["servicenow_sys_id"])
                print("Alert created in database, pass the next alert")

        # Alert status : RESOLVED
        elif alert.status == "resolved":
            existing_alert = await alert_repo.get_alert_by_fingerprint(alert.fingerprint)

            if existing_alert:
                #Check if the status of the incoming resolved alert is firing state
                if existing_alert["alertStatus"] == "firing":
                    await snow_client.set_incident_on_hold(alert,existing_alert["snowSysId"])
                    await alert_repo.update_alert(alert)
                else:
                    print("Alert state : resolved. Known state in database : resolved")