import os
import sys
import time
import requests
import socket
import smtplib
# from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

paths = [
    '/srv'
]

for path in paths:
    if path not in sys.path:
        sys.path.append(path)


INTERVAL = 15

SEND_EMAIL = True
SEND_SLACK = True

EMAIL_USER = 'user@gmail.com'
EMAIL_PASS = 'p455w0rd'

FROM = EMAIL_USER
TO = 'otheruser@email.com'

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

ALERT_SUBJECT = 'Alert: GCE Maintenance Event'

GCE_PROJECT_NAME = 'project-name'

GCE_METADATA_URL = 'http://metadata.google.internal/computeMetadata/v1/'
GCE_METADATA_HEADERS = {'Metadata-Flavor': 'Google'}

GCE_OPERATIONS_URL = 'https://console.cloud.google.com/compute/operations?project={}'.format(GCE_PROJECT_NAME)

SLACK_URL = 'https://hooks.slack.com/services/xxxxxxxxx/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
SLACK_HEADERS = {'Content-type': 'application/json'}

SLACK_USERNAME = 'GCE Maintenance Alerts'


class GCEMaintenanceAlerts():
    """
    Send alerts for GCE Maintenance Events.

    - Email
    - Slack
    """

    def __init__(self):
        send_email = True
        send_slack = True

        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587

        self.slack_url = ''
        self.slack_username = ''


    def check_maintenance_event(self, callback):
        """
        Check metadata URL for GCE Maintenance Event.
        """

        request_url = GCE_METADATA_URL + 'instance/maintenance-event'
        last_maintenance_event = None
        last_etag = '0'
        hostname = socket.gethostname()

        while True:
            request = requests.get(
                request_url,
                params={
                    'last_etag': last_etag,
                    'wait_for_change': True
                },
                headers=GCE_METADATA_HEADERS
            )

            # During maintenance GCE can return a 503, so retry request
            if request.status_code == 503:
                time.sleep(1)
                continue
            request.raise_for_status()

            last_etag = request.headers['etag']

            if request.text == 'NONE':
                maintenance_event = None
            else:
                # Possible events:
                # MIGRATE_ON_HOST_MAINTENANCE = instance will be migrated
                # SHUTDOWN_ON_HOST_MAINTENANCE = instance will be shut down
                maintenance_event = request.text

            # Check for which type of maintenance will be occurring
            if maintenance_event == 'MIGRATE_ON_HOST_MAINTENANCE':
                msg['Subject'] = 'Urgent: GCE Maintenance Alert (migration): {}'.format(hostname)
                maintenance_message = 'Urgent: GCE Maintenance Alert for impending instance Migration: {}'.format(hostname)
            elif maintenance_event == 'SHUTDOWN_ON_HOST_MAINTENANCE':
                msg['Subject'] = 'Urgent: GCE Maintenance Alert (shutdown): {}'.format(hostname)
                maintenance_message = 'Urgent: GCE Maintenance Alert for impending instance Shutdown: {}'.format(hostname)
            else:
                msg['Subject'] = 'Urgent: GCE Maintenance Alert (unknown): {}'.format(hostname)
                maintenance_message = 'Urgent: GCE Maintenance Alert for impending instance Maintenance: {}'.format(hostname)

            if maintenance_event != last_maintenance_event:
                last_maintenance_event = maintenance_event
                callback(maintenance_event)


    def send_email(self, to, subject, text):
        """
        Send Email alert.
        """

        # Create message
        message = MIMEMultipart()
        message['From'] = FROM
        message['To'] = to
        message['Subject'] = subject
        message.attach(MIMEText(text))

        # Connect to mail server
        mail_server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        mail_server.ehlo()
        # Encrypt connection
        mail_server.starttls()
        mail_server.ehlo()
        # Authenticate
        mail_server.login(EMAIL_USER, EMAIL_PASS)
        # Send mail
        # mail_server.sendmail(GMAIL_USER, [to], message.as_string())
        mail_server.sendmail(EMAIL_USER, to, message.as_string())
        mail_server.close()


    def send_slack(self, subject, text, url):
        """
        Send Slack alert.
        """

        # Send Slack channel alert
        request = requests.post(
            url,
            data={
                # 'channel': '#general',
                'username': self.slack_username,
                'icon_emoji': ':rotating_light:',
                'text': '{}\n<{}|View GCE Operations Log>'.format(SUBJECT, GCE_OPERATIONS_URL)
            },
            headers=SLACK_HEADERS
        )


    def alert_maintenance_event(self, event):
        """
        Send alerts via email and Slack for GCE Maintenance Event.
        """

        if event:
            print('Undergoing host maintenance: {}'.format(event))

            if SEND_MAIL == True:
                self.send_email(TO, SUBJECT, event)

            if SEND_SLACK == True:
                self.send_slack(SUBJECT, event, SLACK_URL)
        else:
            print('Finished host maintenance')


    # def main():
    #     GMA.check_maintenance_event(self, alert_maintenance_event)
    #     time.sleep(INTERVAL)


if __name__ == 'main':

    GMA = GCEMaintenanceAlerts()

    while(True):
        # main()
        GMA.check_maintenance_event(self, alert_maintenance_event)
        time.sleep(INTERVAL)
