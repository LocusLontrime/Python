# accepted on codewars.com
def hex_string_to_RGB(hex_string: str):
    # converts colour like 'ffffff' to (ff, ff, ff)
    return {['r', 'g', 'b'][i // 2]: int(hex_string[1:].lower()[i: i + 2], 16) for i in range(0, 6, 2)}


print(f"res {hex_string_to_RGB('#FF9933')}")





