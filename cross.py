import pinyin


def convert_name():
    with open('name_data.txt') as f:
        names = f.readlines()
        return list(
            map(lambda name: pinyin.get_initial(name[:-1]).split(' '), names))


name_pinyin = convert_name()
# print(name_pinyin)


def match(pattern, name):
    if len(pattern) != len(name):
        raise ValueError('Must same length')
    for i in range(len(name)):
        if not pattern[i] in ('-', name[i]):
            return False
    return True


class NameMap:
    def __init__(self, seed=None, size=None):
        self.border = 0
        self.chr_total = 0
        if seed is None and size is not None:
            w, h = size
            self.width, self.height = size
            self.data = []
            for i in range(h):
                self.data.append(['-'] * w)
        elif seed is not None:
            with open(seed) as f:
                self.data = list(
                    map(lambda line: list(line[:-1]), f.readlines()))
                self.width = len(self.data[0])
                self.height = len(self.data)

    def __getitem__(self, args):
        rows, columns = args
        if isinstance(rows, int) and isinstance(columns, (slice, int)):
            return self.data[rows][columns]
        if isinstance(columns, int) and isinstance(rows, slice):
            item = []
            for i in range(rows.start, rows.stop):
                item.append(self.data[i][columns])
            return item
        raise ValueError('Slice invalid')

    def text_plain(self, nu=False):
        text = ''
        if nu:
            # text += ''.join(map(str,range(self.width)))
            text += '01234567890123\n'
        for row in self.data:
            text += ''.join(row) + '\n'
        return text

    def save_plain(self, dest):
        with open(dest, 'w') as f:
            f.write(self.text_plain())

    def detect_border(self):
        self.border = 0
        self.chr_total = 0
        border_pos = []
        for i in range(self.height):
            for j in range(self.width):
                if not self.is_blank((i, j)):
                    blanks = list(map(self.is_blank, [
                        (i-1, j), (i+1, j), (i, j-1), (i, j+1)])).count(True)
                    # print(blanks, (i, j), self.data[i][j])
                    self.border += blanks
                    self.chr_total += 1
                    if blanks > 0:
                        border_pos.append((i, j))
        return border_pos

    def is_blank(self, pos):
        i, j = pos
        return (0 <= i <= self.height and
                0 <= j <= self.width and
                self.data[i][j] == '-')

    def get_choices(self):
        choices = []
        for i in range(self.height):
            for j in range(self.width):
                name_chr = self[i, j]
                if name_chr != '-':
                    available_names = list(filter(
                        lambda n: name_chr in n, name_pinyin))
                    # print('-'*20)
                    for name in available_names:
                        # ADD: name with some same letters
                        index = name.index(name_chr)
                        pattern = self[i, j-index:j-index+len(name)]
                        if pattern == name:
                            name_pinyin.remove(name)
                        elif match(pattern, name):
                            choices.append((name, (i, j)))
                        pattern = self[i-index:i-index+len(name), j]
                        if pattern == name:
                            name_pinyin.remove(name)
                        elif match(pattern, name):
                            choices.append((name, (i, j)))
        choices = list(filter(lambda choice: choice[0] in name_pinyin,
                              choices))
        print(choices)
        # for name, pos in choices:
        #     pass


# name_map = NameMap(size=(14, 7))
name_map = NameMap(seed='seed_alpha.txt')
print(name_map.text_plain(nu=True))
# print(name_map.detect_border())
# name_map.save_plain('map_tmpl')
# print(name_map[2:4, 7])
name_map.get_choices()
