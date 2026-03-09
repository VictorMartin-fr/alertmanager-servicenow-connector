from src.core.database import db_instance
from src.schemas.alertmanager import Alert
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

    async def create_new_alert(self, alert: Alert, servicenow_ticket_number: str, servicenow_sys_id: str):
        """
        Create new alert inside MongoDB
        """
        document = {
        "alertName": alert.labels['alertname'],
        "incidentNumber": servicenow_ticket_number,
        "snowSysId": servicenow_sys_id,
        "alertStatus": alert.status,
        "alertStartDate": alert.startsAt,
        "alertEndDate": alert.endsAt,
        "fingerprint": alert.fingerprint
        }
        await self.collection.insert_one(document)

    async def update_alert(self, alert: Alert):
        """
        Update alert status in MongoDB
        """
        filter_query = {"fingerprint": alert.fingerprint}
        document_update = {
            "$set": {
                "alertStatus": alert.status,
                "alertEndDate": alert.endsAt
            }
        }
        await self.collection.update_one(filter_query,document_update)