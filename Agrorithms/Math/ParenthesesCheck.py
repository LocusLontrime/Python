def is_balanced(text, brackets="??()[]{}"):

    opening, closing = brackets[::2], brackets[1::2]
    stack = []  # keep track of opening brackets types

    for character in text:

        print(stack)

        if character in opening:  # bracket
            stack.append(opening.index(character))
        elif character in closing:  # bracket

            if stack and stack[-1] == closing.index(character):
                stack.pop()  # remove the matched pair
            else:
                return False  # unbalanced (no corresponding opening bracket) or  unmatched (different type) closing bracket

    return not stack  # no unbalanced brackets


print(is_balanced("{([)(])}"))
print(is_balanced("{()[]}"))

