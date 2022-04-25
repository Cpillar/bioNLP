import time
import requests
from concurrent import futures
import requests
from urllib.request import urlopen
import urllib3
from multiprocessing import Pool
import time
import requests
import urllib.request
import re

file=open("D:\\NLP\\all_of_ab.json",'a',encoding='utf_8_sig')
# url="https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/pubtator?pmids="
url="https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson?pmids="
text=open("D:\\NLP\\近7年文献PMID\\all_of_this.txt",'r')
list=text.readlines()

for n in range (100,len(list),100):
    print(n)
    t = ""
    if(n+100<=len(list)):
        for i in range(n-100,n):
            print(i)
            if i < n-1:
                m=list[i].split('\n')[0]
                t=t+m+','
            else:
                m = list[i].split('\n')[0]
                t=t+m
                turl = url + t +"&concepts=gene,chemical"
                data=urllib.request.urlopen(turl).read()
                data = data.decode("utf-8")
                print("done")
                file.write(data)

    else:
        break
file.close()


