"""
"""


def merge_sort(unsorted_list):
    sorted_list = []
    if len(unsorted_list) <= 1: return unsorted_list

    half = len(unsorted_list) // 2
    lower = merge_sort(unsorted_list[:half])
    upper = merge_sort(unsorted_list[half:])
    lower_len, upper_len = len(lower), len(upper)
    #upper_len = len(upper)

    i, j = 0, 0
    #j = 0

    while i != lower_len or j != upper_len:
        if (i != lower_len and (j == upper_len or lower[i] < upper[j])):
            sorted_list.append(lower[i])
            i += 1
        else:
            sorted_list.append(upper[j])
            j += 1

    return sorted_list

# array = [54, 26, 93, 17, 77, 31, 44, 55]
# ar = merge_sort(array)
# print(" ".join(str(x) for x in ar))
#
# array = ['England Men', 'Australia',
#          'England Women', 'India',
#          'India Men', 'South Africa']
# ar = merge_sort(array)
# print(" ".join(str(x) for x in ar))
