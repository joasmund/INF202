import logging


logger = logging.getLogger("file_logger")
handler = logging.FileHandler("file_log.log", mode='w')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.info(f'My info is {handler}')


logging.basicConfig(
    logFileName = 'file_log.log',
    level = logging.WARNING, # Set the threshold to WARNING
    format="%(asctime)s - %(levelname)s - %(message)s")

logging.debug("This is a degub message")
logging.info("This is an info message for genereal application events.")
logging.warning("This is a warning message")
logging.error("This is an error message")
logging.critical("This is a critical message for a severe problem")
