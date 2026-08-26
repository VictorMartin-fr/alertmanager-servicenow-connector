from src.schemas.core import CoreAlert
import httpx
import uuid

"""
Jira : Alerts / OPS
"""

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

"""
Jira : Incidents / Issues
"""

class JiraIncidentClient:
    def __init__(self, domain: str, email: str, api_key: str, service_desk_id: str):
        self.instance_url = f"https://{domain}.atlassian.net/rest/servicedeskapi/request"
        self.domain = domain
        self.auth = (email, api_key)
        self.service_desk_id = service_desk_id

    async def create_alert(self, alert: CoreAlert):
        """
        POST ALERT ON JIRA ITSM
        """

        comment_builder = ""

        for label in alert.tags:
            comment_builder += f"{label}: {alert.tags[label]} \n"

        description_builder = f"""🔥 {alert.name} 🔥
        
        📦 {alert.source}
        
        *Description*: {alert.description}
        
        *Labels*:
        {{code}}
        {comment_builder}
        {{code}}
        """

        data = {
                "serviceDeskId": self.service_desk_id,
                "requestTypeId": "42",
                "requestFieldValues": {
                    "summary": alert.name,
                    "description": description_builder
                }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.instance_url,
                auth=self.auth,
                json=data,
                headers={
                    "Content-Type": "application/json"
                },
                timeout=10
            )

            response.raise_for_status()

            parsed_response = response.json()

            return {
                "ticket_id": parsed_response["issueKey"],
                "internal_id": parsed_response['issueId'],
                "message": "Alert created inside Jira ServiceDesk"
            }

    async def pause_alert(self, alert: CoreAlert, internal_id: str):
        """
        PAUSE ALERT ON JIRA SERVICEDESK
        """

        comment_builder = f"""✅ *ALERT RESOLVED* ✅
        
        *End date:* {alert.endedAt}
        
        _*Incident on hold for monitoring.*_
        """

        data = {
            "body": comment_builder,
            "public": True
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.instance_url}/{internal_id}/comment",
                auth=self.auth,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            response.raise_for_status()

            #return {
            #    "status": response.status_code,
            #    "message": "Ticket set on hold"
            #}

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://{self.domain}.atlassian.net/rest/api/3/issue/{internal_id}/transitions",
                auth=self.auth,
                json={"transition": {"id": 51}},
                headers={"Content-Type": "application/json"},
                timeout=10
            )

    async def resume_alert(self, alert: CoreAlert, internal_id: str):
        """
        RESUME INCIDENT ON JIRA SERVICEDESK
        """

        comment_builder = f"""🔄 *ALERT FIRING* 🔄
        
        ⚠️ *ALERT IS FLAPPING !* ⚠️
        
        *New alert date:* {alert.startedAt}
        """

        data = {
            "body": comment_builder,
            "public": True
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.instance_url}/{internal_id}/comment",
                auth=self.auth,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            response.raise_for_status()

            # return {
            #    "status": response.status_code,
            #    "message": "Ticket set on hold"
            # }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://{self.domain}.atlassian.net/rest/api/3/issue/{internal_id}/transitions",
                auth=self.auth,
                json={"transition": {"id": 31}},
                headers={"Content-Type": "application/json"},
                timeout=10
            )