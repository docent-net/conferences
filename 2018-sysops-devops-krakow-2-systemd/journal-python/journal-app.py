#!/usr/bin/python3
# See https://www.freedesktop.org/software/systemd/python-systemd/journal.html

from systemd import journal

journal.send(MESSAGE='Hello world')
journal.send(
    MESSAGE='Hello, again, world',
    PRIORITY=3,
    SYSLOG_IDENTIFIER='myapp',
    FIELD2='Greetings!'
)
