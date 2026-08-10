# Zulip documentation

## Webhook configuration

First, create a new `Robot` on your Organization for `Incoming webhook` usage.

## Configuration

Once the webhook is created, you can configure ASC :

```yaml
#Zulip configuration
zulip:
  enabled: True
  instance_url: "https://"
  email: ""
  api_key: ""
  channel: ""
```

- `instance_url` : url of your Zulip instance
- `email` : email of the bot
- `api_key` : key of the bot
- `channel` : on which channel the alert are wrote

## Environment variable

| configuration key                 | environment variable      |
|-----------------------------------|---------------------------|
| **zulip.enabled**                 | `ASC_ZULIP__ENABLED`      |
| **zulip.instance_url**            | `ASC_ZULIP__INSTANCE_URL` |
| **zulip.email**                   | `ASC_ZULIP__EMAIL`        |
| **zulip.api_key**                 | `ASC_ZULIP__API_KEY`      |
| **zulip.channel**                 | `ASC_ZULIP__CHANNEL`      |