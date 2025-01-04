import logging

logger = logging.getLogger("copcon")
logger.setLevel(logging.DEBUG)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)
