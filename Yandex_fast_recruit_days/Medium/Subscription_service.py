# accepted on coderun
import json
from itertools import chain


offers = []
fields = [
    'price',
    'stock_count',
    'partner_content.title',
    'partner_content.description',
]


def get_pars():
    n, m = map(int, input().strip().split())
    subscribers = [input().strip().split() for _ in range(n)]
    subscribers = [dict(tr=rem[:int(l1)], sh=rem[int(l1): int(l1 + l2)]) for l1, l2, *rem in subscribers]
    queries = [json.loads(input().strip()) for _ in range(m)]
    return n, m, subscribers, queries


def update_field(field, offer, q):
    if '.' in field:
        fields_ = field.split('.')
        parent = fields_[0]
        nested = fields_[1:]
        if parent in q:
            if parent not in offer:
                offer[parent] = dict()
            trigger = update_field('.'.join(nested), offer[parent], q[parent])
            if trigger:
                return [parent] + [
                    f'{parent}.{t}'
                    for t in trigger
                ]
    elif field in q:
        if field not in offer or offer[field] != q[field]:
            offer[field] = q[field]
            return [field]


def insert_field(field, data, offer):
    if '.' in field:
        _fields = field.split('.')
        parent = _fields[0]
        nested = _fields[1:]
        if parent in offer:
            if parent not in data:
                data[parent] = dict()
            insert_field('.'.join(nested), data[parent], offer[parent])
    elif field in offer:
        data[field] = offer[field]


def build_data(s, offer):
    data = dict(id=offer['id'])
    for f in chain(s['tr'], s['sh']):
        insert_field(f, data, offer)
    return data


def process_reqs():
    n, m, subscribers, queries = get_pars()
    for query in queries:
        q_offer = query['offer']
        offer = [_ for _ in offers if _['id'] == q_offer['id']]
        if offer:
            offer = offer[0]
        else:
            offer = dict(id=q_offer['id'])
            offers.append(offer)

        candidates = list(enumerate(subscribers))
        subscribers_for_query = []

        for f in fields:
            triggers = update_field(f, offer, q_offer)
            if triggers:
                subscribers_for_trigger = [
                    (i, s)
                    for i, s in candidates
                    if any(trig in triggers for trig in s['tr'])
                ]
                subscribers_for_query += subscribers_for_trigger
                for s in subscribers_for_trigger:
                    candidates.remove(s)

        subscribers_for_query.sort(key=lambda s: s[0])

        for i, s in subscribers_for_query:
            data = build_data(s, offer)
            trace = dict(
                trace_id=query['trace_id'],
                offer=data
            )
            print(json.dumps(trace))


