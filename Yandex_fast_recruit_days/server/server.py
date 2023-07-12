import argparse
import http.server as hs
import os
import random
import sys

requests = 0


def parse(header_value):
    return [value.strip() for value in header_value.split(',')]


def random_capitalize(name):
    symbols = [random.choice((c, c.upper())) for c in name]
    return ''.join(symbols)


class MyHTTPHandler(hs.BaseHTTPRequestHandler):
    def do_MEW(self):
        global values, requests
        if self.path != '/':
            print('Invalid path')
            self.send_error(404)
            return

        header_values = self.headers.get_all('x-cat-variable')
        variables = []
        for header_value in header_values:
            variables.extend(parse(header_value))
        if len(set(variables)) != len(variables):
            print('Repeating variables')
            self.send_error(404)
            return
        for var in variables:
            if var not in values:
                print('Variable %s is not known' % var)
                self.send_error(404)
                return
        if requests >= 3:
            print('Too many requests')
            self.send_error(404)
            return
        requests += 1
        answer_values = sorted([values[var] for var in variables])
        print('Request: %d' % requests)
        print('Variables: %s' % ' '.join(variables))
        print('Values: %s' % ' '.join(answer_values))
        self.send_response(200)
        header_name = random_capitalize('x-cat-value')
        for value in answer_values:
            self.send_header(header_name, value)
        self.end_headers()
        return


def get_file_tokens(f):
    result = []
    for line in f:
        tokens = line.split()
        result.extend(tokens)
    return result


def main():
    global values
    parser = argparse.ArgumentParser(description='MEW HTTP Server')
    parser.add_argument('-i', '--input', type=argparse.FileType('r'), help='Variable names', required=True)
    parser.add_argument('-a', '--answer', type=argparse.FileType('r'), help='Variable values', required=True)

    params = parser.parse_args()
    variables_list = get_file_tokens(params.input)
    if len(variables_list) != 4:
        print('Expected 4 variable names found %d names' % len(variables_list))
        sys.exit(1)
    params.input.close()
    values_list = get_file_tokens(params.answer)
    if len(values_list) != 4:
        print('Expected 4 values found %d values' % len(values_list))
    params.answer.close()
    values = {}
    for i in range(4):
        values[variables_list[i]] = values_list[i]

    server = hs.HTTPServer(('127.0.0.1', 7777), MyHTTPHandler)
    server.serve_forever()


if __name__ == '__main__':                                                            # 36.6 98
    main()
