from src.schemas.core import CoreAlert

import httpx

class SlackClient:
    def __init__(self, webhook_url: str):
        self.webhook = webhook_url

    async def send_notification(self, core_alert: CoreAlert, is_flapping: bool):
        """
        SEND SLACK NOTIFICATION
        """

        labels_builder = ""

        for label in core_alert.tags:
            labels_builder += f"{label}: {core_alert.tags[label]} \n"

        flapping_message = "\n\n*Warning, this alert already been triggered this last 24 hours*" if is_flapping else ""

        emoji = ":warning:" if is_flapping else ":fire:" if core_alert.status == "firing" else ":white_check_mark:"
        message = (
            f"*{emoji} {core_alert.name} {emoji}*"
            "\n\n"
            f"*📦 Source:* {core_alert.source}"
            f"{flapping_message}"
            "\n\n"
            f"*Description:* {core_alert.description}"
            "\n\n"
            "*Labels:*\n"
            "```\n"
            f"{labels_builder}"
            "```"
        )

        print(message)

        data = {
            "type": "mrkdwn",
            "text": f"{message}"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.webhook,
                json=data
            )