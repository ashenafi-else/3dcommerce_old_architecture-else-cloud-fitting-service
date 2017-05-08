import json
import requests
from threading import Thread

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db import connection, transaction

from fitting.models import Scan, CompareResult, ScanAttribute, LastAttribute
from fitting_algorithm import lists_comparison
import logging

logger = logging.getLogger(__name__)


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


def compare_by_metrics(scan, last):

    last_attributes = LastAttribute.objects.filter(last=last, disabled=False)
    scan_metrics = []
    last_metrics = []

    for last_attribute in last_attributes:

        scan_attribute = ScanAttribute.objects.filter(scan=scan, name=last_attribute.scan_attribute_name).first()
        if scan_attribute is not None:
            scan_metrics.append(float(scan_attribute.value))
            last_metrics.append(float(last_attribute.value))

    limits = tuple((attr.left_limit_value, attr.best_value, attr.right_limit_value) for attr in last_attributes)

    compare_result = CompareResult(
        last=last,
        scan_1=scan,
        compare_result = lists_comparison(scan_metrics, last_metrics, limits),
        compare_type=CompareResult.TYPE_FITTING,
        compare_mode=CompareResult.MODE_METRICS,
    )
    compare_result.save()

    return compare_result
