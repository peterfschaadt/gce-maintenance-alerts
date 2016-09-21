import os
import sys
import argparse
import ConfigParser
import time
# import requests
import urllib3
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

# Enable this to disable all alerts
TEST = False


class GCEMaintenanceAlerts():
    """
    Send alerts for GCE Maintenance Events.

    - Email
    - Slack
    """

    def __init__(self):
        """
        Gather configuration settings.
        """

        parser = argparse.ArgumentParser(description='Send alerts for GCE Maintenance Events.')
        # parser.add_argument('config', metavar='c', type='Path to the ini config file (default: working directory)')
        parser.add_argument('-c', '--config', help='Path to the ini config file (default: working directory)', required=False)

        args = parser.parse_args()

        # Check for config file path as argument
        if args.config:
            config_file = args.config
        else:
            # Default location is config.ini in script's directory
            config_file = '{}/config.ini'.format(os.path.dirname(os.path.realpath(__file__)))

        config = ConfigParser.ConfigParser
        # Read ini file
        config.read(config_file)

        # Collect General config settings
        self.gce_project_name = config.get('General', 'gce_project_name')
        self.interval = config.get('General', 'interval')
        self.alert_subject = config.get('General', 'alert_subject')

        # Collect Email config settings
        self.send_email = config.get('Email', 'send_email')
        self.email_user = config.get('Email', 'email_user')
        self.email_pass = config.get('Email', 'email_pass')
        self.email_to = config.get('Email', 'email_to')
        self.smtp_host = config.get('Email', 'smtp_host')
        self.smtp_port = config.get('Email', 'smtp_port')

        # Collect Slack config settings
        self.send_slack = config.get('Slack', 'send_slack')
        self.slack_url = config.get('Slack', 'slack_url')
        self.slack_username = config.get('Slack', 'slack_username')

        # Other config settings
        self.gce_metadata_url = 'http://metadata.google.internal/computeMetadata/v1/'
        self.gce_metadata_headers = {'Metadata-Flavor': 'Google'}
        self.gce_operations_url = 'https://console.cloud.google.com/compute/operations?project={}'.format(self.gce_project_name)
        self.alert_message = ''
        self.slack_headers = {'Content-type': 'application/json'}


    def check_maintenance_event(self, callback):
        """
        Check metadata URL for GCE Maintenance Event.
        """

        request_url = self.gce_metadata_url + 'instance/maintenance-event'
        last_maintenance_event = None
        last_etag = '0'
        hostname = socket.gethostname()

        while True:
            # request = requests.get(
            #     request_url,
            #     params={
            #         'last_etag': last_etag,
            #         'wait_for_change': True
            #     },
            #     headers=self.gce_metadata_headers
            # )

            http = urllib3.PoolManager(num_pools=1)
            request = http.request(
                'GET',
                request_url,
                fields={
                    'last_etag': last_etag,
                    'wait_for_change': True
                },
                headers=self.gce_metadata_headers
            )

            # During maintenance GCE can return a 503, so retry request
            # if request.status_code == 503:
            if request.status == 503:
                time.sleep(1)
                continue
            # request.raise_for_status()
            # except urllib3.HTTPError as e:
            #     print 'HTTPError %r' % e

            last_etag = request.headers['ETag']

            # if request.text == 'NONE':
            if request.data == 'NONE':
                maintenance_event = None
            else:
                # Possible events:
                # MIGRATE_ON_HOST_MAINTENANCE = instance will be migrated
                # SHUTDOWN_ON_HOST_MAINTENANCE = instance will be shut down
                # maintenance_event = request.text
                maintenance_event = request.data

            # Check for which type of maintenance will be occurring
            if maintenance_event == 'MIGRATE_ON_HOST_MAINTENANCE':
                # msg['Subject'] = 'Urgent: GCE Maintenance Alert (migration): {}'.format(hostname)
                self.alert_subject = 'Urgent: GCE Maintenance Alert (migration): {}'.format(hostname)
                self.alert_message = 'Urgent: GCE Maintenance Alert for impending instance Migration: {}'.format(hostname)
            elif maintenance_event == 'SHUTDOWN_ON_HOST_MAINTENANCE':
                # msg['Subject'] = 'Urgent: GCE Maintenance Alert (shutdown): {}'.format(hostname)
                self.alert_subject = 'Urgent: GCE Maintenance Alert (shutdown): {}'.format(hostname)
                self.alert_message = 'Urgent: GCE Maintenance Alert for impending instance Shutdown: {}'.format(hostname)
            else:
                # msg['Subject'] = 'Urgent: GCE Maintenance Alert (unknown): {}'.format(hostname)
                self.alert_subject = 'Urgent: GCE Maintenance Alert (unknown): {}'.format(hostname)
                self.alert_message = 'Urgent: GCE Maintenance Alert for impending instance Maintenance: {}'.format(hostname)

            if maintenance_event != last_maintenance_event:
                last_maintenance_event = maintenance_event
                # callback(maintenance_event)
                self.alert_maintenance_event(maintenance_event)


    def send_email(self, to, subject, text):
        """
        Send Email alert.
        """

        # Create message
        message = MIMEMultipart()
        message['From'] = self.email_user
        message['To'] = to
        message['Subject'] = subject
        message.attach(MIMEText(text))

        # Connect to mail server
        mail_server = smtplib.SMTP(self.smtp_host, self.smtp_port)
        mail_server.ehlo()
        # Encrypt connection
        mail_server.starttls()
        mail_server.ehlo()
        # Authenticate
        mail_server.login(self.email_user, self.email_pass)
        # Send mail
        # mail_server.sendmail(self.email_user, [to], message.as_string())
        mail_server.sendmail(self.email_user, to, message.as_string())
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
                'text': '{}\n<{}|View GCE Operations Log>'.format(subject, url)
            },
            headers=self.slack_headers
        )


    def alert_maintenance_event(self, event):
        """
        Send alerts via email and Slack for GCE Maintenance Event.
        """

        if event:
            print('Undergoing host maintenance: {}'.format(event))

            if TEST != True:
                if self.send_mail == True:
                    # self.send_email(self.email_to, self.alert_subject, event)
                    self.send_email(self.email_to, self.alert_subject, self.alert_message)

                if self.send_slack == True:
                    # self.send_slack(self.alert_subject, event, self.slack_url)
                    self.send_slack(self.alert_subject, self.alert_message, self.slack_url)
        else:
            print('Finished host maintenance')


    # def main():
    #     GMA.check_maintenance_event(self, alert_maintenance_event)
    #     time.sleep(self.interval)


if __name__ == 'main':

    GMA = GCEMaintenanceAlerts()

    while(True):
        # main()
        # GMA.check_maintenance_event(self, self.alert_maintenance_event)
        GMA.check_maintenance_event(self, alert_maintenance_event)
        time.sleep(self.interval)
