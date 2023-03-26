def eulers_totient_phi(m: int) -> int:  # algo for computing totient function

    totient = m

    i = 2

    while i * i <= m:  # searching for factors of m

        if m % i == 0:

            while m % i == 0:
                m //= i  # if a current factor repeats

            totient *= (1.0 - 1.0 / i)  # Euler's product formula

        i += 1

    if m > 1:
        totient = totient * (1.0 - 1.0 / m)  # there is a factor that is larger than sqrt(m), only one such factor is possible

    return int(totient)


print(f'totient: {eulers_totient_phi(6)}')

