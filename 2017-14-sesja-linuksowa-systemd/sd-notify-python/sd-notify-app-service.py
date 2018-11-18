#!/usr/bin/python3
# https://github.com/bb4242/sdnotify

from time import sleep
import sdnotify
import logging
from systemd.journal import JournaldLogHandler


class App(object):
    def __init__(self):
        self.create_logger()
        self.sdn = sdnotify.SystemdNotifier()

    def create_logger(self):
        self.log = logging.getLogger('app_logger')
        self.log.propagate = False
        self.log.setLevel(logging.DEBUG)
        self.log.addHandler(JournaldLogHandler())

    def start(self):
        # do something specific to app startup
        sleep(2)

        # tell systemd we're ready
        self.sdn.notify("READY=1")
        self.log.info("Ready")

        count = 1
        while True:
            self.log.info("Running... {}".format(count))
            self.sdn.notify("STATUS=Count is {}".format(count))
            count += 1
            sleep(2)
            if count == 10:
                break

app = App()
app.start()
