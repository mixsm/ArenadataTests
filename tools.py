"""
Module for used functions
"""
import json
from pathlib import Path

import requests

import config


def send_request(verb, url, payload=None, params=None, files=None, headers=None):
    """
    Function for sending requests
    """
    if headers is None:
        headers = {'content-type': 'application/json'}
    if headers.get('content-type') == 'application/json':
        data = json.dumps(payload).encode()
    else:
        data = payload
    response = requests.request(
        method=verb,
        url=url,
        data=data,
        params=params,
        files=files,
        headers=headers,
        verify=False
    )
    print('Payload:', payload)
    print('Response URL:', response.url)
    print('Response status code:', response.status_code)
    print('Response text:', response.text)
    if response.text != '':
        response.json_data = json.loads(response.text)
    return response


def delete_templates():
    """
    Deleting all autotest files on the server
    """
    p = Path(config.template_files_path)
    for f in list(p.glob('**/autotest*.*')) + list(p.glob('current/template.*')):
        f.unlink()
