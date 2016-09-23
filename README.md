# Google Compute Engine VM Maintenance Alerts


A Python service to receive email or Slack alerts when a Google Compute Engine VM is about to undergo maintenance. Requires no external dependencies, just Python.


## Alert Types

- Email (requires a GMail account for sender, but not recipients)

- Slack (requires a webhook URL)

- TODO: Ability to run an arbitrary Python or shell script


## Usage

1. Copy example-config.ini and edit it with your credentials and preferred settings.

2. Run script (must be run on a Google Compute Engine VM to work) and pass path to the ini config file as an argument.

```
$ python gce_maintenance_alerts.py -c /path/to/config.ini
```


## Settings

These settings can be specified in the ini config file, or supplied via command line arguments.


### General

__gce\_project\_name__ = hello-world

__interval__ = 15 (default, in seconds)

__alert_subject__ = Alert: GCE Maintenance Event (default)


### Email

__send_email__ = True

__email_user__ = user@gmail.com

__email_pass__ = p455w0rd

__email_to__ = otheruser@email.com

__smtp_host__ = smtp.gmail.com (default)

__smtp_port__ = 587 (default)


### Slack

__send_slack__ = True

__slack_url__ = https://hooks.slack.com/services/xxxxxxxxx/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

__slack_username__ = GCE Maintenance Alerts (default)
