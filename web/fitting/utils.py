import json
import requests
from threading import Thread

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db import connection, transaction

from fitting.models import Scan, CompareResult
import logging

logger = logging.getLogger(__name__)


def upload(url):
    request = requests.get(
        url=url,
    )
    return request.content


class CompareShoesThread(Thread):

    def __init__(self, scan_id):
        self.scan_id = scan_id
        super(CompareShoesThread, self).__init__()

    def run(self):
        try:
            scan = Scan.objects.get(id=self.scan_id)
            shoes = Shoe.objects.all()
            for shoe in shoes:
                try:
                    compare_scan_with_shoe(shoe, scan)
                    logger.debug('shoe {} and scan {} are compared'.format(shoe.id, scan.id))
                except (ValueError, KeyError):
                    logger.debug('shoe {} and scan {} are not compared'.format(shoe.id, scan.id))
        except Scan.DoesNotExist:
            logger.log('Scan {} not compared'.format(self.scan_id))
        finally:
            logger.debug('connection for scan {} close'.format(self.scan_id))
            connection.close()


@transaction.atomic
def compare_scan_with_shoe(shoe, scan):

    if not shoe.path_in_fitting_service:
        shoe.path_in_fitting_service = upload_to_fitting(shoe.path, 'UploadTemplate')
        shoe.save()

    request_to_fitting = requests.post(
        'http://fittingwebapp.azurewebsites.net/api/fitting',
        data=json.dumps(
            {
                'ScanBlobPath': scan.path_right_foot_in_fitting_service,
                'TemplateBlobPath': shoe.path_in_fitting_service
            }
        ),
        headers={
            'Content-Type': 'application/json'
        }
    )

    fitting_result = request_to_fitting.json()
    try:
        compare_result = CompareResults.objects.get(shoe_id=shoe.id, scan_id=scan.id,)
    except CompareResults.DoesNotExist:
        compare_result = CompareResults(
            shoe_id=shoe.id,
            scan_id=scan.id,
        )
    compare_result.compare_result = float(fitting_result['Result']['ResultpPoint3D']['ResultPercent'])
    output_analysis_model_url = fitting_result['OutputAnalysisModelUrl']
    output_factory_model_url = fitting_result['OutputFactoryModelUrl']
    compare_result.output_model = get_fitting_image_url([output_analysis_model_url, output_factory_model_url])
    try:
        compare_result.save()
    except (ValidationError, IntegrityError):
        compare_result = CompareResults.objects.get(shoe_id=shoe.id, scan_id=scan.id,)
        logger.debug('Try to duplicate compare result: "{}"'.format(compare_result))

    return compare_result


def get_fitting_image_url(urls):
    get_fitting_image = requests.post(
        url='http://else-3d-service.cloudapp.net/scripts/stl_to_image',
        data=json.dumps({'stl_url': urls, 'resolution': ['384', '683']}),
        headers={
            'Content-Type': 'application/json'
        }
    )
    logger.debug(get_fitting_image.text)
    return get_fitting_image.json()['result_image_url']

