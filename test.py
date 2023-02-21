import spacy
import textacy 

import json

data = json.load(open('articles.json'))
jtopy=json.dumps(data)
dict_json=json.loads(jtopy)

excluded_tags = {"ADV"}


nlp = spacy.load('en_core_web_sm')

def remove_tags(doc):
    new_sentence = []
    for token in nlp(doc):
        if token.pos_ not in excluded_tags:
            new_sentence.append(token.text)
    return new_sentence

def get_subject_phrase(doc):
    for token in doc:
        if ("subj" in token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            return doc[start:end]

def get_object_phrase(doc):
    for token in doc:
        if ("dobj" in token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            return doc[start:end]


for i in range(len(dict_json)):
    sentence = dict_json["articles"][0].get('measures')[0].get("measure-"+str(i+1))
    
    if(dict_json["articles"][0].get('measures')[0].get('sub-measures') is not None):
        print("ok submeasures")

    doc = nlp(sentence)
    
    removed = remove_tags(doc)
    final  = ' '.join(map(str,removed))
    final_nlp = nlp(final)

    subject_phrase = get_subject_phrase(final_nlp)
    object_phrase = get_object_phrase(final_nlp)
    print("Subject ->", subject_phrase)
    print("Object ->", object_phrase)
