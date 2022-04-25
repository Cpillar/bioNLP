from nltk.tokenize import sent_tokenize
data=open("D:/NLP/all_of_ab.txt",'r',encoding='utf_8_sig').read().lower()
file=open("D:/NLP/keysentence_contain_chemical_target_w.txt",'a')
sentence=sent_tokenize(data)
# To get all Sentences list from file
# print(sentence)
# keywords = ['covid-19','adiponectin','pannexins','tricarboxylic','cyclooxygenase-2','donepezil','rivastigmine','memantine','mutation','stress','pharmaceuticals','medicines','target','chemical']
keywords1=['gene','mutation','tau','amyloid']
keywords2=['pharmaceuticals','medicines','donepezil','rivastigmine','memantine','chemical']
keywords3=['target']
keyword4=['stress','action','mental']
keyword5=['covid-19']
result = [sen  for sen in sentence if any([key in sen for key in keywords2])]
result1=[sen  for sen in result if any([key in sen for key in keywords3])]
for i in result1:
    file.write(i+'\n')

# All Sentences containing keywords will store in result


