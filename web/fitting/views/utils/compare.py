import json
import requests
from threading import Thread

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db import connection, transaction

from fitting.models import Scan, CompareResult, ScanAttribute, LastAttribute, Last
from fitting_algorithm import get_metrics_by_sizes
import logging

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


def compare_by_metrics(scans, product):

    def save_results(scan, lasts, results):

        for result in results:

            last = lasts.filter(size__value=result[0]).first()

            try:
                compare_result = CompareResult.objects.get(
                    scan_1=scan,
                    last=last,
                    compare_type=CompareResult.TYPE_FITTING,
                    compare_mode=CompareResult.MODE_METRICS
                )
            except CompareResult.DoesNotExist:
                compare_result = CompareResult(
                    scan_1=scan,
                    last=last,
                    compare_type=CompareResult.TYPE_FITTING,
                    compare_mode=CompareResult.MODE_METRICS
                )
            compare_result.compare_result = result[1]
            compare_result.save()

    left_lasts = Last.objects.filter(product=product, model_type=scans[0].model_type)
    right_lasts = Last.objects.filter(product=product, model_type=scans[1].model_type)

    compare_for_left = get_compare_result(scans[0], left_lasts)
    save_results(scans[0], left_lasts, compare_for_left)
    compare_for_right = get_compare_result(scans[1], right_lasts)
    save_results(scans[1], right_lasts, compare_for_right)


compare_functions = [compare_by_metrics, ]


class CompareScansThread(Thread):

    def __init__(self, scan):
        self.scan = scan
        super(CompareScansThread, self).__init__()

    def run(self):
        try:
            products = Product.objects.all()
            for product in products:
                for compare_function in compare_functions:
                    try:
                        compare_function(self.scan, product)
                        logger.debug('shoe {} and scan {} are compared'.format(last, self.scan))
                    except (ValueError, KeyError):
                        logger.debug('shoe {} and scan {} are not compared'.format(last, self.scan))
        except Scan.DoesNotExist:
            logger.log('Scan {} not compared'.format(self.scan))
        finally:
            logger.debug('connection for scan {} close'.format(self.scan))
            connection.close()
