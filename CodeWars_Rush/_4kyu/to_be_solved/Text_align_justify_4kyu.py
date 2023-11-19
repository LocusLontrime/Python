# accepted on codewars.com
def justify(text: str, width: int):
    words = [word for word in text.split(' ') if word]
    text_justified = ''
    i = 0
    while i < len(words):
        length, temp_i = 0, i
        while i < len(words) and (length_ := length + len(words[i])) + (i - temp_i) <= width:
            length, i = length_, i + 1
        words_q = i - temp_i
        interval_q, rem = divmod(width - length, words_q - 1) if words_q > 1 else (0, 0)
        row = ''
        for ind in range(temp_i, i):
            row += words[ind]
            if i != len(words):
                if ind - temp_i < rem:
                    row += ' ' * (interval_q + 1)
                elif ind < i - 1:
                    row += ' ' * interval_q
            else:
                if ind < i - 1:
                    row += ' '
        text_justified += f'{row}\n'
    return text_justified[:-1]


string_ = f'The one she loved slayed so many souls... she never knew how deadly he become '  # width = 17
ex = f'PrC WWrwQULTI Ko yF hfwH Vo TW ZWY xpFEJOpej SozO gDOtZMQyZD HCADNI jxdzcIs Qeum H c rlE QSxnQ iXMYTMq NEldHKHlmI Xx iIGG PxNZqY WuHW ' \
     f'eP PwDbWmGPw RxDABqLgrG ChwRbotaeR msH vW hgrrLRDhoF mMJiH fVgrqKjLd tSzuUScW cavn ghqw poCjgVPe cRPY gkJwok jUzAFCJ MuoxNYqSi akFm YsJYBNU ' \
     f'b cFN zeYEXkhu'  # width = 28

print(f'text justified:\n{justify(ex, 28)}')

# print(f'{"lala   fafa".split(" ")}')


print(f'lala')
