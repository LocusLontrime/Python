# accepted on codewars.com
adjacents = [
  ['8'],
  ['2', '4'],
  ['1', '3', '5'],
  ['2', '6'],
  ['1', '5', '7'],
  ['2', '4', '6', '8'],
  ['3', '5', '9'],
  ['4', '8'],
  ['0', '5', '7', '9'],
  ['6', '8']
]


def get_pins(observed):
    global adjacents
    '''TODO: This is your job, detective!'''
    result = []

    def recursive_seeker(curr_len, curr_pin):
        if curr_len == len(observed):
            result.append(curr_pin)
            return

        for symbol in adjacents[int(observed[curr_len])] + [observed[curr_len]]:
            recursive_seeker(curr_len + 1, curr_pin + symbol)

    recursive_seeker(0, '')

    return result


print(get_pins('369'))
print(get_pins('8'))
