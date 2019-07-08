#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
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


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', default=100, help='Number of attempts')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        '--seed', '-s', default=None, help='The seed to apply')
    group.add_argument('--random', '-r', default='12x12',
                       help='Specify the random mode and its size, e.g. 12x12')
    return parser.parse_args()


class NameMap:
    __slots__ = ['border', 'chr_total', 'rest_name',
                 'score', 'new_chrs', 'data', 'height', 'width']

    def __init__(self, seed, names=None):
        self.new_chrs = []
        if isinstance(seed, NameMap):
            self.data = [seed[i, :] for i in range(seed.height)]
            self.border = seed.border
            self.chr_total = seed.chr_total
            self.rest_name = seed.rest_name.copy()
            self.width = seed.width
            self.height = seed.height
            return
        if isinstance(seed, str):
            with open(seed) as f:
                self.data = [list(line[:-1]) for line in f.readlines()]
        elif isinstance(seed, list):
            self.data = seed
        else:
            raise ValueError('seed must be instance of NameMap, str or list')
        self.width = len(self.data[0])
        self.height = len(self.data)
        self.chr_total = 0
        self.border = 0
        self.rest_name = names
        for i in range(self.height):
            for j in range(self.width):
                if self[i, j] != '-':
                    self.chr_total += 1
                    self.border += self.get_blanks(i, j)
                    self.new_chrs.append((i, j))

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

    @staticmethod
    def empty(size, names):
        w, h = size
        data = []
        for _ in range(h):
            data.append(['-'] * w)
        return NameMap(data, names)

    @staticmethod
    def random(size, names):
        w, h = size
        new_map = NameMap.empty(size, names)
        name = random.choice(names)
        print(f'Chose {"".join(name):4} as random seed.', end='')
        length = len(name)
        if random.random() < 0.5:
            i = random.randint(0, h-length)
            j = random.randint(0, w-1)
            new_map[i:i+length, j] = name
        else:
            i = random.randint(0, h-1)
            j = random.randint(0, w-length)
            new_map[i, j:j+length] = name
        new_map.chr_total = length
        new_map.border = 2+2*length
        return new_map

    def adopt(self, choice):
        new_map = NameMap(seed=self)
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
        try:
            score += d*name_freq[''.join(name)]/freq_total
        except ZeroDivisionError:
            pass
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
        return len([p for p in ((i-1, j), (i+1, j),
                                (i, j-1), (i, j+1)) if is_blank(p)])

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

    def prune(self):
        for i in range(self.height-1, -1, -1):
            if set(self.data[i]) == {'-'}:
                del self.data[i]
        self.height = len(self.data)
        for j in range(self.width-1, -1, -1):
            for i in range(self.height):
                if self.data[i][j] != '-':
                    break
            else:
                for i in range(self.height):
                    del self.data[i][j]
        self.width = len(self.data[0])
        # Calc border again
        self.border = 0
        for i in range(self.height):
            for j in range(self.width):
                if self[i, j] != '-':
                    self.border += self.get_blanks(i, j)


def main(args):
    global freq_total
    size = [int(s) for s in args.random.split('x')[:2]]
    for i in range(int(args.n)):
        print(f'Attempt {i: 4}. ', end='')
        if args.seed is not None:
            name_map = NameMap(seed='seed_one.txt', names=name_pinyin.copy())
        else:
            name_map = NameMap.random(size, name_pinyin.copy())
        print('\r', end='')
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
            name_map.prune()
            print()
            if name_map.width*name_map.height <= 100:
                print('\033[33m'+'#'*20)
                print(name_map.text_plain(), name_map.height, name_map.width)
                print('#'*20+'\033[0m')
                name_map.save_plain(
                    'better/'+md5(name_map.text_plain().encode()).hexdigest())
            else:
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
    main(get_args())
    with open('freq.pkl', 'wb') as f:
        pickle.dump(name_freq, f)
