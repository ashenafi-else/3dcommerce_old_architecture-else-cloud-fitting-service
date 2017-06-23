import json
import requests
from threading import Thread

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db import connection, transaction

from fitting.models import Scan, CompareResult, ScanAttribute, LastAttribute, Last
from fitting_algorithm import lists_comparison
import logging

logger = logging.getLogger(__name__)


def compare_by_metrics(scan, product):

    lasts = Last.objects.filter(product=product)
    metrics = {}

    for last in lasts:

        last_attributes = LastAttribute.objects.filter(last=last, disabled=False)

        for last_attribute in last_attributes:

            scan_attribute = ScanAttribute.objects.filter(scan=scan, name=last_attribute.scan_attribute_name).first()

            if last_attribute.name not in metrics:
                metrics[last_attribute.name] = {
                    'scan': scan_attribute.value,
                    'lasts': []
                }

            if scan_attribute is not None:
                if scan
                scan_metrics.append(float(scan_attribute.value))
                last_metrics.append(float(last_attribute.value))

        limits = tuple((attr.left_limit_value, attr.best_value, attr.right_limit_value) for attr in last_attributes)

    try:
        compare_result = CompareResult.objects.get(
            last=last,
            scan_1=scan,
            compare_type=CompareResult.TYPE_FITTING,
            compare_mode=CompareResult.MODE_METRICS,
        )
    except CompareResult.DoesNotExist:
        compare_result = CompareResult(
            last=last,
            scan_1=scan,
            compare_type=CompareResult.TYPE_FITTING,
            compare_mode=CompareResult.MODE_METRICS,
        )
    compare_result.compare_result = lists_comparison(scan_metrics, last_metrics, limits)
    compare_result.save()

    return compare_result


compare_functions = [compare_by_metrics, ]


class CompareScansThread(Thread):

    def __init__(self, scan):
        self.scan = scan
        super(CompareScansThread, self).__init__()

    def run(self):
        try:
            lasts = Last.objects.filter(model_type=self.scan.model_type)
            for last in lasts:
                for compare_function in compare_functions:
                    try:
                        compare_function(self.scan, last)
                        logger.debug('shoe {} and scan {} are compared'.format(last, self.scan))
                    except (ValueError, KeyError):
                        logger.debug('shoe {} and scan {} are not compared'.format(last, self.scan))
        except Scan.DoesNotExist:
            logger.log('Scan {} not compared'.format(self.scan))
        finally:
            logger.debug('connection for scan {} close'.format(self.scan))
            connection.close()
