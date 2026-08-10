# Slack documentation

## Webhook configuration

First, you will need to create a new Slack App to be able to create an incoming webhook. All the documentation is available on the [slack website](https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/#getting_started)

## Configuration

Once the webhook is created, you can configure ASC :

```yaml
slack:
  enabled: True
  webhook_url: [WEBHOOK]
```

## Environment variable

| configuration key                 | environment variable     |
|-----------------------------------|--------------------------|
| **slack.enabled**                 | `ASC_SLACK__ENABLED`     |
| **slack.webhook_url**             | `ASC_SLACK__WEBHOOK_URL` |