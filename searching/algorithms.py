def merge_sort(unsorted_list):
    print('Divide and conquer')
    # On every iteration, this is the list which will be formed and returned.
    sorted_list = []

    # Handles the base xase of the recursion. If the length is less than one
    # then the merge sort divide and conquer has broken down the initial
    # unsorted list into unit blocks. These can now be built up.
    if len(unsorted_list) <= 1: return unsorted_list

    # Divide and conquer - splits the list in half and sorts each half
    # separately. Each sorted half is returned to the parent functuon where the
    # while loop below builds up the sorted list.
    half = len(unsorted_list) // 2
    lower_list = merge_sort(unsorted_list[:half])
    upper_list = merge_sort(unsorted_list[half:])
    lower_list_len, upper_list_len = len(lower_list), len(upper_list)

    # i is the position counter for the lower list and j is position counter for
    # the upper list.
    i, j = 0, 0
    print('LOWER: {} UPPER: {}'.format(lower_list, upper_list))
    # conducts the actual sorting.
    # while loop continues until we have reached the max length of either list
    while i != lower_list_len or j != upper_list_len:
        print('i: {}, j: {}'.format(i,j))
        if (i != lower_list_len and (j == upper_list_len or lower_list[i] < upper_list[j])):
            # print('lower_list {} < upper_list {}'.format(lower_list[i], upper_list[j]))
            print('SORTED IF:',sorted_list)
            sorted_list.append(lower_list[i])
            i += 1
        else:
            # print('ELSE: i: {}, j: {}'.format(i,j))
            # print('lower_list {} > upper_list {}'.format(lower_list[i], upper_list[j]))
            sorted_list.append(upper_list[j])
            j += 1
            print('SORTED ELSE:',sorted_list)

    print('Sorted: {}'.format(sorted_list))
    print()
    print()
    print()
    return sorted_list

# array = [54, 26, 93, 17, 77, 31, 44, 55]
# ar = merge_sort(array)
# print(" ".join(str(x) for x in ar))
#
array = ['England Men', 'Australia',
         'England Women', 'India',
         'India Men', 'South Africa', 'Australia', 'Austrlia']
ar = merge_sort(array)
print(" ".join(str(x) for x in ar))
