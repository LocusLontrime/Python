# -*- coding: utf-8 -*-

# 2. В большой текстовой строке подсчитать количество встречаемых слов и вернуть 10 самых частых.
# Не учитывать знаки препинания и регистр символов. За основу возьмите любую статью из википедии или из документации к языку.


def get_most_frequent_words(text: str):
    words_freqs = {}
    # building of the words frequencies dict:
    for word in (words := text.split(' ')):
        words_freqs.setdefault(word, 0)
        words_freqs[word] += 1
    # now sorting:
    most_frequent_ones = sorted(words_freqs, key=lambda x: -words_freqs[x])
    # most_frequent_ones number always must be less or equal to 10:
    return most_frequent_ones[:10]


txt = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas sagittis lacinia massa nec rutrum. ' \
      'Phasellus varius scelerisque eros et congue. In vehicula iaculis erat id blandit. Aliquam auctor volutpat mi,' \
      'nec ultricies risus imperdiet at. Etiam lacinia convallis ultricies. Vestibulum sed tincidunt urna.' \
      'Integer gravida augue non nunc accumsan malesuada. Suspendisse molestie fermentum nisi, id vehicula felis.' \
      'Maecenas faucibus, turpis eu egestas cursus, nisi urna congue nunc, id ultricies eros lacus in ante.' \
      'Proin molestie, augue eu rhoncus vehicula, neque sapien volutpat sapien, ut faucibus metus nunc sit amet' \
      'felis. Pellentesque sit amet lorem pellentesque ante convallis mollis. Donec neque mauris, volutpat a orci ' \
      'vitae, sodales faucibus erat. Cras pharetra ornare suscipit. In turpis urna, egestas sit amet ornare in, ' \
      'ultrices non turpis. Fusce vel sapien eget nunc volutpat congue. Aliquam erat turpis, posuere eget tristique ' \
      'vitae, vestibulum nec risus. Sed vehicula leo a dui semper, ut suscipit diam ullamcorper. ' \
      'Interdum et malesuada fames ac ante ipsum primis in faucibus. Integer vel semper justo, ' \
      'et eleifend erat. Etiam at purus eu nisl dignissim varius ut eu eros. Vivamus tempus varius malesuada. ' \
      'Nam tortor justo, varius et nisi nec, ultricies sodales erat. Ut bibendum efficitur arcu, quis eleifend' \
      'nisi vestibulum eu. Sed massa mi, tempor sit amet vestibulum at, eleifend sit amet est. ' \
      'Mauris vitae elit vitae erat gravida convallis et quis neque. Integer semper nulla a justo ' \
      'fermentum bibendum. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ' \
      'ac turpis egestas. Donec eu nisl quis tellus tempus euismod. Vestibulum a lectus iaculis, ' \
      'feugiat magna sed, ultrices purus. Integer ultrices leo non ex iaculis vehicula. Sed sollicitudin' \
      'purus ligula, non porta tellus iaculis in. Mauris varius sollicitudin odio, cursus sodales nunc' \
      'tincidunt nec. Donec blandit volutpat eros, ut commodo erat scelerisque ut. Donec et metus nisi. ' \
      'Vivamus quis tristique erat. Ut pretium mauris et urna interdum dapibus. Fusce pharetra ullamcorper urna. ' \
      'Praesent non urna feugiat, mollis metus a, blandit neque. Vestibulum mollis sed libero in commodo.' \
      'Proin cursus urna mi, eu iaculis augue scelerisque condimentum. Donec pulvinar, neque et elementum varius,' \
      'justo quam pellentesque sem, non auctor orci felis ac nisi. Ut quis pretium dui, sed finibus tellus. ' \
      'Sed facilisis, orci at viverra tristique, felis dolor imperdiet purus, vitae porttitor nunc libero eget odio.' \
      'Sed vulputate mi sit amet sem ultricies mollis. Donec turpis enim, gravida quis ipsum et, convallis' \
      'facilisis tellus. Curabitur eleifend aliquam porta. Donec sodales purus magna, nec tempus ' \
      'sapien molestie at. Integer dolor leo, tincidunt sit amet gravida at, tempus a lorem.' \
      'Pellentesque condimentum, ante a maximus varius, leo urna accumsan diam, nec molestie orci mauris ' \
      'et libero. Curabitur vitae pulvinar est. Integer feugiat diam nisi, sed suscipit magna malesuada quis. ' \
      'Quisque volutpat nec magna quis tristique. Suspendisse imperdiet, massa vel interdum dictum, nulla augue' \
      'posuere sem, sed eleifend velit mi ac quam. Suspendisse justo felis, tempor vel faucibus in, luctus ac enim.'


print(f'most frequent ones: {get_most_frequent_words(txt)}')
