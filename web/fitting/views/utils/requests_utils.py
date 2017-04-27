import json
import requests

import logging

logger = logging.getLogger(__name__)


def upload(url):
    request = requests.get(
        url=url,
    )
    request.raise_for_status()
    return request.content


def get_fitting_image_url(urls):
    get_fitting_image = requests.post(
        url=f'{ELSE_3D_SERVICE_SCRIPTS_URL}/stl_to_image',
        data=json.dumps({'stl_url': urls, 'resolution': ['384', '683']}),
        headers={
            'Content-Type': 'application/json'
        }
    )
    logger.debug(get_fitting_image.text)
    return get_fitting_image.json()['result_image_url']