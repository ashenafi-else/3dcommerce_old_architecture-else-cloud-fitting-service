import json
import requests
import csv
import logging
from fitting.models import ScanAttribute, ModelType
from web.settings import ELSE_3D_SERVICE_SCRIPTS_URL

logger = logging.getLogger(__name__)

attribute_urls_type = {
    ModelType.TYPE_LEFT_FOOT: 'left',
    ModelType.TYPE_RIGHT_FOOT: 'right',
}


def get_3d_url(url):
    get_scan_3d = requests.post(
        url=f'{ELSE_3D_SERVICE_SCRIPTS_URL}scans_to_json',
        data=json.dumps({'stl_url': url}),
        headers={
            'Content-Type': 'application/json'
        }
    )
    get_scan_3d.raise_for_status()
    return get_scan_3d.json()['result_json_url']


def get_scan_image_url(url):
    get_scan_image = requests.post(
        url=f'{ELSE_3D_SERVICE_SCRIPTS_URL}stl_to_image',
        data=json.dumps({'stl_url': url, 'resolution': ['384', '683']}),
        headers={
            'Content-Type': 'application/json'
        }
    )
    get_scan_image.raise_for_status()
    return get_scan_image.json()['result_image_url']


def update_scan_attributes(base_url, scan, scan_type):
    path_to_csv = '{}{}/{}/{}_{}_mes.csv'.format(base_url, scan.scanner, scan.scan_id, scan.scan_id, attribute_urls_type[scan_type])
    request = requests.get(path_to_csv)
    profile = list(request.iter_lines(decode_unicode=True))[1:]
    request.raise_for_status()
    for row in csv.DictReader(profile, delimiter=';'):
        for key, value in row.items():
            if key != '':
                name = key.split('(')[0].strip()
                try:
                    attribute = ScanAttribute.objects.get(name=name, scan=scan)
                except ScanAttribute.DoesNotExist:
                    attribute = ScanAttribute(name=name, scan=scan)
                attribute.value = value
                attribute.save()