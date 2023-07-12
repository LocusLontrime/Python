# accepted on coderun
import http.client

# task important pars:
VARS_Q = 4

method = 'MEW'

request_header = "X-Cat-Variable"
response_header = "X-Cat-Value"


def get_values():
    names = get_pars()
    print(f'names: {names}')
    # connection establishing:
    client_ = http.client.HTTPConnection('127.0.0.1', 7777)
    client_.connect()
    values_data = []
    names_queries = [
        [names[1], names[2]],
        [names[1], names[3]],
        [names[0], names[2], names[3]]
    ]
    for query in names_queries:
        values_data.append(req(client_, query).split(', '))
    print(f'values_data: {values_data}')
    if values_data[0] == values_data[1]:
        print(f'value3 = value4')
        # value3 = value4
        val_set_2 = set(values_data[2])
        print(f'val_set_2: {val_set_2}')
        val4 = val3 = val_set_2.pop() if len(val_set_2) == 1 else sorted(val_set_2, key=lambda x: values_data[2].count(x), reverse=True)[0]
        print(f'val4 = val3: {val3}')
        val2 = set(values_data[0]).difference({val3})
        val2 = val2.pop() if val2 else val3
        val1 = val_set_2.difference({val3})
        val1 = val1.pop() if val1 else val3
    else:
        val2 = set(values_data[0]).intersection(set(values_data[1])).pop()
        val3 = set(values_data[0]).difference({val2})
        val3 = val3.pop() if val3 else val2
        val4 = set(values_data[1]).difference({val2})
        val4 = val4.pop() if val4 else val2
        val1 = set(values_data[2]).difference({val3, val4})  # list needed!!!
        val1 = val1.pop() if val1 else (val3 if values_data[2].count(val3) == 2 else val4)
    print(f'{val1}\n{val2}\n{val3}\n{val4}')


def req(client_: http.client, names):
    names = ', '.join(names)
    client_.request(method, '', headers={request_header: names})
    response_ = client_.getresponse()
    return response_.getheader(response_header)


def get_pars():
    names = [input() for _ in range(VARS_Q)]
    return names


get_values()






