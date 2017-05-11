import math

""" difference calculations TYPE4_4"""

#  multiplier for coordinates shift calculation (max deviation by axis * axis_shift_multiplier)
axis_shift_multiplier = 2


def deviation_test(x, y, f1, corr, f2):
    """ test if x + corr in range [-f1+y..y..+f2+y]

        :param x: tested value
        :type x: float
        :param corr: shift between scan and model value
        :type corr: float
        :param y: model value
        :type y: float
        :param f1: -deviation range '+'
        :type f1: float
        :param f1: -correction value
        :type f1: float
        :param f2: +deviation range '-'
        :type f2: float
        :return: float (tested value in range)
        :rtype: float
    """

    value = x + corr if (y - f1 <= x + corr <= y + f2) else 0

    return value


def lists_comparison(list1, list2, ranges):
    """ compare 2 lists by deviation rules
    
    :param list1: list of tested values
    :type list1: list of float
    :param list2: list of model values
    :type list2: list of float
    :param ranges: list of (f1, corr, f2) => deviation range definition x + corr ?=> [-f1-y..y..+f2+y]
    :type ranges: list of (float, float, float)
    :return: float in [0..100]: % of values in expected range
    :rtype: float
    """
    #  value of coord center [center_axis_value] * n normalized by maximum range
    center_axis_value = max(max(r[0], r[2]) for r in ranges) * axis_shift_multiplier

    # coordinates shift to [center_axis_value] * n
    coord_shift = [center_axis_value - list2[n] for n in range(len(list2))]

    tested_list = [deviation_test(list1[n] + coord_shift[n], list2[n] + coord_shift[n], ranges[n][0], ranges[n][1], ranges[n][2]) for n in range(len(list1))]

    value = math.sqrt(sum((y + sh - x) ** 2 for x, y, sh in zip(tested_list, list2, coord_shift)))

    # total = vector from 0 to [center_axis_value] * n
    total = math.sqrt(sum([center_axis_value ** 2] * len(list1)))

    # correct cases when distance to value higher than to total (worst case)
    value = value if value < total else total

    result = 100 - (value / total) * 100

    return result

