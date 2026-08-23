from src.schemas.core import CoreAlert
import httpx
import uuid

class JiraAlertClient:
    def __init__(self, genie_key: str):
        self.instance_url = "https://api.atlassian.com/jsm/ops/integration/v2/alerts"
        self.api_key = genie_key

    async def create_alert(self, alert: CoreAlert):
        """
        POST ALERT ON JIRA OPS
        """

        internal_id = str(uuid.uuid4())

        data = {
            "message": f"🔥 {alert.name} 🔥",
            "description": f"📦 Source: {alert.source} \n\nDescription: {alert.description}",
            "alias": internal_id,
            "source": "ASC",
            "details": alert.tags
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.instance_url,
                json=data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"GenieKey {self.api_key}"
                },
                timeout=10
            )

            response.raise_for_status()

            return {
                "ticket_id": "N/A",
                "internal_id": internal_id,
                "message": "Alert created inside Jira Ops"
            }

    async def pause_alert(self, alert: CoreAlert, internal_id: str):
        """
        CLOSE ALERT ON JIRA OPS
        """

        data = {
            "user": "robot",
            "source": "ASC",
            "note": f"/// ALERT RESOLVED /// end date : {alert.endedAt}."
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.instance_url}/{internal_id}/close?identifierType=alias",
                json=data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"GenieKey {self.api_key}"
                },
            )

            response.raise_for_status()

            return {
                "status": response.status_code,
                "message": "Alert closed inside Jira Ops"
            }

    async def resume_alert(self, alert: CoreAlert, internal_id: str):
        """
        CREATE ALERT ON JIRA OPS + FLAPPING ALERT
        """

        data = {
            "message": f"🔄 {alert.name} 🔄",
            "description": f"📦 Source: {alert.source} \n\n⚠️ FLAPPING DETECTED ⚠️ \n\nDescription: {alert.description}",
            "alias": internal_id,
            "source": "ASC",
            "details": alert.tags
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.instance_url,
                json=data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"GenieKey {self.api_key}"
                },
                timeout=10
            )

            response.raise_for_status()

            return {
                "status": response.status_code,
                "internal_id": internal_id,
                "message": "Alert created inside Jira Ops"
            }