import pandas as pd
import json
import jsonlines
all_abstarct=open("D:/NLP/all_of_ab.txt",'a')
file=open("D:/NLP/all_of_ab.json",'r')
def get_abstact(input_file,output_file):
    for item in jsonlines.Reader(input_file):
        i=item.get('passages')[1]
        t=i.get('text')
        if(t!=''):
            output_file.write(t+'\n')

if __name__ =='__main__':
    get_abstact(file,all_abstarct)



