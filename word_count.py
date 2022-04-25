# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import nltk
from nltk.corpus import stopwords
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# In[31]:
from nltk import word_tokenize
from nltk.corpus import stopwords # 导入停用词包
stopwords.readme().replace('\n', ' ')
stopwords.raw('english').replace('\n',' ')
def getText():
    txt = open("D:/NLP/all_ab_ty.txt", "r").read()  # 打开读取文章
    # txt = open("D:/NLP/sample.txt", "r").read()
    txt = txt.lower()  # 将大写字母转为小写
    # for ch in '!"#$%&()*+,-./:;<=>?@[\\]^_‘{|}~':
    #     txt = txt.replace(ch, " ")  # 将文本中特殊字符替换为空格
    return txt



hamletTxt = getText()
words = word_tokenize(hamletTxt)
interpunctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%',"=","also","using","-","'s","may","p","0","1","2","3","4","5","6","7","8","9","<","mesh","could",'n']   #定义标点符号列表
cutwords = [word for word in words if word not in interpunctuations]
counts = {}
for word in cutwords:
    counts[word] = counts.get(word, 0) + 1
items = list(counts.items())
tokens = [token for token in items if token[0] not in stopwords.words('english')]
tokens.sort(key=lambda x: x[1], reverse=True)
for i in range(1000):
    word, count = tokens[i]
    print("{0:<10} & {1:>5} \\\\".format(word, count))
