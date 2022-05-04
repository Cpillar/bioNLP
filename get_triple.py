import en_core_web_sm
import spacy
nlp=spacy.load('en_core_web_sm')
import os
import pandas as pd
import re
import spacy
from spacy.attrs import intify_attrs
from nltk.corpus import stopwords
'''
Referenced https://blog.csdn.net/qq_36426650/article/details/110390887

'''
all_stop_words = ['many', 'us', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
                  'today', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                  'september', 'october', 'november', 'december', 'today', 'old', 'new']
all_stop_words = sorted(list(set(all_stop_words + list(stopwords.words('english')))))

def get_tags_spacy(nlp,text):
    doc=nlp(text)
    entities_spacy=[]
    for ent in doc.ents:
        entities_spacy.append([ent.text, ent.start_char, ent.end_char, ent.label_])
    return entities_spacy

def filter_spans(spans):
    # Filter a sequence of spans so they don't contain overlaps
    get_sort_key = lambda span: (span.end - span.start, span.start)
    sorted_spans = sorted(spans, key=get_sort_key, reverse=True)
    result = []
    seen_tokens = set()
    for span in sorted_spans:
        if span.start not in seen_tokens and span.end - 1 not in seen_tokens:
            result.append(span)
            seen_tokens.update(range(span.start, span.end))
    return result

def tag_chunks(doc):
    spans = list(doc.ents) + list(doc.noun_chunks)
    spans = filter_spans(spans)
    with doc.retokenize() as retokenizer:
        string_store = doc.vocab.strings
        for span in spans:
            start = span.start
            end = span.end
            retokenizer.merge(doc[start: end], attrs=intify_attrs({'ent_type': 'ENTITY'}, string_store))

def tag_chunks_spans(doc, spans, ent_type):
    spans = filter_spans(spans)
    with doc.retokenize() as retokenizer:
        string_store = doc.vocab.strings
        for span in spans:
            start = span.start
            end = span.end
            retokenizer.merge(doc[start: end], attrs=intify_attrs({'ent_type': ent_type}, string_store))

def tagger(text):
    df_out = pd.DataFrame(columns=['Document#', 'Sentence#', 'Word#', 'Word', 'EntityType', 'EntityIOB', 'Lemma', 'POS', 'POSTag','Start', 'End', 'Dependency'])
    nlp = spacy.load("en_core_web_sm")
    document = nlp(text)
    entities_spacy = get_tags_spacy(nlp, text)
    tag_chunks(document)
    spans_change = []
    for i in range(2, len(document)):
        w_left = document[i - 2]
        w_middle = document[i - 1]
        w_right = document[i]
        if w_left.dep_ == 'attr':
            continue
        if w_left.ent_type_ == 'ENTITY' and w_right.ent_type_ == 'ENTITY' and (
                w_middle.text == 'of'):  # or w_middle.text == 'for'): #  or w_middle.text == 'with'
            spans_change.append(document[w_left.i: w_right.i + 1])
    tag_chunks_spans(document, spans_change, 'ENTITY')
    spans_change_verbs = []
    for i in range(1, len(document)):
        w_left = document[i - 1]
        w_right = document[i]
        if w_left.pos_ == 'VERB' and (w_right.pos_ == 'VERB'):
            spans_change_verbs.append(document[w_left.i: w_right.i + 1])
    tag_chunks_spans(document, spans_change_verbs, 'VERB')

    # chunk: verb + adp; verb + part
    spans_change_verbs = []
    for i in range(1, len(document)):
        w_left = document[i - 1]
        w_right = document[i]
        if w_left.pos_ == 'VERB' and (w_right.pos_ == 'ADP' or w_right.pos_ == 'PART'):
            spans_change_verbs.append(document[w_left.i: w_right.i + 1])
    tag_chunks_spans(document, spans_change_verbs, 'VERB')

    # chunk: adp + verb; part  + verb
    spans_change_verbs = []
    for i in range(1, len(document)):
        w_left = document[i - 1]
        w_right = document[i]
        if w_right.pos_ == 'VERB' and (w_left.pos_ == 'ADP' or w_left.pos_ == 'PART'):
            spans_change_verbs.append(document[w_left.i: w_right.i + 1])
    tag_chunks_spans(document, spans_change_verbs, 'VERB')

    # chunk verbs with multiple words: 'were exhibited'
    spans_change_verbs = []
    for i in range(1, len(document)):
        w_left = document[i - 1]
        w_right = document[i]
        if w_left.pos_ == 'VERB' and (w_right.pos_ == 'VERB'):
            spans_change_verbs.append(document[w_left.i: w_right.i + 1])
    tag_chunks_spans(document, spans_change_verbs, 'VERB')

    # chunk all between LRB- -RRB- (something between brackets)
    start = 0
    end = 0
    spans_between_brackets = []
    for i in range(0, len(document)):
        if ('-LRB-' == document[i].tag_ or r"(" in document[i].text):
            start = document[i].i
            continue
        if ('-RRB-' == document[i].tag_ or r')' in document[i].text):
            end = document[i].i + 1
        if (end > start and not start == 0):
            span = document[start:end]
            try:
                assert (u"(" in span.text and u")" in span.text)
            except:
                pass
                # print(span)
            spans_between_brackets.append(span)
            start = 0
            end = 0
    tag_chunks_spans(document, spans_between_brackets, 'ENTITY')

    # chunk entities  两个实体相邻时，合并
    spans_change_verbs = []
    for i in range(1, len(document)):
        w_left = document[i - 1]
        w_right = document[i]
        if w_left.ent_type_ == 'ENTITY' and w_right.ent_type_ == 'ENTITY':
            spans_change_verbs.append(document[w_left.i: w_right.i + 1])
    tag_chunks_spans(document, spans_change_verbs, 'ENTITY')

    doc_id = 1
    count_sentences = 0
    prev_dep = 'nsubj'
    for token in document:
        if (token.dep_ == 'ROOT'):
            if token.pos_ == 'VERB':
                #  将pipeline的输出保存到csv，列名：['Document#', 'Sentence#', 'Word#', 'Word', 'EntityType', 'EntityIOB', 'Lemma', 'POS', 'POSTag', 'Start', 'End', 'Dependency']
                df_out.loc[len(df_out)] = [doc_id, count_sentences, token.i, token.text, token.ent_type_,
                                           token.ent_iob_, token.lemma_, token.pos_, token.tag_, token.idx,
                                           token.idx + len(token) - 1, token.dep_]
            else:
                df_out.loc[len(df_out)] = [doc_id, count_sentences, token.i, token.text, token.ent_type_,
                                           token.ent_iob_, token.lemma_, token.pos_, token.tag_, token.idx,
                                           token.idx + len(token) - 1, prev_dep]
        else:
            df_out.loc[len(df_out)] = [doc_id, count_sentences, token.i, token.text, token.ent_type_, token.ent_iob_,
                                       token.lemma_, token.pos_, token.tag_, token.idx, token.idx + len(token) - 1,
                                       token.dep_]

        if (token.text == '.'):
            count_sentences += 1
        prev_dep = token.dep_

    return df_out

def get_predicate(s):
    pred_ids = {}
    for w, index, spo in s:
        if spo == 'predicate' and w != "'s" and w != "\"": #= 11.95
            pred_ids[index] = w
    predicates = {}
    for key, value in pred_ids.items():
        predicates[key] = value
    return predicates


def get_subjects(s, start, end, adps):
    subjects = {}
    for w, index, spo in s:
        if index >= start and index <= end:
            if 'subject' in spo or 'entity' in spo or 'object' in spo:
                subjects[index] = w
    return subjects


def get_objects(s, start, end, adps):
    objects = {}
    for w, index, spo in s:
        if index >= start and index <= end:
            if 'object' in spo or 'entity' in spo or 'subject' in spo:
                objects[index] = w
    return objects


def get_positions(s, start, end):
    adps = {}
    for w, index, spo in s:
        if index >= start and index <= end:
            if 'of' == spo or 'at' == spo:
                adps[index] = w
    return adps


def create_triples(df_text, corefs):
    ## 创建三元组
    sentences = []  # 所有句子
    aSentence = []  # 某个句子

    for index, row in df_text.iterrows():
        d_id, s_id, word_id, word, ent, ent_iob, lemma, cg_pos, pos, start, end, dep = row.items()
        if 'subj' in dep[1]:
            aSentence.append([word[1], word_id[1], 'subject'])
        elif 'ROOT' in dep[1] or 'VERB' in cg_pos[1] or pos[1] == 'IN':
            aSentence.append([word[1], word_id[1], 'predicate'])
        elif 'obj' in dep[1]:
            aSentence.append([word[1], word_id[1], 'object'])
        elif ent[1] == 'ENTITY':
            aSentence.append([word[1], word_id[1], 'entity'])
        elif word[1] == '.':
            sentences.append(aSentence)
            aSentence = []
        else:
            aSentence.append([word[1], word_id[1], pos[1]])

    relations = []
    # loose_entities = []
    for s in sentences:
        if len(s) == 0: continue
        preds = get_predicate(s)  # Get all verbs
        if preds:
            if (len(preds) == 1):
                # print("preds = ", preds)
                predicate = list(preds.values())[0]
                if (len(predicate) < 2):
                    predicate = 'is'
                # print(s)
                ents = [e[0] for e in s if e[2] == 'entity']
                # print('ents = ', ents)
                for i in range(1, len(ents)):
                    relations.append([ents[0], predicate, ents[i]])

            pred_ids = list(preds.keys())
            pred_ids.append(s[0][1])
            pred_ids.append(s[len(s) - 1][1])
            pred_ids.sort()

            for i in range(1, len(pred_ids) - 1):
                predicate = preds[pred_ids[i]]
                adps_subjs = get_positions(s, pred_ids[i - 1], pred_ids[i])
                subjs = get_subjects(s, pred_ids[i - 1], pred_ids[i], adps_subjs)
                adps_objs = get_positions(s, pred_ids[i], pred_ids[i + 1])
                objs = get_objects(s, pred_ids[i], pred_ids[i + 1], adps_objs)
                for k_s, subj in subjs.items():
                    for k_o, obj in objs.items():
                        obj_prev_id = int(k_o) - 1
                        if obj_prev_id in adps_objs:  # at, in, of
                            relations.append([subj, predicate + ' ' + adps_objs[obj_prev_id], obj])
                        else:
                            relations.append([subj, predicate, obj])

    ### Read coreferences: coreference files are TAB separated values
    coreferences = []
    for val in corefs:
        if val[0].strip() != val[1].strip():
            if len(val[0]) <= 50 and len(val[1]) <= 50:
                co_word = val[0]
                real_word = val[1].strip('[,- \'\n]*')
                real_word = re.sub("'s$", '', real_word, flags=re.UNICODE)
                if (co_word != real_word):
                    coreferences.append([co_word, real_word])
            else:
                co_word = val[0]
                real_word = ' '.join((val[1].strip('[,- \'\n]*')).split()[:7])
                real_word = re.sub("'s$", '', real_word, flags=re.UNICODE)
                if (co_word != real_word):
                    coreferences.append([co_word, real_word])

    # Resolve corefs
    triples_object_coref_resolved = []
    triples_all_coref_resolved = []
    for s, p, o in relations:
        coref_resolved = False
        for co in coreferences:
            if (s == co[0]):
                subj = co[1]
                triples_object_coref_resolved.append([subj, p, o])
                coref_resolved = True
                break
        if not coref_resolved:
            triples_object_coref_resolved.append([s, p, o])

    for s, p, o in triples_object_coref_resolved:
        coref_resolved = False
        for co in coreferences:
            if (o == co[0]):
                obj = co[1]
                triples_all_coref_resolved.append([s, p, obj])
                coref_resolved = True
                break
        if not coref_resolved:
            triples_all_coref_resolved.append([s, p, o])
    return (triples_all_coref_resolved)



def extract_triples(text):
    df_tagged= tagger(text)  # pipeline处理文本，并返回每个token的特征，以及共指消解的结果
    corefs=[]
    doc_triples = create_triples(df_tagged, corefs)
    filtered_triples = []
    print(doc_triples)
    for s, p, o in doc_triples:
        if ([s, p, o] not in filtered_triples):
            if s.lower() in all_stop_words or o.lower() in all_stop_words:
                continue
            elif s == p:
                continue
            if s.isdigit() or o.isdigit():
                continue
            if '%' in o or '%' in s:  # = 11.96
                continue
            if (len(s) < 2) or (len(o) < 2):
                continue
            if (s.islower() and len(s) < 4) or (o.islower() and len(o) < 4):
                continue
            if s == o:
                continue
            subj = s.strip('[,- :\'\"\n]*')
            pred = p.strip('[- :\'\"\n]*.')
            obj = o.strip('[,- :\'\"\n]*')

            for sw in ['a', 'an', 'the', 'its', 'their', 'his', 'her', 'our', 'all', 'old', 'new', 'latest', 'who',
                       'that', 'this', 'these', 'those']:
                subj = ' '.join(word for word in subj.split() if not word == sw)
                obj = ' '.join(word for word in obj.split() if not word == sw)
            subj = re.sub("\s\s+", " ", subj)
            obj = re.sub("\s\s+", " ", obj)

            if subj and pred and obj:
                filtered_triples.append([subj, pred, obj])

    # TRIPLES = rank_by_degree(filtered_triples)
    return filtered_triples
def filiter(triples):#过滤器，筛选出含有关键词drought和gene的三元组
    keywords=['pharmaceuticals','medicines','donepezil','rivastigmine','memantine']
    m=0
    filitedlist=[]
    for i in triples:
        temp=i[0].split(" ")
        for j in temp:
            if j in keywords:
                m = m + 1
                print(i)
                filitedlist.append(i)
    print(m)
    return filitedlist

def write_to_sif(output_file,list):#导出sif文件，用于cytoscape绘制三元组关系网络
    for i in list:
        s=i[0]
        r=i[1]
        o=i[2]
        output_file.write(s+'\t'+r+'\t'+o+'\n')
    output_file.close()

def process_all():
    text = open("D:/NLP/keysentence_contain_chemical_gene_core.txt", 'r').read()
    outfile = open("C:/Users/pillar/Desktop/graph.sif" , "a")
    triples = extract_triples(text)
     print("\n\n===============the result=============\n\n")
    print(triples)
    print("\n\n===============the filite result=============\n\n")
    filitedlist = filiter(triples)
    write_to_sif(outfile, filitedlist)

if __name__ == "__main__":
    process_all()
    print("Finished the process.")
