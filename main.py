# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
from spacy import displacy
import spacy
import networkx as nx
import jupyter
import  matplotlib.pyplot as plt
# file=open("D:/NLP/result1(18-22).txt", "r").read()
# file=open("D:/NLP/keysentence_contain_gene_medicines.txt", "r").read()
file=open("D:/NLP/keysentence_contain_chemical_target.txt", "r").read()
spacy.prefer_gpu()
nlp = spacy.load('en_core_web_sm')
nlp.max_length = 100000000
doc=nlp(file)
pattern1=re.compile(r'.*subj')
pattern2=re.compile(r'.*obj')
countm=0
countn=0
subj=[]
obj=[]
subjword={}
objword={}

for sent in doc.sents:
    #print("\nSentence is: ",sent)
    for token in nlp(str(sent)):
        #print("Tokens are: ",token.text)
        if 'medicines' == token.text:
            if(pattern1.match(token.dep_)!=None):
                countm+=1
                print((token.head.text,token.text,token.dep_))
                if token.dep_ not in subj:
                    subj.append(token.dep_)
                if token.head.text in subjword.keys():
                    subjword[token.head.text]+=1
                else:
                    subjword.update({token.head.text:1})

            elif(pattern2.match(token.dep_)!=None):
                countn+=1
                print((token.head.text,token.text,token.dep_))
                if token.dep_ not in obj:
                    obj.append(token.dep_)
                if token.head.text in objword.keys():
                    objword[token.head.text]+=1
                else:
                    objword.update({token.head.text:1})

print('\n\n')
print('subj count:',countm,' ; obj count:',countn)  #统计medicines作为主语的次数，medicines作为宾语的次数
print('\n\n')
print('medicines subj type:',subj)  #medicines作为主语的情形
print('medicines obj type:',obj)  #medicines作为宾语的情形
print('\n\n')
subjword2 = sorted(subjword.items(), key=lambda subjword:subjword[1],reverse = True)

print('medicines subj word:',subjword2)  #medicines作为主语时，该句中与之直接相关的另一单词
print('\n\n')
objword2 = sorted(objword.items(), key=lambda objword:objword[1],reverse = True)
print('medicines obj word:',objword2)   #medicines作为宾语时，该句中与之直接相关的另一单词

# print([(token.text, token.tag_) for token in doc])
# edges=[]
# for token in doc:
#     for child in token.children:
#         edges.append(('{0}'.format(token.lower_),'{0}'.format(child.lower_)))
# graph=nx.Graph(edges)
# entity1='medicines'
# entity2='target'
# print(nx.shortest_path_length(graph,source=entity1,target=entity2))
# print(nx.shortest_path(graph,source=entity1,target=entity2))



# for token in doc:
#     print("{0}/{1} <--{2}-- {3}/{4}".format(token.text, token.tag_, token.dep_, token.head.text, token.head.tag_))
# # displacy.render(doc, style="dep",jupyter=True, options = {'distance': 90})

displacy.serve(doc,style="dep",options = {'distance': 90})
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
