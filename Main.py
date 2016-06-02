import glob
from random import shuffle
from functools import reduce
import re

PARTS = 5


def divide(l, sz):
    return [l[k: k + sz] for k in range(0, len(l), sz)]


dirs = glob.glob('./data/*')  # list
files = []  # store the dirs of all the files
for file in dirs:
    files += glob.glob(file + '/*')
# divide the files into PARTS groups randomly
shuffle(files)
groups = divide(files, int(len(files) / PARTS))

for i in range(0, PARTS):
    # step1: learning
    test = groups[i]  # take turn to be testing group
    learn = [f for f in files if f not in test]
    vocabulary = []
    marks = set()
    proportion = {}  # dict, P(ck)
    P = {}  # dict, P(wj|ck)
    for file in learn:  # file is actually file name
        content = open(file, 'rb').read().decode('utf-8', errors='ignore')
        words = re.findall(r'\w+', content)  # only words
        m = file.split('/')[2]  # m: mark
        vocabulary += words
        marks.add(m)
    for mark in marks:
        docs = [f for f in learn if f.split('/')[2] == mark]
        proportion[mark] = len(docs) / len(learn)
        # print('P(' + mark + ') = ' + str(proportion[mark]))
        text = []
        for doc in docs:
            text += [w for w in re.findall(r'\w+', open(doc, 'rb').read().decode('utf-8', errors='ignore'))]
        n = len(text)
        for word in vocabulary:
            occur = text.count(word)
            P[(word, mark)] = (occur + 1) / (n + len(vocabulary))  # key is tuple
            # print('P(' + word + '|' + mark + ') = ' + str(P[(word, mark)]))
    # step2: testing
    cnt = 0
    for file in test:
        content = open(file, 'rb').read().decode('utf-8', errors='ignore')
        words = re.findall(r'\w+', content)  # only words
        positions = [w for w in words if w in vocabulary]
        ans = max(marks, key=lambda v: proportion[v] * reduce(lambda x, y: x * y, [P[(w, v)] for w in positions]))
        print('ans:' + ans)
        if ans == file.split('/')[2]:
            cnt += 1
    print(cnt / len(test))
