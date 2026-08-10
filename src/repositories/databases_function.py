from src.schemas.core import CoreAlert
from src.core.database import db_instance
from src.core.config import settings

class AlertDatabase:

    @property
    def collection(self):
        return db_instance.db[settings.mongodb.collection]

    async def get_alert_by_fingerprint(self, fingerprint: str):
        """
        Search for alert inside MongoDB by fingerprint
        """
        return await self.collection.find_one({"fingerprint": fingerprint})

    async def create_new_alert(self, core_alert: CoreAlert, ticket_id: str, internal_id: str):
        """
        Create new alert inside MongoDB
        """
        document = {
            "alertName": core_alert.name,
            "ticket_id": ticket_id,
            "internal_id": internal_id,
            "alertStatus": core_alert.status,
            "alertStartDate": core_alert.startedAt,
            "alertEndDate": core_alert.endedAt,
            "fingerprint": core_alert.fingerprint
        }
        await self.collection.insert_one(document)

    async def update_alert(self, core_alert: CoreAlert):
        """
        Update alert status in MongoDB
        """
        filter_query = {"fingerprint": core_alert.fingerprint}
        document_update = {
            "$set": {
                "alertStatus": core_alert.status,
                "alertEndDate": core_alert.endedAt
            }
        }
        await self.collection.update_one(filter_query,document_update)