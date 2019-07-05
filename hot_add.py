from hashlib import md5
with open('D:\\Desktop\\hh.txt') as f:
    maps = f.read().split('\n\n')
    print(maps)

for i in maps:
    if not i.endswith('\n'):
        i += '\n'
    print(i)
    with open(md5(i.encode()).hexdigest(), 'w', encoding='utf-8') as f:
        f.write(i)
