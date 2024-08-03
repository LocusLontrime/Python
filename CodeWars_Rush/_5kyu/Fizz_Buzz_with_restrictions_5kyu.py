# accepted on codewars.com
fizz_buzz = lambda n: ["Fizz Buzz", [["Fizz", "Buzz"][n % 3 > 0], f'{n}'][bool(n % 3) and bool(n % 5)]][n % 15 > 0]


for n_ in [3, 5, 15, 23]:
    print(f'fizz_buzz({n_}) -> {fizz_buzz(n_)}')


