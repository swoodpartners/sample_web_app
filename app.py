import logging
import json
import os
import requests

from sys import exc_info
from flask import Flask, render_template, request

# Setup logging mechanism
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


# Setup up a Flask instance
app = Flask(__name__)

# Obtain time from public api
def query_time():
    try:
        response = requests.get(
            url="http://worldtimeapi.org/api/timezone/america/new_york",
            timeout=5
        )

        if response.status_code == 200:
            time = (json.loads(response.text))['datetime']
            logger.info('Successfully queried public API')
            return time
        elif response.status_code != 200:
            logger.error(
                f"Error querying API.  Status code: {response.status_code}")
            return "Unavailable"
            
    except Exception:
        logger.error('Failed to contact public api', exc_info=True)
        return "Unavailable"


def get_ip(web_request):
    if 'X-Forwarded-For' in web_request.headers:
        xforwardfor = web_request.headers['X-Forwarded-For']
        return web_request.remote_addr + f" and X-Forwarded-For header value of {xforwardfor}"
    else:
        return web_request.remote_addr

# Render the template
@app.route("/")
def index():
    ipinfo = get_ip(web_request=request)
    candidateName = os.getenv('CANDIDATE_NAME')
    todaystime = query_time()
    return render_template('index.html', name=candidateName, time=todaystime, ip=ipinfo)
