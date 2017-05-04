from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from pathlib import Path
from fitting.models import Last, LastAttribute
from web.settings import str2bool, MEDIA_ROOT
import requests
import logging
import json
import csv
import os

logger = logging.getLogger(__name__)

references = {
    'Foot Length': ('Effective Length', (5.2, 6.24, 5.5), (7.3, 6.55, 4.6)),
    'Instep Girth': ('Instep Girth', (10.6, 20.18, 12.2), (9.3, 16.54, 15.5)),
    'Ball Girth': ('Joint Girth', (5.9, 13.87, 6.9), (3.6, 11.40, 6.3)),
    'Ball Width': ('Stick Width', (2.2, -0.28, 2.2), (3.0, -0.67, 3.8)),
    'Instep to heel Girth': ('CLGP 65mm Offset', (11.7, -4.45, 12.3), (9.2, -1.50, 6.8)),
    'Toes Height': ('Toes Height', (0.6, 0.93, 0.7), (0.9, 2.55, 0.7)),
    'Medial Ball Height': ('Ball Height', (1.5, 6.36, 2.0), (3.0, 0.82, 2.1)),
    'Instep Height': ('Instep Height', (4.2, -12.07, 6.6), (2.5, -13.96, 3.9)),
    'Instep Width': ('Instep Width',  (1.9, 2.08, 1.5), (3.6, 2.11, 4.6)),
}


@csrf_exempt
def update_lasts_view(request):

    # request_body = json.loads(request.body.decode("utf-8"))

    request_body = {
        'products': [
            {
                'uuid': 'dasfsdf',
                'url': 'https://publicdamelse.blob.core.windows.net/public/6a37e8f2-64fd-4390-873e-0bafc947028c/lol_ZY9CdgL.csv',
                'last_type': 'foot'
            }
        ]
    }
    result = []

    for product in request_body['products']:

        try:
            update_last(product['uuid'], product['url'])
            result.append({
                'uuid': product['uuid'],
                'success': True,
            })
        except Exception as e:
            logger.debug(e)
            result.append({
                'uuid': product['uuid'],
                'success': False,
            })
            

    return HttpResponse(
        json.dumps(result)
    )


def upload_csv(product, url):

    request = requests.get(url)
    request.raise_for_status()

    csv_file_name = f'{product}.csv'
    csv_file_path = os.path.join(
        os.sep,
        MEDIA_ROOT,
        'last_attributes',
        csv_file_name
    )
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    Path(csv_file_path).touch()
    Path(csv_file_path).write_bytes(request.content)

    return csv_file_path


@transaction.atomic
def update_last(product, url):

    csv_file_path = upload_csv(product, url)

    with open(csv_file_path) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')

        for row in reader:

            last_attribute_name = row.pop('Last').strip()
            scan_attribute_name = row.pop('Scan').strip()

            for size in row:
                
                last = Last.objects.get(product__uuid=product, size__value=size)
                attribute = LastAttribute(
                    last=last,
                    name=last_attribute_name,
                    value=row[size],
                    scan_attribute_name=scan_attribute_name,
                )
                if scan_attribute_name in references:
                    attribute.left_limit_value=references[scan_attribute_name][2][0]
                    attribute.best_value=references[scan_attribute_name][2][1]
                    attribute.right_limit_value=references[scan_attribute_name][2][2]

                attribute.disabled = True if scan_attribute_name == '' else False
                attribute.save()


                

    if os.path.isfile(csv_file_path):
        os.remove(csv_file_path)
