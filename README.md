# NameCross
Make a cross maze to include everyone's name! The connection made up a whole picture, you could not split it into two parts without spliting any name.

把所有人的名字组合成一个交叉迷宫！并且整个迷宫是一个整体，你不能把迷宫分成两部分而不分裂任何一个名字。

## Perfect Example
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

## How It Works

It has **nothing to do with AI**, because it is just hard-coded evaluation with high weight of the often no used names, and a kiand of random choice. On average (estimated), 4 answers are found per hundred attempt, and 7 is the best score. It takes 8s to complete 100 attempts.

它**和AI没有半毛钱关系** ， 因为它不过是预先写好的评估算法（加上对失败尝试时未被使用的名字的高权重）和随机选择。平均下来，目测每100次尝试会有4个解，最好的一次有7个。~~而且，跑起来很费时间~~100次现在要花8秒钟。

# ToDo

- [ ] Add overall evaluation to get best output in all solutions
- [ ] Different name to be the seed
- [ ] Better algorithm (maybe real ML)
- [ ] Gif animation or HTML&JS interaction
