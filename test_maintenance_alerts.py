import web
import random

# Test Endpoint: http://metadata.google.internal/computeMetadata/v1/
# Runs on 0.0.0.0:8080 by default
# Set 0.0.0.0:8080 to metadata.google.internal in /etc/hosts

urls = (
    '/computeMetadata/v1/', 'maintenance_window'
)

app = web.application(urls, globals())


class maintenance_window:

    def GET(self):
        rand = random.randint(1, 10)
        if rand == 1:
            return 'MIGRATE_ON_HOST_MAINTENANCE'
        elif rand == 2:
            return 'SHUTDOWN_ON_HOST_MAINTENANCE'
        else:
            return 'NONE'

if __name__ == '__main__':
    app.run()
