from Insertion_sort import insertion_sort as sort


def bucket_sort(array: list[int], buckets_num: int):
    # define the min and max elements for the array given
    largest_element = max(array)
    least_element = min(array)
    print(f'max el: {largest_element}, min el: {least_element}')
    # now let us calculate the range and bucket size:
    rng = largest_element - least_element
    bucket_width = rng / buckets_num
    print(f'bucket width: {bucket_width}')
    # creating buckets for further sorting:
    buckets = [[] for _ in range(buckets_num)]
    # now we are allocating the array's elements into buckets previously created:
    for i in range(len(array)):
        temp = (array[i] - least_element) / bucket_width
        difference = temp - int(temp)
        # here we are adding the boundary array elements to the left bucket:
        if difference == 0 and array[i] != least_element:
            k = int(temp) - 1
            print(f'min el --> bucket index: {k}')
            buckets[k].append(array[i])
        else:
            k = int(temp)
            print(f'bucket index: {k}')
            buckets[k].append(array[i])
    # sorting each bucket separately:
    if len(buckets) != 0:
        for i in range(len(buckets)):
            # here we are using previously implemented insertion sort fot an every bucket
            sort(buckets[i])
    # now we are gathering all the elements located in the buckets into a result array
    i = 0
    for bucket in buckets:
        if len(bucket) > 0:
            for el in bucket:
                array[i] = el
                i += 1


arr = [1, 1, 3, 1, 5, 15, 77, 989, 9, 9, 111, 98989, 98]
arr_x = [1, 5, 6, 7, 4, 2, 2, 2, 0, 8, 7, 6, 9, 9, 7, 5, 1, 1, 9, 1, 9, 7, 7, 9]
bucket_sort(arr_x, 5)
print(arr_x)
