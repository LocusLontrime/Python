def convert_to_rgb(hex_colour: str):
    # converts colour like 'ffffff' to (ff, ff, ff)
    return int(hex_colour[0: 2], 16), int(hex_colour[2: 4], 16), int(hex_colour[4: 6], 16)


rgb = f'ffba98'


print(f'res: {convert_to_rgb(rgb)}')


