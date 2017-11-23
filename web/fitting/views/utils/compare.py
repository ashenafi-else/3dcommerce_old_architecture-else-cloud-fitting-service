import json
import requests
from threading import Thread

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db import connection, transaction

from fitting.models import Scan, CompareResult, CompareVisualization, ScanAttribute, LastAttribute, Last, Product
from fitting_algorithm import get_metrics_by_sizes
from fitting.utils import gen_file_name
from blender_scripts.worker import execute_blender_script
from django.conf import settings
from pathlib import Path

import sys, traceback
import logging
import os

logger = logging.getLogger(__name__)


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
    if compare_instance.last.attachment and compare_instance.scan_1.attachment:
        image_file_name = gen_file_name(compare_instance, 'FITTING.png')
        image_file_path = create_file(image_file_name)
        json_file_name = gen_file_name(compare_instance, 'FITTING.json')
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


def visualization(best_last, scan):
    lasts = [best_last,]
    previous_model = Last.objects.filter(
        product=best_last.product,
        model_type=best_last.model_type,
        size__numeric_value__lt=best_last.size.numeric_value).order_by('size__numeric_value').last()
    if previous_model is not None:
        lasts.append(previous_model)
    next_model = Last.objects.filter(
        product=best_last.product,
        model_type=best_last.model_type,
        size__numeric_value__gt=best_last.size.numeric_value).order_by('size__numeric_value').first()
    if next_model is not None:
        lasts.append(next_model)
    for model in lasts:
        visualisation_instance = CompareVisualization.objects.get_or_create(last=model, scan_1=scan)[0]
        with transaction.atomic():
            locked_instance = CompareVisualization.objects.select_for_update().get(pk=visualisation_instance.pk)
            if locked_instance is None:
                visualisation_instance = CompareVisualization.objects.create(last=model, scan_1=scan)
            if locked_instance.output_model is None or locked_instance.output_model is None:
                create_fitting_visualization(locked_instance)


def get_compare_result(scan, lasts):

    scan_data = []
    lasts_data = {}
    metrics = []

    scan_attributes = ScanAttribute.objects.filter(scan=scan)

    for scan_attribute in scan_attributes:

        need_to_add = False
        for last in lasts:
            last_attribute = LastAttribute.objects.filter(
                scan_attribute_name=scan_attribute.name,
                last=last,
                disabled=False
            ).first()

            if last_attribute is not None:
                ranges = (last_attribute.left_limit_value, last_attribute.best_value, last_attribute.right_limit_value,)

                if last_attribute.last.size.value not in lasts_data:
                    lasts_data[last_attribute.last.size.value] = ([float(last_attribute.value)], [ranges])
                else:
                    lasts_data[last_attribute.last.size.value][0].append(float(last_attribute.value))
                    lasts_data[last_attribute.last.size.value][1].append(ranges)
                need_to_add = True

        if need_to_add:
            scan_data.append(float(scan_attribute.value))
            metrics.append(scan_attribute.name)
            
    return (get_metrics_by_sizes(scan_data, [(size, metrics[0], metrics[1]) for size, metrics in lasts_data.items()]), metrics)


def get_best_size(product, left_scan, right_scan):

    best_size_result = CompareResult.MIN
    best_pair = (None, None)
    lasts = zip(
        Last.objects.filter(product=product, model_type=left_scan.model_type).order_by('size__value'),
        Last.objects.filter(product=product, model_type=right_scan.model_type).order_by('size__value')
    )
    for pair in lasts:
        compare_result_left = CompareResult.objects.filter(last=pair[0], scan_1=left_scan).first()
        if compare_result_left is None:
            compare_by_metrics(left_scan, product)
            compare_result_left = CompareResult.objects.filter(last=pair[0], scan_1=left_scan).first()
        compare_result_right = CompareResult.objects.filter(last=pair[1], scan_1=right_scan).first()
        if compare_result_right is None:
            compare_by_metrics(right_scan, product)
            compare_result_right = CompareResult.objects.filter(last=pair[1], scan_1=right_scan).first()

        average_result = (compare_result_right.compare_result + compare_result_left.compare_result) / 2
        if average_result > best_size_result:
            best_size_result = average_result
            best_pair = pair
    return best_pair


@transaction.atomic
def compare_by_metrics(scan, product):


    def save_results(scan, lasts, results):

        for result in results[0]:

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
            compare_result.output_difference = [{'name': metric, 'difference': diff} for diff, metric in zip(result[2], results[1])]

            compare_result.save()

    lasts = Last.objects.filter(product=product, model_type=scan.model_type)
    compare = get_compare_result(scan, lasts)
    save_results(scan, lasts, compare)

compare_functions = [compare_by_metrics, ]


class VisualisationThread(Thread):

    def __init__(self, left_scan, right_scan, products):
        self.left_scan = left_scan
        self.right_scan = right_scan     
        self.products = products
        super(VisualisationThread, self).__init__()

    def run(self):

        for product in self.products:
            try:

                best_pair = get_best_size(product, self.left_scan, self.right_scan)
                visualization(best_pair[0], self.left_scan)
                visualization(best_pair[1], self.right_scan)
                    
            except Exception as e:
                logger.error(e)
            finally:
                connection.close()
