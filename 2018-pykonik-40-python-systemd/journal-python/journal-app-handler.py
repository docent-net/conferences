#!/usr/bin/python3
# See https://www.freedesktop.org/software/systemd/python-systemd/journal.html

import logging
import uuid
from systemd.journal import JournaldLogHandler

log = logging.getLogger('custom_logger_name')
log.propagate = False
log.setLevel(logging.DEBUG)
log.addHandler(JournaldLogHandler())

log.warning("Simple message: %s", 'simple_value')

message_uuid = uuid.uuid4()
log.warning("Message with ID", extra={'MESSAGE_ID': message_uuid})