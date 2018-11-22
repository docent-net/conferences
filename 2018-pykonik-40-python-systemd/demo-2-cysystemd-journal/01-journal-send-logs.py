#!/usr/bin/python3

from cysystemd import journal

journal.write('Hello Pykonik')

journal.send(
    MESSAGE='Hello, structurized Pykonik',
    PRIORITY=3,
    SYSLOG_IDENTIFIER='pykonik_app',
    FIELD2='ah, you found me!'
)
