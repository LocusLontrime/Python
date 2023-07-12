# accepted on coderun
import requests
import xml.etree.ElementTree
import re


server = 'http://127.0.0.1:7777/'
method = 'GET'
participants_req = 'view/participants'
submissions_req = 'view/submissions'
par_attr_name = 'login'
sub_attrs_names = ['timestamp', 'problem', 'verdict']
verdicts = ['OK', 'CE', 'WA', 'TL', 'RE']
TIME_PEN = 20


def get_winners():
    contest_name = get_pars()
    # participants request:
    url_ = f'{server}{participants_req}?contest={contest_name}'  # /view/participants?contest=backend_contest
    resp_participants = requests.request(method, url_)
    # saving the xml file
    with open('participants.xml', 'w+') as f:
        add_, new_text = resp_participants.text.split('\n')
        new_text = re.sub(r'(<.+?>)', r'\1\n', new_text)
        new_text = re.sub(r'(<.+?/>)', r'\t\1', new_text)
        f.write(f'{add_}\n{new_text}')
        f.seek(0)
        xml_ = xml.etree.ElementTree.parse(f)
        participants = [_.get(f'{par_attr_name}') for _ in xml_.getroot().findall(path="participant")]  # backend_contest
    # submissions request
    # participant's dict:
    pd: dict[str, list[int, int]] = {}
    for participant_ in participants:
        sd = dict()
        problems_solved = set()
        url_ = f'{server}{submissions_req}?contest={contest_name}&{par_attr_name}={participant_}'  # /view/submissions?contest=backend_contest\&login=polycarp
        resp_submissions = requests.request(method, url_)
        print(f'participant_: {participant_}')
        # saving the xml file
        with open('submissions.xml', 'w+') as f:
            add_, new_text = resp_submissions.text.split('\n')
            new_text = re.sub(r'(<.+?>)', r'\1\n', new_text)
            new_text = re.sub(r'(<.+?/>)', r'\t\1', new_text)
            f.write(f'{add_}\n{new_text}')
            f.seek(0)
            xml_ = xml.etree.ElementTree.parse(f)
            submissions_ = [[_.get(f'{x}') for x in sub_attrs_names] for _ in xml_.getroot().findall(path="submission")]
            print(f'submissions_: {submissions_}')
            for timestamp_, problem_, verdict_ in submissions_:
                timestamp_ = int(timestamp_)
                if problem_ not in sd.keys():
                    sd[problem_] = -1
                if sd[problem_] == -1 or sd[problem_] != -1 and timestamp_ < sd[problem_]:
                    if verdict_ == verdicts[0]:
                        sd[problem_] = timestamp_
                        problems_solved.add(problem_)
        penalty_ = sum(sd[p_] for p_ in problems_solved)
        penalty_ += sum(1 for s in submissions_ if s[2] in verdicts[2: 5] and int(s[0]) <= sd[s[1]]) * TIME_PEN
        pd[participant_] = [len(problems_solved), penalty_]
    print(f'pd: ')
    for k, v in pd.items():
        print(f'{k}: {v}')
    sorted_keys = sorted(pd.keys(), key=lambda x: (-pd[x][0], pd[x][1]))
    print(f'sorted_keys: {sorted_keys}')
    best_participant = sorted_keys[0]
    max_problem_solved, min_penalty = pd[best_participant][0], pd[best_participant][1]
    winners = [x for x in sorted_keys if pd[x][0] == max_problem_solved and pd[x][1] == min_penalty]
    print(f'{len(winners)}')
    winners = sorted(winners)
    for winner_ in winners:
        print(f'winners: {winner_}')


def get_pars():
    contest_name = input()
    return contest_name


get_winners()

