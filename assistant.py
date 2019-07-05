#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import random
from collections import namedtuple
from hashlib import md5

# from math import exp
# from time import process_time


def convert_name():
    import pinyin

    with open('name_data.txt', encoding='utf-8') as f:
        names = f.readlines()
        return list(
            map(lambda name: pinyin.get_initial(name[:-1]).split(' '), names))


Choice = namedtuple('Choice', 'name y x direction pattern'.split(' '))


def match(pattern, name):
    if len(pattern) != len(name):
        raise ValueError('Must same length')
    for p, n in zip(pattern, name):
        if not p in ('-', n):
            return False
    return True


class NameMap:
    __slots__ = ['border', 'chr_total', 'rest_name',
                 'used_chr', 'new_chrs', 'data', 'height', 'width']

    def __init__(self, seed):
        self.border = 0
        self.chr_total = 0
        self.rest_name = []
        self.used_chr = 0
        if isinstance(seed, str):
            with open(seed) as f:
                self.data = list(
                    map(lambda line: list(line[:-1]), f.readlines()))
        elif isinstance(seed, list):
            self.data = seed
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

    def __setitem__(self, args, name):
        rows, columns = args
        if isinstance(rows, int) and isinstance(columns, (slice, int)):
            self.data[rows][columns] = name
        elif isinstance(columns, int) and isinstance(rows, slice):
            for i in range(rows.start, rows.stop):
                self.data[i][columns] = name[i - rows.start]
        else:
            raise ValueError('Slice invalid')

    @staticmethod
    def empty(w, h):
        data = []
        for _ in range(h):
            data.append(['-'] * w)
        return NameMap(data)

    def copy(self):
        data = []
        for i in range(self.height):
            data.append(self[i, :])
        new_map = NameMap(seed=data)
        new_map.border = self.border
        new_map.chr_total = self.chr_total
        new_map.rest_name = self.rest_name.copy()
        return new_map

    def adopt(self, choice):
        new_map = self.copy()
        new_map.new_chrs = []
        if choice.direction == 'h':
            new_map[choice.y, choice.x:choice.x+len(choice.name)] =\
                choice.name
        elif choice.direction == 'v':  # and y+len(name) <= self.height:
            new_map[choice.y:choice.y+len(choice.name), choice.x] =\
                choice.name
        for index, ch in enumerate(choice.pattern):
            if ch == '-':
                new_map.chr_total += 1
                if choice.direction == 'h':
                    i, j = choice.y, choice.x+index
                else:
                    i, j = choice.y+index, choice.x
                new_map.border += self.get_blanks(i, j) + \
                    new_map.get_blanks(i, j)-4
                new_map.new_chrs.append((i, j))
            else:
                new_map.used_chr += 1
        return new_map

    def text_plain(self, nu=False):
        text = ''
        if nu:
            # text += ''.join(map(str,range(self.width)))
            text += '01234567890123\n'
        for row in self.data:
            text += ''.join(row)+'\n'
        return text

    def save_plain(self, dest):
        with open(dest, 'w', encoding='utf-8', newline='\n') as f:
            f.write(self.text_plain())

    def iter_chr(self):
        self.border = 0
        self.chr_total = 0
        for i in range(self.height):
            for j in range(self.width):
                if self[i, j] != '-':
                    self.chr_total += 1
                    border_count = self.get_blanks(i, j)
                    self.border += border_count
                    yield ((i, j), border_count)

    def get_blanks(self, i, j):
        def is_blank(pos):
            i, j = pos
            return (0 <= i < self.height and
                    0 <= j < self.width and
                    self.data[i][j] == '-')
        return list(map(is_blank, [(i-1, j), (i+1, j),
                                   (i, j-1), (i, j+1)])).count(True)

    def get_choices(self):
        choices = []
        for pos, border_count in self.iter_chr():
            i, j = pos
            name_chr = self[i, j]
            available_names = list(filter(
                lambda n: name_chr in n, self.rest_name))
            for name in available_names:
                # ADD: name with some same letters
                index = name.index(name_chr)
                if not (0 <= j-index <= self.width-len(name) and
                        0 <= i-index <= self.height-len(name)):
                    # Make sure index in range
                    continue
                pattern_h = self[i, j-index:j-index+len(name)]
                pattern_v = self[i-index:i-index+len(name), j]
                if name in (pattern_h, pattern_v):
                    self.rest_name.remove(name)
                    # This name will not involve further matching
                    # as it is automatically in the map
                    continue
                # Only when it has blanks is there hope to match
                if border_count != 0:
                    if match(pattern_h, name):
                        choices.append(
                            Choice(name, i, j-index, 'h', pattern_h))
                    elif match(pattern_v, name):
                        choices.append(
                            Choice(name, i-index, j, 'v', pattern_v))
        # Check again if the name has been removed later on
        choices = list(
            filter(lambda choice: choice.name in self.rest_name, choices))
        return choices


def get_max_ones(l, key):
    max_ones = [l[0]]
    max_value = key(l[0])
    if len(l) > 1:
        for item in l[1:]:
            value = key(item)
            if value > max_value:
                max_ones = [item]
                max_value = value
            elif value == max_value:
                max_ones.append(item)
    return max_ones


def main():
    def evaluate(new_map):
        score = 100-a*new_map.border**2/new_map.chr_total +\
            b*new_map.used_chr  # *exp(c*new_map.chr_total)
        for name, freq in name_freq.items():
            if freq > 0 and name not in new_map.rest_name:
                score += d*freq/freq_total
        # print(new_map.text_plain(), score)
        return score
    a, b, c, d = 2, 2, -0.02, 5
    name_pinyin = convert_name()
    try:
        with open('freq.pkl', 'rb') as f:
            name_freq = pickle.load(f)
        freq_total = sum(name_freq.values())
    except FileNotFoundError:
        name_freq = {''.join(name): 0 for name in name_pinyin}
        freq_total = 0
    print(name_freq)
    for _ in range(100):
        name_map = NameMap(seed='seed_one.txt')
        name_map.rest_name = name_pinyin.copy()
        while name_map.rest_name:
            new_maps = [name_map.adopt(m) for m in name_map.get_choices()]
            if not new_maps:
                break
            name_map = random.choice(get_max_ones(new_maps, evaluate))
        for name in name_map.rest_name:
            name_freq[''.join(name)] += 1
            freq_total += 1
        if not name_map.rest_name:
            name_map.save_plain(
                'solutions/'+md5(name_map.text_plain().encode()).hexdigest())
            print(name_map.text_plain())
            # print(name_freq)
    with open('freq.pkl', 'wb') as f:
        pickle.dump(name_freq, f)


if __name__ == "__main__":
    main()
