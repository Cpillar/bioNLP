edit by peilin xie
For bionlp

不含指代消解的nlp分析的流程：
获取pmid——从pubtator获取注释信息（pubtator）——word_count——从pubtator获取注释信息（json）——json_parse——sentence_parse——dependency_Analysis（包含依存树、主谓宾分析、最短路径分析）——get_triple——构建知识图谱
这条piplines的优点是：速度快，可以初步得到一些知识。缺点是会丢失很多由于代词而产生的知识。

指代消解的nlp分析流程为：
获取pmid——从pubtator获取注释信息（pubtator）——word_count——从pubtator获取注释信息（json）——json_parse——sentence_parse——dependency_Analysis（包含依存树、主谓宾分析、最短路径分析）——get_triple——构建知识图谱
这条piplines的优点是：可以获得较为全面的知识体系，并且可以统一主语和谓语，构建的网络更为体系化。缺点是：速度较慢，指代消解提取摘要的时间远远大于上述非指代消解流程。

websession是最后的药物知识图谱，采用的是指代消解流程。

实验的python环境为python 3.97
spacy版本2.3.7（之前位3.1.2但是由于要进行指代消解，降级为了指代消解拓展程序所需的spcay 2版本，训练集为英文的对应版本）
neuralcoref版本4.00（安装较为繁琐，需配置c++环境库）
nltk pip最新版本（训练集是通过科学上网获取的，但是应该也可以通过修改镜像或者离线安装的方法下载）
