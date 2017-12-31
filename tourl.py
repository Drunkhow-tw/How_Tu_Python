output = open('urls.txt','w')

urls = list()
with open('Vocab.txt','r') as data:
    vocabs = data.read().split()
    for vocab in vocabs:
        sense = 'https://dictionary.cambridge.org/dictionary/english/'+vocab.lower()+'\n'
        output.write(sense)
output.close()
with open("urls.txt") as data:
    vocabs = data.read().split()
    print(vocabs)
