# accepted om codewars.com
def make_triangle(m: int, n: int):
    print(f'validating... {(max_ := validate(n - m + 1))}')
    triangle = [['*' for _ in range(length)] for length in range(1, max_ + 1)]
    print(f'triangle:\n{triangle}')
    m_, triangles_q = m, (max_ + 2) // 3
    print(f'triangles_q: {triangles_q}')
    for k in range(triangles_q):
        j, i = 2 * k, k
        print(f'k, j, i: {k, j, i}')
        while j < max_ - k - 1:
            print(f'1st cycle, (j, i): {j, i}')
            triangle[j][i] = m_ % 10
            j, i, m_ = j + 1, i + 1, m_ + 1
        while i >= k + 1:
            print(f'2nd cycle, (j, i): {j, i}')
            triangle[j][i] = m_ % 10
            i, m_ = i - 1, m_ + 1
        while j >= 2 * k + 1:
            print(f'3rd cycle, (j, i): {j, i}')
            triangle[j][i] = m_ % 10
            j, m_ = j - 1, m_ + 1
        if triangle[j][i] == '*':
            triangle[j][i] = m_ % 10
            m_ += 1
    return '\n'.join(' ' * (max_ - ind - 1) + ' '.join(str(el) for el in row) for ind, row in enumerate(triangle))


def validate(delta: int):
    return int((-1 + r) / 2) if (r := (1 + 8 * delta) ** .5) % 1 == .0 else 0


print(f'triangle:\n\n{make_triangle(0, 5050 - 1)}')
print(f'triangle:\n\n{make_triangle(1, 10)}')


