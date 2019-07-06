#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import random
from collections import namedtuple
from hashlib import md5
from heapq import nlargest
from math import copysign

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
                 'score', 'new_chrs', 'data', 'height', 'width']

    def __init__(self, seed):
        if isinstance(seed, str):
            with open(seed) as f:
                self.data = [list(line[:-1]) for line in f.readlines()]
        elif isinstance(seed, list):
            self.data = seed
        self.width = len(self.data[0])
        self.height = len(self.data)

    def __getitem__(self, args):
        rows, columns = args
        if isinstance(columns, int) and isinstance(rows, slice):
            return [self.data[i][columns] for i in range(rows.start, rows.stop)]
        # Omit checks to be faster
        return self.data[rows][columns]

    def __setitem__(self, args, name):
        rows, columns = args
        if isinstance(rows, int) and isinstance(columns, (slice, int)):
            self.data[rows][columns] = name
        elif isinstance(columns, int) and isinstance(rows, slice):
            for i in range(rows.start, rows.stop):
                self.data[i][columns] = name[i - rows.start]
        else:
            raise ValueError('Slice invalid')

    def digest(self):
        '''To digest input data and set some attributes'''
        self.chr_total = 0
        self.border = 0
        self.new_chrs = []
        self.rest_name = name_pinyin.copy()
        for i in range(self.height):
            for j in range(self.width):
                if self[i, j] != '-':
                    self.chr_total += 1
                    self.border += self.get_blanks(i, j)
                    self.new_chrs.append((i, j))

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
        new_map.rest_name.remove(choice.name)
        used_chr = 0
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
                used_chr += 1
        new_map.evaluate(used_chr, choice.name)
        return new_map

    def evaluate(self, used_chr, name):
        # print(self.text_plain())
        score = a*self.border**2/self.chr_total
        score = copysign(score, 30-self.chr_total)
        # print(score, end=' ')
        score += b*used_chr  # *exp(c*self.chr_total)
        # print(score, end=' ')
        score += d*name_freq[''.join(name)]/freq_total
        # print(score)
        # print(self.text_plain(), score)
        self.score = score

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

    def iter_border(self):
        for i in range(self.height):
            for j in range(self.width):
                if self[i, j] != '-' and self.get_blanks(i, j) > 0:
                    yield i, j

    def iter_name(self, iterator):
        for i, j in iterator:
            name_chr = self.data[i][j]
            available_names = [n for n in self.rest_name if name_chr in n]
            for name in available_names:
                # ADD: name with some same letters
                index = name.index(name_chr)
                if not (0 <= j-index <= self.width-len(name) and
                        0 <= i-index <= self.height-len(name)):
                    # Make sure index in range
                    continue
                pattern_h = self[i, j-index:j-index+len(name)]
                pattern_v = self[i-index:i-index+len(name), j]
                yield (i, j), index, name, (pattern_h, pattern_v)

    def get_blanks(self, i, j):
        def is_blank(pos):
            i, j = pos
            try:
                return self.data[i][j] == '-'
            except IndexError:
                return False
        return len([is_blank(i) for i in ((i-1, j), (i+1, j),
                                   (i, j-1), (i, j+1))])

    def get_choices(self):
        choices = []
        for _, __, name, pattern in self.iter_name(self.new_chrs):
            if name in pattern:
                self.rest_name.remove(name)
        for pos, index, name, pattern in self.iter_name(self.iter_border()):
            i, j = pos
            pattern_h, pattern_v = pattern
            if match(pattern_h, name):
                choices.append(
                    Choice(name, i, j-index, 'h', pattern_h))
            elif match(pattern_v, name):
                choices.append(
                    Choice(name, i-index, j, 'v', pattern_v))
        return choices


def main():
    global freq_total
    for _ in range(10):
        name_map = NameMap(seed='seed_one.txt')
        name_map.digest()
        while name_map.rest_name:
            new_maps = [name_map.adopt(m) for m in name_map.get_choices()]
            if not new_maps:
                break
            name_map = random.choice(
                nlargest(5, new_maps, key=lambda m: m.score))
        for name in name_map.rest_name:
            name_freq[''.join(name)] += 1
            freq_total += 1
        if not name_map.rest_name:
            name_map.save_plain(
                'solutions/'+md5(name_map.text_plain().encode()).hexdigest())
            print(name_map.text_plain())
        # print(name_freq)


if __name__ == "__main__":
    a, b, c, d = 0.6, 20, -0.02, 50
    name_pinyin = convert_name()
    try:
        with open('freq.pkl', 'rb') as f:
            name_freq = pickle.load(f)
        freq_total = sum(name_freq.values())
    except FileNotFoundError:
        name_freq = {''.join(name): 0 for name in name_pinyin}
        freq_total = 0
    print(name_freq)
    main()
    with open('freq.pkl', 'wb') as f:
        pickle.dump(name_freq, f)
