
import spacy
import rdflib
from rdflib import Graph, Literal, Namespace, BNode
from rdflib.namespace import RDF, OWL, RDFS, URIRef
from rdflib.collection import Collection
from tika import parser

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

excluded_tags = stopwords.words()
nlp = spacy.load('en_core_web_sm')


def create_ontology(subj, pred, obj):

    g = Graph()
    ex = Namespace("http://nas.onto/")
    a = BNode()
    b = BNode()
    c = BNode()

    mainClass = URIRef("http://nas.onto/Article-7-Compliant")

    relation = URIRef("http://nas.onto/" + pred)
    object = URIRef("http://nas.onto/" + obj)

    g.add((a, RDF.type, OWL.Restriction))
    g.add((a, OWL.onProperty, relation))
    g.add((a, OWL.someValuesFrom, object))

    g.add((b, RDF.type, OWL.Restriction))
    g.add((b, OWL.onProperty, ex.promote))
    g.add((b, OWL.someValuesFrom, ex.memberstate))

    coll = BNode()
    Collection(g, coll, [a, b])

    g.add((c, OWL.intersectionOf, coll))
    g.add((c, RDF.type, OWL.Class))

    g.add((mainClass, OWL.equivalentClass, c))
    g.add((mainClass, RDF.type, OWL.Class))

    print(g.serialize(format="turtle"))


def find_between(s, first, last):
    start = end = ""
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return "Error"


def remove_tags(doc):
    new_sentence = []
    for token in nlp(doc):
        if token.pos_ not in excluded_tags:
            new_sentence.append(token.text)
    return new_sentence


def clean_object(obj_var):
    final = ' '.join(map(str, obj_var))
    text_tokens = word_tokenize(final)
    tokens_without_sw = [
        word for word in text_tokens if not word in stopwords.words()]

    final = ' '.join(map(str, tokens_without_sw))

    return final


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


def get_relation(doc):
    aux = False
    for i, tok in enumerate(doc):

        if (tok.text == "may" or tok.text == "shall"):
            aux = True
        if (tok.pos_ == "VERB" and aux == True and not (tok.dep_ == "advcl")):
            aux = False
            verb = tok.text
            return verb


input_n = input("Enter 1 for GDPR, 2 FOR NIS:")

if (input_n == "1"):
    parsed_pdf = parser.from_file("gdpr.pdf")
    space = ""
    start_a = 11
    end_a = 13

elif (input_n == "2"):
    parsed_pdf = parser.from_file("nis2.pdf")
    space = "\n\n"
    start_a = 7
    end_a = 36
data = parsed_pdf['content']


def get_articles_name():
    articles = []
    for i in range(start_a, end_a):
        article = "\n\nArticle " + str(i)
        start = data.find(article)

        end = data.find("1.", start)
        var = data[start:end]

        var = var.replace("Article " + str(i), "")
        var = var.strip()

        if "\n\n" in var:
            var = var[0:var.index("\n\n")]
        articles.append(var)

    return (articles)


articles_name = get_articles_name()

to_remove1 = "Official Journal of the European Union"
to_remove2 = "OJ L 241, 17.9.2015, p. 1"


# for u in range(0, len(articles)-1):
for u in range(0, 1):
    article = find_between(
        data, space + articles_name[u] + space, space + articles_name[u+1] + space)

    articles_dict = article.split("\n\n")

    i = 0

    while i < len(articles_dict):
        if (to_remove1 in articles_dict[i] or to_remove2 in articles_dict[i] or articles_dict[i] == ""):
            del articles_dict[i]
        else:
            i = i + 1

    i = 0
    # while i < len(articles_dict) - 1:
    while i < 1:
        ch = "(a)"
        j = 1

        sentences = articles_dict[i].split(".")

        # for t in range(1, len(sentences)):
        for t in range(1, 2):
            if (sentences[t] == "" or sentences[t] == " "):
                continue
            else:
                print("Part:", i, sentences[t])
                doc = nlp(sentences[t])

                removed = remove_tags(doc)
                final = ' '.join(map(str, removed))
                final_nlp = nlp(final)
                subject_phrase = get_subject_phrase(final_nlp)
                relation_phrase = get_relation(final_nlp)
                print("Subject", i, "-->", subject_phrase)
                print("Relation", i, "--->", relation_phrase)

            if (":" in sentences[t]):
                print("Submeasure list --> ", sentences[t])
                i = i + 1
                while (articles_dict[i][0:3] == ch):
                    print("SubObject", i, " -->", articles_dict[i])
                    ch = "(" + chr(ord('a') + j) + ")"
                    i = i + 1
                    j = j + 1

                i = i - 1

            else:
                object_phrase = get_object_phrase(final_nlp)
                if (object_phrase is not None):
                    obj_var = [z.text for z in object_phrase]
                    final_object = clean_object(obj_var)
                    print("Object", i, " -->", final_object)
                else:
                    print("Object --> No object")

            subject = str(subject_phrase)
            subject = subject.strip()
            subject = ''.join(subject.split())

            relation = str(relation_phrase)
            relation = relation.strip()
            relation = ''.join(relation.split())

            object = str(object_phrase)
            object = object.strip()
            object = ''.join(object.split())
            
            print(subject, "\n", relation, "\n", object)

            create_ontology(subject, relation, object)

        i = i + 1
        print()
