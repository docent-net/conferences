#!/usr/bin/python3

import logging
from time import sleep
import pystemd.daemon
from cysystemd.journal import JournaldLogHandler


class App(object):
    def __init__(self):
        self.create_logger()
        self.count = 1

    def create_logger(self):
        self.log = logging.getLogger('app_logger')
        self.log.setLevel(logging.DEBUG)
        self.log.addHandler(JournaldLogHandler())

    def start(self):
        # do something specific to app startup
        sleep(2)

        # tell systemd we're ready
        pystemd.daemon.notify(False, ready=1,
                              status="starting processor service")
        self.log.info("Ready")

        while True:
            self.process_something()

        # if you'd like to stop properly
        self.stop()

    def process_something(self):
        self.log.info("Running... {}".format(self.count))
        pystemd.daemon.notify(False, ready=1,
                              status="STATUS=Count is {}".format(self.count))
        pystemd.daemon.notify(False, watchdog=1)
        # processing....
        self.count += 1
        sleep(1)

    def stop(self):
        # tell systemd we're stopping service
        self.log.info('Stopping...')
        pystemd.daemon.notify(False, 'STOPPING=1')


app = App()
app.start()
