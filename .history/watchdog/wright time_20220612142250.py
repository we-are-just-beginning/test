import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s', datefmt='%H:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
fileHandler = logging.FileHandler('test.log', mode='a+')
formatter = logging.Formatter('%(asctime)s', datefmt='%H:%M:%S')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

while True:
    logger.info('')
    time.sleep(1)
