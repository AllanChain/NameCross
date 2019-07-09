import argparse
from random import shuffle

from PIL import Image, ImageDraw, ImageFont

from main import Choice, NameMap, convert_name

CELL_SIZE = 60
X_SHIFT = 0.35
FONT = ImageFont.truetype(
    "C:\\Windows\\Fonts\\consola.ttf", size=CELL_SIZE*3//4)
FONT_BOLD = ImageFont.truetype(
    "C:\\Windows\\Fonts\\consolab.ttf", size=CELL_SIZE*3//4)
FONT_BIG = ImageFont.truetype(
    "C:\\Windows\\Fonts\\constanb.ttf", size=380)


def get_choices(name_map):
    # for i, j in name_map.new_chrs:
    #     draw.text(xy=((X_SHIFT+j)*CELL_SIZE, i*CELL_SIZE),
    #               text=name_map[i, j], fill="black", font=FONT)
    choices = []
    for pos, index, name, pattern in name_map.iter_name(name_map.new_chrs):
        pattern_h, pattern_v = pattern
        i, j = pos
        if pattern_h == name:
            choices.append(
                Choice(name, i, j-index, 'h', pattern_h))
            name_map.rest_name.remove(name)
        elif pattern_v == name:
            choices.append(
                Choice(name, i-index, j, 'v', pattern_v))
            name_map.rest_name.remove(name)
    return choices


def process(filename, output, text):
    name_map = NameMap(
        seed=filename, names=name_pinyin)
    choices = get_choices(name_map)
    W, H = name_map.width*CELL_SIZE, name_map.height*CELL_SIZE
    im0 = Image.new('RGBA', (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(im0)
    w, h = draw.textsize(text, font=FONT_BIG)
    draw.text(((W-w)/2, (H-h)/2), text, fill=(0, 255, 0, 50), font=FONT_BIG)
    im1 = im0.copy()
    im_blank = im0.copy()
    draw = ImageDraw.Draw(im1)

    def all_imgs():
        for i in animate(im0, choices, FONT, 'black', copy=False):
            yield i
        shuffle(choices)
        for i in animate(im1, choices, FONT_BOLD, 'red'):
            yield i
    im_blank.save(output, save_all=True,
                  append_images=all_imgs(), duration=500)


def animate(im, choices, font, color='red', copy=True):
    for choice in choices:
        imc = im.copy() if copy else im
        draw = ImageDraw.Draw(imc)
        if choice.direction == 'h':
            for j, ch in enumerate(choice.pattern):
                if ch == '-':
                    continue
                draw.text(xy=((X_SHIFT+j+choice.x)*CELL_SIZE, choice.y*CELL_SIZE),
                          text=ch, fill=color, font=font)
        elif choice.direction == 'v':  # and y+len(name) <= self.height:
            for i, ch in enumerate(choice.pattern):
                if ch == '-':
                    continue
                draw.text(xy=((X_SHIFT+choice.x)*CELL_SIZE, (choice.y+i)*CELL_SIZE),
                          text=ch, fill=color, font=font)
        if copy:
            yield imc
        else:
            yield imc.copy()


# tmp_map = NameMap.empty(name_map.height, name_map.width)
# if choice.direction == 'h':
#     tmp_map[choice.y, choice.x:choice.x+len(choice.name)] =\
#         choice.name
# elif choice.direction == 'v':  # and y+len(name) <= self.height:
#     tmp_map[choice.y:choice.y+len(choice.name), choice.x] =\
#         choice.name
# # print(tmp_map.text_plain())

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', '-d', required=True,
                        help='Name data file')
    parser.add_argument('--input', '-i', required=True,
                        help='Input name map file')
    parser.add_argument('--text', '-t', required=False, default='303',
                        help='Text to draw')
    parser.add_argument('--output', '-o', required=True,
                        help='Output directory')
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    name_pinyin = convert_name(args.data)
    process(args.input, args.output, args.text)
