import spacy
import json

data = json.load(open('articles.json'))
dump = json.dumps(data)
articles_dict = json.loads(dump)

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


for i in range(len(articles_dict)):
    sentence = articles_dict["articles"][0].get(
        'measures')[0].get("measure-"+str(i+1))

    sentences = sentence.split(".")

    for s in sentences:
        doc = nlp(s)

        removed = remove_tags(doc)
        final = ' '.join(map(str, removed))
        final_nlp = nlp(final)

        subject_phrase = get_subject_phrase(final_nlp)

        print("Subject ->", subject_phrase)

        if (s == sentences[-1]):

            sub_measure_check = articles_dict["articles"][0].get(
                'measures')[0].get('sub-measures-'+str(i+1))

            if (sub_measure_check is not None):
                for j in range(len(sub_measure_check[0])):
                    var_sub = nlp(sub_measure_check[0].get(
                        'sub-measure-'+str(i+1)+chr(ord('a') + j)))

                    print("Object ->", var_sub)
        else:
            object_phrase = get_object_phrase(final_nlp)
            print("Object ->", object_phrase)
