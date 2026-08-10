# ServiceNow documentation

## Prerequisites

Make sure to have a service account who can use the `REST Api` using `BasicAuth` authentication.

## Assignment group mapping

When an alert is created as an incident in `ServiceNow`, the ASC field `support_team` will be used to fill the Assignment Group.
Example:

| Alert Source     | `support_team` field                       |
|------------------|--------------------------------------------|
| **AlertManager** | `receiver` (or `Contact Point` on Grafana) |
| **Healthcheck**  | tag `support_team`                         |

## Setup

To set up ServiceNow, fill the section `servicenow` on the `config.yaml` file

```yaml
#ServiceNow configuration
service_now:
  enabled: True
  module: "incident"
  instance_id: "xxxx.service-now.com"
  username: ""
  caller_id: ""
  state:
    in_progress: 2
    on_hold: 3
    hold_reason: 1
```

> For now, the only module supported in ServiceNow is `incident` (in the future, we could implement `event` module support)

- `instance_id` : is the base URL of your ServiceNow instance. example: `dev313850.service-now.com`
- `username` : is your service account username
- `caller_id` : by default, it's the same id of your service account
- `state.in_progress` : is the ID of the `InProgress` state (by default `2` if no customization had made on your instance)
- `state.on_hold` : is the ID of the `OnHold` state (by default `3`)
- `state.hold_reason` : is the ID of the `HoldReason` (by default `1`)

> To configure the password, we recommend to use the environment variable `ASC_SERVICE_NOW__PASSWORD`

## Environment variable

| configuration key                 | environment variable                  |
|-----------------------------------|---------------------------------------|
| **service_now.enabled**           | `ASC_SERVICE_NOW__ENABLED`            |
| **service_now.module**            | `ASC_SERVICE_NOW__MODULE`             |
| **service_now.instance_id**       | `ASC_SERVICE_NOW__INSTANCE_ID`        |
| **service_now.username**          | `ASC_SERVICE_NOW__USERNAME`           |
| **service_now.password**          | `ASC_SERVICE_NOW__PASSWORD`           |
| **service_now.caller_id**         | `ASC_SERVICE_NOW__CALLER_ID`          |
| **service_now.state.in_progress** | `ASC_SERVICE_NOW__STATE__IN_PROGRESS` |
| **service_now.state.on_hold**     | `ASC_SERVICE_NOW__STATE__ON_HOLD`     |
| **service_now.state.hold_reason** | `ASC_SERVICE_NOW__STATE__HOLD_REASON` |

