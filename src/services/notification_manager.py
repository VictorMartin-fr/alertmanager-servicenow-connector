from src.schemas.core import CoreAlert
from src.schemas.alertmanager import Alert

class NotificationManager:
    def __init__(self):
        self.notifiers = []

    def register_notifier(self, client):
        self.notifiers.append(client)

    async def notify_all(self, core_alert: CoreAlert, is_flapping: bool):
        for notifier in self.notifiers:
            await notifier.send_notification(core_alert, is_flapping)

notify = NotificationManager()