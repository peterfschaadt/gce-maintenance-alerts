# Google Compute Engine Maintenance Alerts


A Python service to receive email, Slack alerts, or run a script when a Google Compute Engine VM is about to undergo maintenance.

## Alert Types

- Email (requires a GMail account for sender, but not recipients)

- Slack (requires a webhook URL)


## Settings

These settings can be hardcoded in the file, or supplied via arguments.


### General

GCE\_PROJECT\_NAME = 'hello-world'

INTERVAL = 15 (default, in seconds)

ALERT_SUBJECT = 'Alert: GCE Maintenance Event' (default)


### Email

SEND_EMAIL = True

EMAIL_USER = 'user@gmail.com'

EMAIL_PASS = 'p455w0rd'

EMAIL_TO = 'otheruser@email.com'

SMTP_HOST = 'smtp.google.com' (default)

SMTP_PORT = 587 (default)


### Slack

SEND_SLACK = True

SLACK_URL = 'https://hooks.slack.com/services/xxxxxxxxx/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

SLACK_USERNAME = 'GCE Maintenance Alerts' (default)
