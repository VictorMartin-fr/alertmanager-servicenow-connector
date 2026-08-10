from src.schemas.core import CoreAlert

class IncidentManager:
    def __init__(self):
        self.active_provider = None

    def register_provider(self, client):
        self.active_provider = client

    async def create_ticket(self, alert: CoreAlert):
        if not self.active_provider:
            return {
                    "ticket_id": None,
                    "internal_id": None
                }

        return await self.active_provider.create_alert(alert)

    async def pause_ticket(self, alert: CoreAlert, internal_id: str):
        if not self.active_provider:
            return None, None

        return await self.active_provider.pause_alert(alert, internal_id)

    async def resume_ticket(self, alert: CoreAlert, internal_id: str):
        if not self.active_provider:
            return None, None

        return await self.active_provider.resume_alert(alert, internal_id)

    async def resolve_ticket(self, alert: CoreAlert, internal_id: str):
        if not self.active_provider:
            return None, None

        return await self.active_provider.resolve_alert(alert, internal_id)

ticketing = IncidentManager()