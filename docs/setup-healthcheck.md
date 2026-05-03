#How to setup Healthcheck webhook body

On Healthcheck, create a webhook notifier. For both `down` and `up` status, select `POST`

Insert the following body for both `down` and `up` status :

```json
{
    "alert": {
        "name": "test-ping",
        "slug": "",
        "tags": "",
        "desc": "This playbook is used to backup PostgreSQL",
        "grace": 120,
        "n_pings": 6,
        "status": "up",
        "started": false,
        "last_ping": "2026-05-03T20:07:19+00:00",
        "next_ping": "2026-05-03T20:08:19+00:00",
        "manual_resume": false,
        "methods": "",
        "subject": "",
        "subject_fail": "",
        "start_kw": "",
        "success_kw": "",
        "failure_kw": "",
        "filter_subject": false,
        "filter_body": false,
        "filter_http_body": false,
        "filter_default_fail": false,
        "badge_url": "https://healthchecks.io/b/2/.svg",
        "uuid": "",
        "ping_url": "https://hc-ping.com/6",
        "update_url": "https://healthchecks.io/api/v3/checks/",
        "pause_url": "https://healthchecks.io/api/v3/checks/pause",
        "resume_url": "https://healthchecks.io/api/v3/checks//resume",
        "channels": "",
        "timeout": 60
    }
}
```

For the tags, you can configure tags like this :
- key:value => example: `instance:myjobserver.local`
- value => example: `critical`. Will become : `critical:true`