# all accepted on codewars.com
def queue_time(customers: list, n: int):
    if n == 1:
        return sum(customers)
    elif n >= len(customers):
        return max(customers)
    else:
        customers_on_tills = []
        result_time = 0
        counter = 0

        while counter < len(customers):
            # free tills fulfilling
            while len(customers_on_tills) < n and counter < len(customers):
                customers_on_tills.append(customers[counter])
                counter += 1

            fastest_customer = min(customers_on_tills)
            print(f'The fastest customer = {fastest_customer}')
            print(f'customers on tills before: {customers_on_tills}')
            i = 0
            # time ticking and removing the checked customers
            while i < len(customers_on_tills):
                customers_on_tills[i] -= fastest_customer

                if customers_on_tills[i] != 0:
                    i += 1
                else:
                    customers_on_tills.remove(0)
            result_time += fastest_customer

            print(f'customers on tills after: {customers_on_tills}')
        return result_time + (max(customers_on_tills) if len(customers_on_tills) > 0 else 0)


def queue_time_set(customers: list, n: int):

    print("LALALA")

    if n == 1:
        return sum(customers)
    elif n >= len(customers):
        return max(customers)
    else:
        customers_on_tills = dict()
        customers_on_tills_number = 0
        result_time = 0
        counter = 0

        while counter < len(customers):
            # free tills fulfilling
            while customers_on_tills_number < n:
                if counter >= len(customers):
                    break
                if customers[counter] in customers_on_tills:
                    customers_on_tills[customers[counter]] += 1
                else:
                    customers_on_tills[customers[counter]] = 1

                customers_on_tills_number += 1
                counter += 1

            fastest_customer = min(customers_on_tills.keys())
            print(f'The fastest customer = {fastest_customer}')
            print(f'customers on tills before: {customers_on_tills}')

            # time ticking and removing the checked customers

            customers_on_tills_number -= customers_on_tills[fastest_customer]
            del customers_on_tills[fastest_customer]

            customers_on_tills = {customer_on_tills[0] - fastest_customer: customer_on_tills[1] for customer_on_tills in customers_on_tills.items()}

            result_time += fastest_customer

            print(f'customers on tills after: {customers_on_tills}')
        return result_time + (max(customers_on_tills.keys()) if len(customers_on_tills) > 0 else 0)


def queue_time_fast(customers, n):
    tills = [0] * n

    for customer in customers:
        tills[tills.index(min(tills))] += customer

    return max(tills)


# print(queue_time([10, 2, 3, 3], 2))
# print(queue_time([25, 26, 20, 8, 34, 29, 47, 40, 44, 9, 7, 35], 3))
#
# print(queue_time_set([25, 26, 20, 8, 34, 29, 47, 40, 44, 9, 7, 35], 3))
# print(queue_time_set([2, 2, 3, 3, 4, 4], 2))

print(queue_time([4, 34, 8, 17, 15, 17, 33, 12, 13, 42, 38, 8, 1, 49, 37, 10, 47, 25, 48, 3], 6))
print(queue_time_set([4, 34, 8, 17, 15, 17, 33, 12, 13, 42, 38, 8, 1, 49, 37, 10, 47, 25, 48, 3], 6))
print(queue_time_fast([4, 34, 8, 17, 15, 17, 33, 12, 13, 42, 38, 8, 1, 49, 37, 10, 47, 25, 48, 3], 6))
