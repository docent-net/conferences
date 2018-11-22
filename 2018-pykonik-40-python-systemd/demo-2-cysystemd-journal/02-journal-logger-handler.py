#!/usr/bin/python3

import logging
import uuid
from cysystemd import journal

log = logging.getLogger('pykonik_logger')
log.propagate = False
log.setLevel(logging.DEBUG)
log.addHandler(journal.JournaldLogHandler())

log.warning(
    "Pykonik warning: %s",
    'Maciek,, you probably don\'t have too much time left!'
)

message_uuid = uuid.uuid4()
log.error("Error with ID", extra={'MESSAGE_ID': message_uuid})