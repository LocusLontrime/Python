# accepted on coderun
import sys


def hack_server():
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    # password length:
    n = int(input())
    pass_ = ['a' for _ in range(n)]
    # main cycle:
    for i in range(n):
        # left border check:
        print_(pass_)
        sharskii_left = int(input())
        if sharskii_left == 0:
            return
        # right border check:
        pass_[i] = alphabet[-1]
        sys.stdout.flush()
        print_(pass_)
        sharskii_right = int(input())
        if sharskii_right == 0:
            return
        # logic:
        symbol_ = (sharskii_left - sharskii_right + len(alphabet) - 1) // 2  # index here
        symbol_ = alphabet[symbol_]  # alphabetical symbol here
        # final step, pass' symbol changing:
        pass_[i] = symbol_
        sys.stdout.flush()
        # print(f'{i + 1}. {pass_=}')
    print_(pass_)
    # sys.stdout.flush()


def print_(pass_: list[str]):
    print(f'{"".join(pass_)}')


def main():
    hack_server()


if __name__ == '__main__':
    main()
