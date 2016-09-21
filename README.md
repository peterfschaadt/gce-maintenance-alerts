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

gce\_project\_name = hello-world

interval = 15 (default, in seconds)

alert_subject = Alert: GCE Maintenance Event (default)


### Email

send_email = True

email_user = user@gmail.com

email_pass = p455w0rd

email_to = otheruser@email.com

smtp_host = smtp.google.com (default)

smtp_port = 587 (default)


### Slack

send_slack = True

slack_url = https://hooks.slack.com/services/xxxxxxxxx/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

slack_username = GCE Maintenance Alerts (default)
