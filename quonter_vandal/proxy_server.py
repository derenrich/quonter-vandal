import sys
import subprocess
from flask import Flask, request, Response
import requests

PYTHON_BINARY = sys.executable

# start the uvicorn server
p = subprocess.Popen([PYTHON_BINARY, "-m", "uvicorn", "--port", "8001", "--host", "127.0.0.1", "quonter_vandal.server:app"],
                     stdout=sys.stdout, stderr=sys.stderr)


app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path>')
def redirect_to_API_HOST(path):
    res = requests.request(
        method=request.method,
        url=request.url.replace(request.host_url, f'http://127.0.0.1:8001/'),
        # exclude 'host' header
        headers={k: v for k, v in request.headers if k.lower() != 'host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
    )

    excluded_headers = ['content-encoding',
                        'content-length', 'transfer-encoding', 'connection']
    headers = [
        (k, v) for k, v in res.raw.headers.items()
        if k.lower() not in excluded_headers
    ]

    response = Response(res.content, res.status_code, headers)
    return response
