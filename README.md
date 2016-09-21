# Google Compute Engine Maintenance Alerts


A Python service to receive email or Slack alerts when a Google Compute Engine VM is about to undergo maintenance. Requires no external dependencies, just Python.


## Alert Types

- Email (requires a GMail account for sender, but not recipients)

- Slack (requires a webhook URL)

- TODO: Ability to run an arbitrary Python or shell script


## Usage

1. Copy example-config.ini and edit it with your credentials and preferred settings.

2. Run script (must be run on a Google Compute Engine VM to work) and pass path to config.ini file as an argument.

```
$ python alert_gce_maintenance.py -c /path/to/config.ini
```


## Settings

These settings can be specified in the ini config file, or supplied via command line arguments.


### General

GCE\_PROJECT\_NAME = hello-world

INTERVAL = 15 (default, in seconds)

ALERT_SUBJECT = Alert: GCE Maintenance Event (default)


### Email

SEND_EMAIL = True

EMAIL_USER = user@gmail.com

EMAIL_PASS = p455w0rd

EMAIL_TO = otheruser@email.com

SMTP_HOST = smtp.google.com (default)

SMTP_PORT = 587 (default)


### Slack

SEND_SLACK = True

SLACK_URL = https://hooks.slack.com/services/xxxxxxxxx/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

SLACK_USERNAME = GCE Maintenance Alerts (default)
