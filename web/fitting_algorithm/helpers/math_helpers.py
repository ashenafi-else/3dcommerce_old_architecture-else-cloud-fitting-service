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