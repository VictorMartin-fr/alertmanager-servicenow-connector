# Healthcheck documentation

## Webhook configuration

On Healthcheck, create a webhook notifier. For both `down` and `up` status, select `POST` and add the ASC url : `http(s)://[your IP / DNS]/healthcheck/ping/[tenant_name]`

`tenant_name` is a custom value you need to set to specify which tenant on Healthcheck is sending the alert.

Insert the following body for both `down` and `up` status :

```json
{
    "alert": $JSON
}
```

For the tags, you can configure tags like this :
- key:value => example: `instance:myjobserver.local`
- value => example: `critical`. Will become : `critical:true`

## Alert routing (assignment groups)

To select where the Healthcheck alert need to be sent on ServiceNow, you need to configure the following tag:

```text
support_team:[MY ASSIGNMENT GROUP]
```

## Field mapping

When Healthcheck pings are received, they will be mapped like this :

| ASC Field    | Healthcheck Field                                                   |
|--------------|---------------------------------------------------------------------|
| fingerprint  | uuid                                                                |
| name         | `Healthcheck / Check: {payload.alert.name} / Tenant: {tenant_name}` |
| status       | status                                                              |
| startedAt    | `last_ping` (if status is down)                                     |
| endedAt      | `last_ping` (if status is up)                                       |
| tags         | tags                                                                |
| description  | desc                                                                |
| support_team | tag: `support_team`                                                 |
