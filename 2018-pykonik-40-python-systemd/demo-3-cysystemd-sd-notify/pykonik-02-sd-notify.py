#!/usr/bin/python3

import logging
from time import sleep
from cysystemd.daemon import notify, Notification
from cysystemd.journal import JournaldLogHandler

class App(object):
    def __init__(self):
        self.create_logger()

    def create_logger(self):
        self.log = logging.getLogger('app_logger')
        self.log.setLevel(logging.DEBUG)
        self.log.addHandler(JournaldLogHandler())

    def start(self):
        # do something specific to app startup
        sleep(2)

        # tell systemd we're ready
        notify(Notification.READY)
        self.log.info("Ready")

        count = 1
        while True:
            self.log.info("Running... {}".format(count))
            notify(Notification.STATUS, "STATUS=Count is {}".format(count))
            notify(Notification.WATCHDOG)
            count += 1
            sleep(2)
            if count == 10:
                break

        # wait 15s until watchdog kicks in (after 12s of inactivity - set in
        # unit file) and restart this service
        sleep(15)

        # if you'd like to stop properly
        self.stop()

    def stop(self):
        # tell systemd we're stopping service
        self.log.info('Stopping...')
        notify(Notification.STOPPING)


app = App()
app.start()
