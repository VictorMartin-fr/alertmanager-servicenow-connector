from src.schemas.core import CoreAlert
import httpx

class ServiceNowClient:
    def __init__(self, instance_id: str, username: str, password: str, on_hold_id: int, on_hold_reason: int, in_progress_id: int):
        self.instance_url = f"https://{instance_id}/api/now/table/incident"
        self.auth = (username, password)
        self.on_hold_id = on_hold_id
        self.on_hold_reason = on_hold_reason
        self.in_progress_id = in_progress_id

    async def create_incident(self, core_alert: CoreAlert, caller_id: str):
        """
        POST INCIDENT ON SERVICENOW
        """

        comment_builder = ""

        for label in core_alert.tags:
            comment_builder += f"{label}: {core_alert.tags[label]} <br>"

        data = {
            "caller_id": caller_id,
            "assignment_group": core_alert.support_team,
            "short_description": f"🚨 {core_alert.name}",
            "description": f"📦 Source: {core_alert.source} \n\nDescription: {core_alert.description}",
            "work_notes": f"[code] <b> Alert information: </b> <br> <pre><code> {comment_builder} </code></pre>[/code]"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.instance_url,
                auth=self.auth,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            response.raise_for_status()

            parsed_response = response.json()

            return {
                "servicenow_ticket_number": parsed_response['result']['number'],
                "servicenow_sys_id": parsed_response['result']['sys_id'],
                "message": "Alert created inside ServiceNow"
            }

    async def set_incident_on_hold(self, core_alert: CoreAlert, sys_id):
        """
        SET INCIDENT ON HOLD ON SERVICENOW
        """

        data = {
            "state": self.on_hold_id,
            "hold_reason": self.on_hold_reason,
            "work_notes": f"/// ALERT RESOLVED /// end date : {core_alert.endedAt}. Incident on hold for monitoring."
        }

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.instance_url}/{sys_id}",
                auth=self.auth,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            response.raise_for_status()

            return {
                "status": response.status_code,
                "message": "Incident set on hold"
            }

    async def set_incident_in_progress(self, core_alert: CoreAlert, sys_id):
        """
        SET INCIDENT IN PROGRESS
        """

        data = {
            "state": self.in_progress_id,
            "work_notes": f"/// ALERT FIRING /// was previously resolved. new alert at : {core_alert.startedAt}"
        }

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.instance_url}/{sys_id}",
                auth=self.auth,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            response.raise_for_status()

            return {
                "status": response.status_code,
                "message": "Incident set on hold"
            }