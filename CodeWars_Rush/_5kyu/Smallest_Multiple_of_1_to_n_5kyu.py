# accepted on codewars.com

# not he best algorithm... slowly enough. Sometimes gets runtime error...
MODULO = 1_000_000_007
MAX = 3_000_000 + 1

prime = [0 for i in range(MAX)]
max_map = dict()
multiples = []


def smallest_multiple(n: int) -> int:
    global multiples
    print(f'{n = }')

    if not multiples:
        sieve()

        multiples = [0]
        multiple_ = 1

        for j in range(1, MAX):
            num = j
            temp = dict()

            # temp stores mapping of prime factors
            # to its power for the current element
            while num > 1:

                # factor is the smallest prime
                # factor of num
                factor = prime[num]

                # Increase count of factor in temp
                if factor in temp.keys():
                    temp[factor] += 1
                else:
                    temp[factor] = 1

                # Reduce num by its prime factor
                num = num // factor

            for p in temp:
                # store the highest power of every prime
                # found till now in a new map max_map
                if p in max_map.keys():
                    if temp[p] > max_map[p]:
                        multiple_ = (multiple_ * pow(p, temp[p] - max_map[p], MODULO)) % MODULO
                        max_map[p] = temp[p]
                else:
                    multiple_ = (multiple_ * pow(p, temp[p], MODULO)) % MODULO
                    max_map[p] = temp[p]

            multiples += [multiple_]

    print(f'{multiples = }')
    print(f'len of multiples: {len(multiples)}')

    return multiples[n]


# function to find the smallest prime
# factors of numbers upto MAX
def sieve():
    prime[0], prime[1] = 1, 1
    for i in range(2, MAX):
        if prime[i] == 0:
            for j in range(i * 2, MAX, i):
                if prime[j] == 0:
                    prime[j] = i
            prime[i] = i


print(f'{smallest_multiple(81)}')



























