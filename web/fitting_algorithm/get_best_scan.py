import math
import logging

logger = logging.getLogger(__name__)


def get_best_scan(scans):

    def get_median(list):

        if len(list) > 0:
            sorted_list = sorted(list)

            count = len(sorted_list)
            if count % 2 == 0:
                center = count // 2
                return (sorted_list[center] + sorted_list[center - 1]) / 2
            else:
                center = count // 2
                return sorted_list[center]

    paired_scans_ids = [scan for scan in scans if 'LEFT' in scans[scan] and 'RIGHT' in scans[scan]]

    metrics = {}

    for scan in paired_scans_ids:
        for metric in list(scans[scan]['LEFT'].keys()) + list(scans[scan]['RIGHT'].keys()):
            metrics[metric] = (metrics[metric] + 1) if metric in metrics else 1

    metrics_to_remove = [metr for metr in metrics if metrics[metr] < (len(paired_scans_ids) * 2)]
    for metr in metrics_to_remove:
        if metr in metrics:
            del metrics[metr]

    best_scan_id = ''
    best_scan_distance = float("inf")

    if len(metrics) > 0:
        for scan in paired_scans_ids:
            scan_left_distance = 0
            scan_right_distance = 0

            for metr in metrics:
                left_metrics = []
                right_metrics = []

                for sc in [sc for sc in paired_scans_ids if sc != scan]:
                    left_metrics.append(scans[sc]['LEFT'][metr])
                    right_metrics.append(scans[sc]['RIGHT'][metr])

                if len(left_metrics) * len(right_metrics) > 0:
                    scan_left_distance += math.fabs(scans[scan]['LEFT'][metr] - get_median(left_metrics)) ** 2
                    scan_right_distance += math.fabs(scans[scan]['RIGHT'][metr] - get_median(right_metrics)) ** 2

            scan_zero_distance = math.sqrt(scan_left_distance + scan_right_distance) # sqr( (sqr(left) - 0) ** 2 + (sqr(right) - 0) ** 2)

            if best_scan_distance > scan_zero_distance:
                best_scan_id = scan
                best_scan_distance = scan_zero_distance

    return best_scan_id, best_scan_distance, len(paired_scans_ids), len(metrics)
