progressions = []


def process_the_request(req_str):
    global progressions

    if req_str[0] == '1':
        nums_str = req_str.split(" ")
        print(f'nums str 1: {nums_str}')
        progressions.append([int(nums_str[1]), int(nums_str[2]), int(nums_str[3])])
    elif req_str[0] == '2':
        nums_str = req_str.split(" ")
        print(f'nums str s: {nums_str}')
        for i in range(len(progressions)):
            if progressions[i][2] == int(nums_str[1]):
                progressions.pop(i)
                break
    elif req_str[0] == '3':
        def sort_val(e):
            return [e[0], e[2]]

        progressions = sorted(progressions, key=sort_val)

        print(f'sorted progressions: {progressions}')

        result_elem = progressions[0][0]

        progressions[0][0] += progressions[0][1]

        return result_elem

    else:
        print('wrong operation')
        return








print("1 2 -4 1".split(" "))
strs = ["1 3 -4 1", "1 -5 4 3", "1 -2 10 2", "3", "3", "2 3", "3", "3", "2 2", "1 -5 4 4", "3", "2 1", "3", "3", "3"]
print(process_the_request(strs[0]))
print(process_the_request(strs[1]))
print(process_the_request(strs[2]))
print(process_the_request(strs[3]))
print(process_the_request(strs[4]))
print(process_the_request(strs[5]))
print(process_the_request(strs[6]))
print(process_the_request(strs[7]))
print(process_the_request(strs[8]))
print(process_the_request(strs[9]))
print(process_the_request(strs[10]))
print(process_the_request(strs[11]))
print(process_the_request(strs[12]))
print(process_the_request(strs[13]))
print(process_the_request(strs[14]))
