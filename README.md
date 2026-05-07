# ASC - Alert management

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Async-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

ASC (for AlertManager ServiceNow Connector) is a tool to interconnect AlertManager and ServiceNow. This tool is not just a script that create tickets inside ServiceNow but a full lifecycle management API for alerts.

**Main features:**
- Incidents creation inside ServiceNow
- Noise reduction by storing alerts inside database
- Incident lifecycle (InProgress, On-Hold, Resolved)
- Alerts flapping detection

## Supported technology

| Type           | Technology                                                                                               |
|----------------|----------------------------------------------------------------------------------------------------------|
| Alert sources  | [AlertManager](./docs/alerts/setup-alertmanager.md) • [HealthCheck.io](docs/alerts/setup-healthcheck.md) |
| Ticketing tool | [ServiceNow](./docs/tickets/setup-servicenow.md)                                                         |
| Communication  | [Zulip](./docs/communication/setup-zulip.md)                                                             |

## Configuration

### Prerequisites

Before using ASC, make sure to have the following prerequisites:
- a MongoDB instance
- a service account user inside the ServiceNow instance with appropriate rights to write incidents

### General

ASC use a configuration files and/or environment variables. Create a file `config.yml` or copy and rename the file `config.template.yml`:
```yaml
#ServiceNow configuration
service_now:
  instance_id:
  username:
  password:
  caller_id:
  state:
    in_progress:
    on_hold:
    hold_reason:

#MongoDB configuration
mongodb:
  hostname:
  port:
  username:
  password:
  database:
  collection:
```
Values :

| Value                           | Description                                              | Type     | Example                             | Environment Variable                |
|---------------------------------|----------------------------------------------------------|----------|-------------------------------------|-------------------------------------|
| `service_now.instance_id`       | ID of your ServiceNow instance                           | `string` | `dev278035.service-now.com`         | ASC_SERVICE_NOW__INSTANCE_ID        |
| `service_now.username`          | Username for REST API access                             | `string` | `my-svc`                            | ASC_SERVICE_NOW__USERNAME           |
| `service_now.password`          | Password for REST API access                             | `string` | `Sup3rS3cr3t`                       | ASC_SERVICE_NOW__PASSWORD           |
| `service_now.caller_id`         | ID of user used inside `caller` incident field           | `string` | `MonitoringUser`                    | ASC_SERVICE_NOW__CALLER_ID          |
| `service_now.state.in_progress` | ID of `in progress` state on your instance. Default `2`  | `int`    | `2`                                 | ASC_SERVICE_NOW__STATE__IN_PROGRESS |
| `service_now.state.on_hold`     | ID of `hold state` on your instance. Default `3`         | `int`    | `3`                                 | ASC_SERVICE_NOW__STATE__ON_HOLD     |
| `service_now.state.hold_reason` | ID of `hold reason` status on your instance. Default `1` | `int`    | `1`                                 | ASC_SERVICE_NOW__STATE__HOLD_REASON |
| `mongodb.hostname`              | IP or FQDN of your mongoDB instance                      | `string` | `mongo.example.org`                 | ASC_MONGODB__HOSTNAME               |
| `mongodb.port`                  | Port of your mongoDB instance                            | `int`    | `27017`                             | ASC_MONGODB__PORT                   |
| `mongodb.username`              | Username for mongoDB connection                          | `string` | `svc-mongo`                         | ASC_MONGODB__USERNAME               |
| `mongodb.password`              | Password for mongoDB connection                          | `string` | `S3cureP@ssw0rd`                    | ASC_MONGODB__PASSWORD               |
| `mongodb.database`              | Name of database                                         | `string` | `alertmanager_servicenow_connector` | ASC_MONGODB__DATABASE               |
| `mongodb.collection`            | Name of the collection inside the database               | `string` | `asc`                               | ASC_MONGODB__COLLECTION             |

The image is available TODO.

### Docker

For testing purpose, we have a `docker-compose.yml` file available inside the repository. To start it, copy the file `.env.template` to `.env`, fill the value `SERVICENOW_PASSWORD` with your service account password and configure the secrets for MongoDB (`MONGODB_USERNAME` and `MONGODB_PASSWORD`)

Then, execute the following command:
```bash
podman compose up -d
```

## Usage

### AlertManager

To route alerts from your Prometheus AlertManager to ASC, simply add the following webhook receiver to your `alertmanager.yml` configuration:
```yaml
receivers:
- name: 'asc-servicenow'
  webhook_configs:
  - url: 'http://<ASC_IP>:8000/alerts'
    send_resolved: true
```

### Grafana

To route alerts from your Grafana instance to ASC, create a new contact point using the webhook method and add the following url : `http://<ASC_IP>:8000/alerts`

## Local Development

To run locally the API for Development purpose, you can execute the following commands:
```bash
pip install -r requirements.txt
fastapi dev src/main.py
```

## Roadmap

For now this tool only manage alerts from AlertManager and can only talk to ServiceNow. In the future, we want to release the following features:
- Notifications connectors (Slack, Mattermost, etc...)
- Other alerts sources (Dynatrace, DataDog, etc...)