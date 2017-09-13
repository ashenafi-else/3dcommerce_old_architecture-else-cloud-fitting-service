import math

""" difference calculations TYPE5"""

name = "TEST5"


def get_distances_by_sizes(scan_data, lasts_data):

    lasts_distances = []  # list of (size, real_distance, out_of_range_distance, deviations_by_axis)

    for last in lasts_data:
        real_distance = math.sqrt(
            sum(math.fabs(val[0] + val[2][1] - val[1])**2 for val in zip(scan_data, last[1], last[2]))
        )

        deviation_test = lambda x, y, f1, corr, f2: (y - f1 <= x + corr <= y + f2)

        out_of_range_distance = math.sqrt(
            sum(math.fabs(val[0] + val[2][1] - val[1])**2 if not deviation_test(val[0], val[1], val[2][0], val[2][1], val[2][2]) else 0
                for val in zip(scan_data, last[1], last[2])
                )
        )

        deviations_by_axis = [(-val[2][0], val[1] - (val[0] + val[2][1]), val[2][2]) for val in zip(scan_data, last[1], last[2])]

        lasts_distances.append((last[0], real_distance, out_of_range_distance, deviations_by_axis))

    return lasts_distances


def get_metrics_by_sizes(scan_data, lasts_data):

    lasts_metrics = []  # list of (size, metric)

    lasts_distances = get_distances_by_sizes(scan_data, lasts_data)

    max_distance = max(last[1] for last in lasts_distances)

    for last in lasts_distances:
        metric = (1 - last[2] / max_distance) * 100

        lasts_metrics.append((last[0], metric, last[3]))

    return lasts_metrics