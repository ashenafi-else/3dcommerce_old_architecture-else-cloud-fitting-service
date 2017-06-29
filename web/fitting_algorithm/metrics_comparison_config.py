"""metrics comparison config generation"""
from .helpers.math_helpers import get_median
import logging

logger = logging.getLogger(__name__)


def generate_config(references, scans_by_size, lasts_by_size):

    result_config = {}

    for ref in references:
        last_values = [metrics[references[ref]] for metrics in [lasts_by_size[size] for size in lasts_by_size]]

        steps = [val[0] - val[1] for val in zip(last_values[1:], last_values)]

        max_step = max(steps)
        median_step = get_median(steps)

        # deviations calculation
        f1 = median_step
        f2 = max_step - f1

        # avg scans differences calculations
        l_metric_ranges = []
        r_metric_ranges = []
        for size in scans_by_size:
            l_metrics = []
            r_metrics = []
            for scan in scans_by_size[size]:
                l_scan_data = scans_by_size[size][scan]['LEFT']
                r_scan_data = scans_by_size[size][scan]['RIGHT']

                l_metrics.append(l_scan_data[ref])
                r_metrics.append(r_scan_data[ref])

            l_median = get_median(l_metrics)
            r_median = get_median(r_metrics)

            l_shift = lasts_by_size[size][references[ref]] - l_median
            r_shift = lasts_by_size[size][references[ref]] - r_median

            l_metric_ranges.append((l_median - min(l_metrics), l_shift, max(l_metrics) - l_median))
            r_metric_ranges.append((r_median - min(r_metrics), r_shift, max(r_metrics) - r_median))

        l_range = max(get_median([val[0] for val in l_metric_ranges]), f1) \
                  + max(get_median([val[2] for val in l_metric_ranges]), f2)
        r_range = max(get_median([val[0] for val in r_metric_ranges]), f1) \
                  + max(get_median([val[2] for val in r_metric_ranges]), f2)

        l_center = get_median([val[1] for val in l_metric_ranges])
        r_center = get_median([val[1] for val in r_metric_ranges])

        left_config = (round(l_range * 0.9, 2),
                       round(l_center, 2),
                       round(l_range * 0.1, 2))
        right_config = (round(r_range * 0.9, 2),
                        round(r_center, 2),
                        round(r_range * 0.1, 2))

        for size in lasts_by_size:
            if not size in result_config:
                result_config[size] = {}

            result_config[size][references[ref]] = {
                'scan_metric': ref,
                'value': lasts_by_size[size][references[ref]],
                'l_f1': left_config[0],
                'l_shift': left_config[1],
                'l_f2': left_config[2],
                'r_f1': right_config[0],
                'r_shift': right_config[1],
                'r_f2': right_config[2]
            }

    return result_config
