import json
import requests
import csv
import logging
from fitting.models import Attribute

logger = logging.getLogger(__name__)


def get_3d_url(url):
    get_scan_3d = requests.post(
        url='http://else-3d-service.cloudapp.net/scripts/scans_to_json',
        data=json.dumps({'stl_url': url}),
        headers={
            'Content-Type': 'application/json'
        }
    )
    get_scan_3d.raise_for_status()
    return get_scan_3d.json()['result_json_url']


def get_scan_image_url(url):
    logger.debug(url);
    get_scan_image = requests.post(
        url='http://else-3d-service.cloudapp.net/scripts/stl_to_image',
        data=json.dumps({'stl_url': url, 'resolution': ['384', '683']}),
        headers={
            'Content-Type': 'application/json'
        }
    )
    get_scan_image.raise_for_status()
    return get_scan_image.json()['result_image_url']


def update_scan_attributes(user, base_url, scan, scan_type):
    path_to_csv = '{}{}/{}/{}_{}_mes.csv'.format(base_url, scan.scanner, scan.scan_id, scan.scan_id, scan_type.split('_').pop())
    request = requests.get(path_to_csv)
    profile = list(request.iter_lines(decode_unicode=True))[1:]
    request.raise_for_status()
    for row in csv.DictReader(profile, delimiter=';'):
        for key, value in row.items():
            if key != '':
                try:
                    attribute = Attribute.objects.get(user=user, name=key, scan=scan)
                except Attribute.DoesNotExist:
                    attribute = Attribute(user=user, name=key, scan=scan)
                attribute.value = value
                attribute.save()