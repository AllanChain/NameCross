from hashlib import md5
from sys import argv

with open(argv[1]) as f:
    maps = f.read().split('\n\n')
    print(maps)

for i in maps:
    if not i.endswith('\n'):
        i += '\n'
    print(i)
    with open(md5(i.encode()).hexdigest(), 'w', encoding='utf-8', newline='\n') as f:
        f.write(i)
