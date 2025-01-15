import logging


# Create a logger
logger = logging.getLogger('flexible_logger')
logger.setLevel(logging.DEBUG) # Set the threshold to DEBUG 







# Create handlers for console and log file
file_handler = logging.FileHandler('flexible_output.log', mode='w')
console_handler = logging.StreamHandler()

file_handler.setLevel(logging.DEBUG) # Log all levels to the file
file_formatter = logging.Formatter('%(levelname)a - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

