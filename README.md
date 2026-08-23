# ASC - Alert management

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Async-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

ASC (for AlertManager ServiceNow Connector) is a tool to interconnect `alerting` platform, `ITSM` and `messaging` tools. This tool is not just a script that create tickets inside ITSM but a full lifecycle management API for alerts.

**Main features:**
- Incidents creation inside ITSM tools _(ServiceNow)_
- Noise reduction by storing alerts inside database
- Incident lifecycle (InProgress, On-Hold, Resolved)
- Alerts flapping detection

## Supported technology

| Type           | Technology                                                                                               |
|----------------|----------------------------------------------------------------------------------------------------------|
| Alert sources  | [AlertManager](./docs/alerts/setup-alertmanager.md) • [HealthCheck.io](docs/alerts/setup-healthcheck.md) |
| Ticketing tool | [ServiceNow](./docs/tickets/setup-servicenow.md)                                                         |
| Communication  | [Slack](./docs/communication/setup-slack.md) • [Zulip](./docs/communication/setup-zulip.md)              |

## Configuration

### Prerequisites

Before using ASC, make sure to have the following prerequisites:
- a MongoDB instance
- `Accounts`, `API Key`, etc... needed to configure the different providers (`ITSM` or `notification` channel)

### General

ASC use a configuration files and/or environment variables. Create a file `config.yml` by copying and renaming the file `config.template.yml`.

Documentation of each component are available inside `./docs/` folder.

#### Background jobs

In order to clean the alert database if an alarm has not been triggered for some time, a background job is available, run `every hours` and remove alerts in resolved state for more than `24 hours`.

You can customize these parameters by change this configuration fields :
```yaml
general:
  scheduled_task:
    scheduler_interval:
    keep_alert_interval:
```

- `scheduler_interval`: delay between to clean up job in hours (by default, `1`)
- `keep_alert_interval`: delay before removing the alert in hours (by default, `24`)

### Docker

For testing purpose, we have a `docker-compose.yml` file available inside the repository. To start it, copy the file `.env.template` to `.env`, fill the value `SERVICENOW_PASSWORD` with your service account password and configure the secrets for MongoDB (`MONGODB_USERNAME` and `MONGODB_PASSWORD`)

Then, execute the following command:
```bash
podman compose up -d
```

## Local Development

To run locally the API for Development purpose, you can execute the following commands:
```bash
pip install -r requirements.txt
fastapi dev src/main.py
```

## Roadmap

For now this tool only manage alerts from AlertManager and can only talk to ServiceNow. In the future, we want to release the following features:
- Notifications connectors (Mattermost, Teams, etc...)
- Other alerts sources (Dynatrace, DataDog, etc...)