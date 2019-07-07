from main import NameMap
from os import listdir

name_maps = [NameMap(seed='better\\'+i) for i in listdir('better')]
name_maps.sort(key=lambda m: 2*m.border+m.chr_total)
for name_map in name_maps:
    print(name_map.text_plain(), name_map.border, name_map.chr_total)

