import numpy as np
import bisect
from examples import quality_minmax, bulk_quality_minmax

def new_bulk(data, j):
    ceil_data = [np.ceil(i) for i in data]
    floor_data = [np.floor(i) for i in data]
    rounded_data = floor_data + ceil_data
    points_of_interest = list(set(rounded_data))
    start_point = [min(quality_minmax(data,i), quality_minmax(data,i+2**j-1)) for i in  points_of_interest]
    end_point = [min(quality_minmax(data,i-2**j+1), quality_minmax(data,i)) for i in  points_of_interest]
    return max(start_point+end_point)


def bulk_interval_quality_minmax(data, j):
    sorted_data = sorted(data)
    interval_start = 0
    interval_end = int(2**(j-1))
    max_of_min_quality = 0
    mins = []  # testing

    while interval_start <= max(sorted_data) and interval_end <= max(sorted_data):
        next_index_in_interval = bisect.bisect_right(sorted_data, interval_start)
        next_index_after_interval = bisect.bisect_right(sorted_data, interval_end)
        next_element_in_interval = sorted_data[next_index_in_interval]
        next_element_after_interval = sorted_data[next_index_after_interval]

        move_interval = min(next_element_in_interval-interval_start, next_element_after_interval-interval_end)
        interval_start += move_interval
        interval_end = interval_start + int(2**(j-1))
        min_quality = min(q(sorted_data, interval_start), q(sorted_data, interval_end))
        mins.append(min_quality)  # testing
        max_of_min_quality = max(max_of_min_quality, min_quality)

        interval_start += 1
        interval_end = interval_start + int(2**(j-1))
        min_quality = min(quality_minmax(sorted_data, interval_start),
                          quality_minmax(sorted_data, interval_end))
        mins.append(min_quality)  # testing
        max_of_min_quality = max(max_of_min_quality, min_quality)

    print mins  # testing
    return max_of_min_quality


# test example
n1 = 6
n2 = 10
i = 0
r = range(2**n2)

d = np.random.normal(2**n2/2, 2**n1, 2**n1)
qs2 = bulk_quality_minmax(d, r)
qs = new_bulk(d, i)
print max(qs2)
print qs
print [new_bulk(d, x) for x in xrange(0, n2)]