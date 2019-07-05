# NameCross
Make a cross maze to include everyone's name!

把所有人的名字组合成一个交叉迷宫！

## Perfect Example
As far as I can see, the maze below is perfect:

我觉得下面这个迷宫是完美的：

```
------------
------------
------------
----wdlsry--
--xjxym-----
cjkphrwswn--
szlscsyjx---
lyfscyylyc--
tybtdsszc---
-tjyjzqg----
whh-cyyz----
zmh---b-----
```

Where `-` represents an unused block.

其中`-`代表一个未被使用的空格

Other solutions can be found at `solutions/`

你能在`solution/`文件夹中找到更多解

## How It Works

It has **nothing to do with AI**, because it is just hard-coded evaluation with high weight of the often no used names, and a kiand of random choice. On average (estimated), 4 answers are found per hundred attempt, and 7 is the best score. Also, it takes a lot of time to complete 100 attempts.

它**和AI没有半毛钱关系** ， 因为它不过是预先写好的评估算法（加上对失败尝试时未被使用的名字的高权重）和随机选择。平均下来，目测每100次尝试会有4个解，最好的一次有7个。而且，跑起来很费时间。

# ToDo

- [ ] Add overall evaluation to get best output in all solutions
- [ ] Different name to be the seed
- [ ] Better algorithm (maybe real ML)
- [ ] Gif animation or HTML&JS interaction
