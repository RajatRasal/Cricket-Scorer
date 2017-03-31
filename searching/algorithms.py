'''
This RECURSIVE MERGESORT is being called in the searching/views.py file to ensure
that any list of teams or players is being displayed in alphabetic order. The 
list of players or teams returned from querying the database will be converted to 
a list and then passed into the merge_sort function as a parameter. 
'''

def merge_sort(unsorted_list):
    # On every iteration, this is the list which will be formed and returned.
    sorted_list = [] # sorted list starts off empty at the beginning of every call

    # Handles the base case of the recursion. If the length is less than one
    # then the merge sort divide and conquer has broken down the initial
    # unsorted list into unit blocks. These can now be built up.
    if len(unsorted_list) <= 1: return unsorted_list

    # Divide and conquer - splits the list in half and sorts each half
    # separately. Each sorted half is returned to the parent functuon where the
    # while loop below builds up the sorted list.
    half = len(unsorted_list) // 2 # floor division by 2 - division rounded down
    lower_list = merge_sort(unsorted_list[:half]) # recursive call with top half
    upper_list = merge_sort(unsorted_list[half:]) # recursive call with bottom half
    lower_list_len, upper_list_len = len(lower_list), len(upper_list) 

    # i is the position counter for the lower list and j is position counter for
    # the upper list.
    i, j = 0, 0
    
    # Now we conduct the actual sorting.
    # While loop continues until iteration counters (i or j) have reached the 
    # max length of either list.
    while i != lower_list_len or j != upper_list_len:
    	# Merge sort will look at the lower_list index, i, and then compare this 
    	# with the upper_list index, j.
    	
    	# Conditional --> checks if value of selected index in the upper list is greater 
    	# than the selected index in the lower in IN TERMS OF ALPHABETICAL ORDER
        if (i != lower_list_len and (j == upper_list_len or lower_list[i] < upper_list[j])):
            # Because upper_list value greater, we add lower_list index value to the
            # sorted_list, since we want an ascending order list in the end
            sorted_list.append(lower_list[i])
            i += 1
        else:
        	# lower_list index value is now greater than the upper_list value
        	# we want an ascending order list so we add the upper_list value to sorted_list
            sorted_list.append(upper_list[j])
            j += 1

	# Passes the sorted_list as a parameter to the previous function in the STACK FRAME 
	# recursion works using a LIFO stack frame
	# Sorted_list returned to the previous outer merge sort function where an unsorted
	# list was passed into as a parameter. 
    return sorted_list

# array = [54, 26, 93, 17, 77, 31, 44, 55]
# ar = merge_sort(array)
# # print(" ".join(str(x) for x in ar))
#