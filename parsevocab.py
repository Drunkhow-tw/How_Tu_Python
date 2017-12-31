import re
import os
from random import shuffle

if os.path.isfile('Vocabs'): os.remove('out.txt')
output = open("Vocabs.txt",'w')


with open("data.txt") as vocabs:
    vocab_lst = list()
    for line in vocabs:
        match = re.findall('\**([a-zA-Z]+) ',line)
        for vocab in match:
            vocab_lst.append(vocab)

    shuffle(vocab_lst)
    for vocab in vocab_lst:
        output.write(vocab+'\n')

output.close()
