# AlertManager documentation

## Webhook configuration

To send alert from AlertManager to ASC, you need to configure the following URL `http(s)://[your IP / DNS]/alertmanager/alerts`

No other configuration is required.

## Alert routing (assignment groups)

To select where AlertManager alert are sent on ServiceNow, you need to configure the receiver on AM/Grafana:

```yaml
receivers:
- name: '[MY ASSIGNMENT GROUP]'
  webhook_configs:
  - url: 'http(s)://[your IP / DNS]/alertmanager/alerts'
    send_resolved: true
```

On Grafana, the assignment group will be linked to the `contact point` name.

## Field mapping

When AlertManager alerts are received, they will be mapped like this :

| ASC Field    | AlertManager Field         |
|--------------|----------------------------|
| fingerprint  | fingerprint                |
| name         | `label` : alertname        |
| status       | status                     |
| startedAt    | startsAt                   |
| endedAt      | endsAt                     |
| tags         | labels                     |
| description  | `annotation` : description |
| support_team | receiver                   |