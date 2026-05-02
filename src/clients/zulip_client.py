from schemas.alertmanager import Alert
import httpx

class ZulipClient:
    def __init__(self, instance_url: str, email: str, api_key: str, channel: str):
        self.zulip_url = instance_url
        self.auth = (email, api_key)
        self.channel = channel

    async def send_notification(self, alert: Alert, is_flapping: bool):
        """
        SEND ZULIP NOTIFICATION
        """
        url = f"{self.zulip_url}/api/v1/messages"

        labels_builder = ""

        for label in alert.labels:
            labels_builder += f"{label}: {alert.labels[label]} <br>"

        emoji = "🔄" if is_flapping else "🔥" if alert.status == "firing" else "✅"
        message = (
            f"**{emoji} {alert.labels['alertname']} {emoji}**\n"
            f"Warning, this alert already been triggered this last 24 hours\n" if is_flapping else f"\n"
            f"**Description:** {alert.annotations['description']}"
            f"\n"
            f"**Labels:** {labels_builder}"
        )

        data = {
            "type": "stream",
            "to": self.channel,
            "topic": f"{alert.labels['alertname']}",
            "content": message
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                auth=self.auth,
                data=data
            )