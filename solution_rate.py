from main import NameMap
from os import listdir

for i in listdir('better'):
    name_map = NameMap(seed='better\\'+i)
    print(i, name_map.chr_total, name_map.border)

