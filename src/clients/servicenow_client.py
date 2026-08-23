from src.schemas.core import CoreAlert
import httpx

class ServiceNowClient:
    def __init__(self, instance_id: str, username: str, password: str, caller_id: str, on_hold_id: int, on_hold_reason: int, in_progress_id: int):
        self.instance_url = f"https://{instance_id}/api/now/table/incident"
        self.auth = (username, password)
        self.caller_id = caller_id
        self.on_hold_id = on_hold_id
        self.on_hold_reason = on_hold_reason
        self.in_progress_id = in_progress_id

    async def create_alert(self, alert: CoreAlert):
        """
        POST INCIDENT ON SERVICENOW
        """

        comment_builder = ""

        for label in alert.tags:
            comment_builder += f"{label}: {alert.tags[label]} <br>"

        data = {
            "caller_id": self.caller_id,
            "assignment_group": alert.support_team,
            "short_description": f"🚨 {alert.name}",
            "description": f"📦 Source: {alert.source} \n\nDescription: {alert.description}",
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
                    "ticket_id": parsed_response['result']['number'],
                    "internal_id": parsed_response['result']['sys_id'],
                    "message": "Alert created inside ServiceNow"
                }

    async def pause_alert(self, alert: CoreAlert, internal_id: str):
        """
        PAUSE INCIDENT ON SERVICENOW
        """

        data = {
            "state": self.on_hold_id,
            "hold_reason": self.on_hold_reason,
            "work_notes": f"/// ALERT RESOLVED /// end date : {alert.endedAt}. Incident on hold for monitoring."
        }

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.instance_url}/{internal_id}",
                auth=self.auth,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            response.raise_for_status()

            return {
                "status": response.status_code,
                "message": "Ticket set on hold"
            }

    async def resume_alert(self, alert: CoreAlert, internal_id: str):
        """
        RESUME INCIDENT ON SERVICENOW
        """

        data = {
            "state": self.in_progress_id,
            "work_notes": f"/// ALERT FIRING /// was previously resolved. new alert at : {alert.startedAt}"
        }

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.instance_url}/{internal_id}",
                auth=self.auth,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            response.raise_for_status()

            return {
                "status": response.status_code,
                "message": "Ticket set in progress"
            }