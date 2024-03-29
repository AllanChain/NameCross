# NameCross
Make a cross maze to include everyone's name! The connection made up a whole picture, you could not split it into two parts without spliting any name.

把所有人的名字组合成一个交叉迷宫！并且整个迷宫是一个整体，你不能把迷宫分成两部分而不分裂任何一个名字。

## Perfect Example

![Demo](https://github.com/AllanChain/NameCross/raw/master/demo.gif)

**The demos are outdated after a catastrophy (see commit 875352a)**

**下面的示例内容在大灾难后已经过时（见875352a）**

As far as I can see, the mazes below is perfect (No.2 and 3 is pruned by me):

我觉得下面这几个迷宫是完美的（图2和图3是我修过的）：

```
---wdlsry  ----zgzss---  --slt-sswnp  --xklsry----  lsry----pszl
--xjxym---  -d--mpszc---  -szcxjzqyth  --sltzmh----  -wdlhrwhhzmh
cjkphrwswn  -jxjhhzlycj-  -dyjsjlycc-  jxzdjcwdlx--  -nxycsydjcw-
szlscsyjx-  -ckscsyjyjzq  -jxycsyby--  sjlycsysqyz-  --kfscyyzgz-
lyfscyylyc  -sltcjklsry-  scyjzyftyb-  szyscyy-xcg-  sjl-tcjkyth-
tybtdsszc-  xymwdlyfwhh-  tjmhgmwdl--  wqftybpjyjzy  --szysxjyjzq
-tjyjzqg--  y-dythrwn---  xklhzmh----  nythrwhhmk--  --qyblyc-h--
whh-cyyz--  c-sqyb------  -lsry-h----  -b-----h----  --y--tm--h--
zmh---b---  ----b-------  ---w-------
```

But there are also ugly ones:

但也有丑的：

```
----------x-
----------ks
---------slt
---------zx-
----xymsjlyf
wdlphrwhhycc
--szcsydjcjk
--rmscyythxj
sqyhzgzjyjhh
wyjzy---b---
nbz---------
--q---------
```

Where `-` represents an unused block. Note when you expand a character into a `1 * 1` box rather than `1 * 2`, it will be approximately a square.

其中`-`代表一个未被使用的空格。注意当你让一个字母占据`1 * 1`的格子而不是`1 * 2`时，它会大约变成一个正方形。

> Okey, I know there are two `cyy` and `sc`
> 
> 好吧，我知道它有两个`sc`和`cyy`

Other solutions can be found at `solutions/`

你能在`solution/`文件夹中找到更多解

## Usage

```shell
usage: main.py [-h] --data DATA --output OUTPUT [-n N] [--use-colorama]
               [--seed SEED | --random WxH]

optional arguments:
  -h, --help            show this help message and exit
  --data DATA, -d DATA  The name data file
  --output OUTPUT, -o OUTPUT
                        Directory to store output
  -n N                  Number of attempts
  --use-colorama, -c    Whether use colorama
  --seed SEED, -s SEED  The seed to apply
  --random WxH, -r WxH  Use random mode and specify its size, e.g. 12x12

# To run the example data set for 100 attempts and output to directory better/
python3 main.py --data data/TG2019303.txt --o better

# If you are using Windows cmd and has colorama installed, add a -c option
python3 main.py --data data/TG2019303.txt --o better -c

# To run 1000 attempts
python3 main.py --data data/TG2019303.txt --o better -n 1000

# To give it a seed file
python3 main.py --data data/TG2019303.txt --o better -s data/seed_one.txt

# To use random mode
python3 main.py --data data/TG2019303.txt --o better -r 11x11
```

```shell
usage: gif_maker.py [-h] --data DATA --input INPUT [--text TEXT] --output
                    OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  --data DATA, -d DATA  Name data file
  --input INPUT, -i INPUT
                        Input name map file
  --text TEXT, -t TEXT  Text to draw
  --output OUTPUT, -o OUTPUT
                        Output directory
                        
# To get the demo gif
gif_maker.py -d data/TG2019303.txt -i better/f465c4059c8ab543af0b0b842723ad13 -o demo.gif

# Or if you belong to another class
gif_maker.py -d data/TG2019319.txt -i better/ffffffffffffffffffffffffffffffff -t 319 -o demo.gif
```
## How It Works

It has **nothing to do with AI**, because it is just hard-coded evaluation with high weight of the often no used names, and a kiand of random choice. In general, 10 answers are found per thousand attempt. It takes 47s to complete 1000 attempts on my laptop.

它**和AI没有半毛钱关系** ， 因为它不过是预先写好的评估算法（加上对失败尝试时未被使用的名字的高权重）和随机选择。在我的笔记本上，1000次尝试会有10个解，要花47秒钟。

# ToDo

- [X] Add overall evaluation to get best output in all solutions
- [X] Different name to be the seed
- [ ] Better algorithm (maybe real ML)
- [X] Gif animation or HTML&JS interaction
