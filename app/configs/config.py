import os
import logging
import sys


WEBHOOK_URL = os.environ['APP_WEBHOOK']

team = { 
    'KM': 'kiryl.masliukou@gmail.com'
    }


LOG_FILE = "/microservice/log/app_log"
file_handler = logging.FileHandler(filename=LOG_FILE)
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]
logging.basicConfig(
    level = logging.DEBUG,
    format = '[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S +0000',
    handlers = [file_handler, stdout_handler]
)
logger = logging.getLogger('Jira-Teams-Integration')


server = os.environ['JIRA_SERVER']
basic_auth = (os.environ['JIRA_LOGIN'], os.environ['JIRA_API_TOKEN'])
