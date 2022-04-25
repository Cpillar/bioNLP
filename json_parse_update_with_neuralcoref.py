import pandas as pd
import json
import jsonlines
import spacy
nlp=spacy.load('en_core_web_sm')
import neuralcoref
neuralcoref.add_to_pipe(nlp)
all_abstarct=open("D:/NLP/all_core.txt",'a')
file=open("D:/NLP/all_of_ab.json",'r')
def get_abstact(input_file,output_file):
    for item in jsonlines.Reader(input_file):
        i=item.get('passages')[1]
        t=i.get('text')
        if(t!=''):
            doc = nlp(t)
            print(doc._.has_coref)
            print(doc._.coref_clusters)
            m=doc._.coref_resolved
            output_file.write(m+'\n')

if __name__ =='__main__':
    get_abstact(file,all_abstarct)

