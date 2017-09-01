import json
import requests
from threading import Thread

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db import connection, transaction

from fitting.models import Scan, CompareResult, ScanAttribute, LastAttribute, Last, Product
from fitting_algorithm import get_metrics_by_sizes
from fitting.utils import gen_file_name
from blender_scripts.worker import execute_blender_script
from django.conf import settings
from pathlib import Path

import sys, traceback
import logging
import os

logger = logging.getLogger(__name__)


def get_compare_result(scan, lasts):

    scan_data = []
    lasts_data = {}

    scan_attributes = ScanAttribute.objects.filter(scan=scan)

    for scan_attribute in scan_attributes:

        lasts_attributes = LastAttribute.objects.filter(
            scan_attribute_name=scan_attribute.name,
            last__model_type=scan.model_type,
            disabled=False
        )

        if lasts_attributes.exists():
            scan_data.append(float(scan_attribute.value))
        for lasts_attribute in lasts_attributes:

            ranges = (lasts_attribute.left_limit_value, lasts_attribute.best_value, lasts_attribute.right_limit_value,)

            if lasts_attribute.last.size.value not in lasts_data:
                lasts_data[lasts_attribute.last.size.value] = ([float(lasts_attribute.value)], [ranges])
            else:
                lasts_data[lasts_attribute.last.size.value][0].append(float(lasts_attribute.value))
                lasts_data[lasts_attribute.last.size.value][1].append(ranges)
    return get_metrics_by_sizes(scan_data, [(size, metrics[0], metrics[1]) for size, metrics in lasts_data.items()])


@transaction.atomic
def compare_by_metrics(scan, product):

    def create_file(file_name):
        file_path = os.path.join(
            os.sep,
            settings.MEDIA_ROOT,
            file_name
        )
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        Path(file_path).touch()
        return file_path


    def create_fitting_visualization(compare_instance):
        logger.debug(compare_instance.last.attachment.path)
        image_file_name = gen_file_name(compare_instance, f'{compare_instance.compare_type}.png')
        image_file_path = create_file(image_file_name)
        json_file_name = gen_file_name(compare_instance, f'{compare_instance.compare_type}.json')
        json_file_path = create_file(json_file_name)
        execute_blender_script(
            script='new_fitting_visualisation.py',
            in_file='/www/transparent_environment.blend',
            out_file=image_file_path,
            params=[compare_instance.last.attachment.path, compare_instance.scan_1.attachment.path],
        )

        compare_instance.output_model = '/'.join([settings.PROXY_HOST] + image_file_path.split('/')[2:])
        compare_instance.output_model_3d = '/'.join([settings.PROXY_HOST] + json_file_path.split('/')[2:])
        compare_instance.save()


    def save_results(scan, lasts, results):

        best_result = CompareResult(
            compare_result=0
        )
        for result in results:

            last = lasts.filter(size__value=result[0]).first()

            compare_result = CompareResult.objects.filter(
                scan_1=scan,
                last=last,
                compare_type=CompareResult.TYPE_FITTING,
                compare_mode=CompareResult.MODE_METRICS
            ).first()

            if compare_result is None:
                compare_result = CompareResult(
                    scan_1=scan,
                    last=last,
                    compare_type=CompareResult.TYPE_FITTING,
                    compare_mode=CompareResult.MODE_METRICS
                )
            compare_result.compare_result = result[1]
            compare_result.save()
            if compare_result.compare_result > best_result.compare_result:
                best_result = compare_result
        if best_result.last.attachment and best_result.scan_1.attachment:
            create_fitting_visualization(best_result)

    lasts = Last.objects.filter(product=product, model_type=scan.model_type)
    compare = get_compare_result(scan, lasts)
    save_results(scan, lasts, compare)

compare_functions = [compare_by_metrics, ]


class CompareScansThread(Thread):

    def __init__(self, scan, products):
        self.scan = scan     
        self.products = products
        super(CompareScansThread, self).__init__()

    def run(self):
        try:
            for product in self.products:
                for compare_function in compare_functions:
                    try:
                        compare_function(self.scan, product)
                        logger.debug('shoe {} and scan {} are compared'.format(product, self.scan))
                    except Exception as e:
                        traceback.print_exc(file=sys.stdout)
                        logger.debug('shoe {} and scan {} are not compared'.format(product, self.scan))
        except Scan.DoesNotExist:
            logger.log('Scan {} not compared'.format(self.scan))
        finally:
            logger.debug('connection for scan {} close'.format(self.scan))
            connection.close()
