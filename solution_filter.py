from hashlib import md5
from os import listdir


def process(solution):
    data = []
    for row in solution:
        row = row[:-1]
        if set(row) == {'-'}:
            continue
        data.append(list(row))
    for j in range(len(data[0])-1, -1, -1):
        for i in range(len(data)):
            if data[i][j] != '-':
                break
        else:
            for i in range(len(data)):
                del data[i][j]
    if len(data) < 11 and len(data[0]) < 11:
        text = ''.join([''.join(row)+'\n' for row in data])
        with open('better\\'+md5(text.encode()).hexdigest(), 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)



def main():
    for i in listdir('solutions'):
        with open(f'solutions\\{i}', encoding='utf-8') as f:
            process(f.readlines())


if __name__ == "__main__":
    main()
