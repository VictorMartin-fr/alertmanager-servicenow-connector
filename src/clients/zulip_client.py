from src.schemas.core import CoreAlert

import httpx

class ZulipClient:
    def __init__(self, instance_url: str, email: str, api_key: str, channel: str):
        self.zulip_url = instance_url
        self.auth = (email, api_key)
        self.channel = channel

    async def send_notification(self, core_alert: CoreAlert, is_flapping: bool):
        """
        SEND ZULIP NOTIFICATION
        """
        url = f"{self.zulip_url}/api/v1/messages"

        labels_builder = ""

        for label in core_alert.tags:
            labels_builder += f"{label}: {core_alert.tags[label]} \n"

        flapping_message = "**Warning, this alert already been triggered this last 24 hours**\n" if is_flapping else "\n"

        emoji = ":warning:" if is_flapping else ":fire:" if core_alert.status == "firing" else ":check:"
        message = (
            f"**{emoji} {core_alert.name} {emoji}**\n"
            "\n\n"
            f"**📦 Source:** {core_alert.source}\n\n"
            f"{flapping_message}"
            "\n\n"
            f"**Description:** {core_alert.description}"
            "\n\n"
            "**Labels:**\n"
            "```\n"
            f"{labels_builder}\n"
            "```"
        )

        print(message)

        data = {
            "type": "stream",
            "to": self.channel,
            "topic": f"{core_alert.name}",
            "content": message
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                auth=self.auth,
                data=data
            )