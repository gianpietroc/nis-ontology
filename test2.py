import spacy
from tika import parser
import re

excluded_tags = {"ADV"}

nlp = spacy.load('en_core_web_sm')

parsed_pdf = parser.from_file("nis2.pdf")
data = parsed_pdf['content']

articles = ["Jurisdiction and territoriality",
            "Registry of entities",
            "Database of domain name registration data",
            "Cybersecurity information-sharing arrangements"]

to_remove = "EN Official Journal of the European Union L 333/132 27.12.2022"


def find_between(s, first, last):
    start = end = ""
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


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


for u in range(2, 3):
    article = find_between(
        data, "\n\n" + articles[u] + "\n\n", "\n\n" + articles[u+1]+"\n\n")

    articles_dict = article.split("\n\n")

    i = 0

    while i < 10:
        if (to_remove in articles_dict[i] or articles_dict[i] == ""):
            del articles_dict[i]
        else:
            i = i + 1

    i = 0
    while i < 10:
        ch = "(a)"
        j = 1

        sentences = articles_dict[i].split(".")

        for t in range(1, len(sentences)):
            if (sentences[t] == ""):
                continue
            else:
                print("S:", i, " ", sentences[t])
            if (":" in sentences[t]):
                print("submeasure here --> ", sentences[t])
                i = i + 1
                while (articles_dict[i][0:3] == ch):
                    print("sm:", i, " sub-measure", articles_dict[i])
                    ch = "(" + chr(ord('a') + j) + ")"
                    i = i + 1
                    j = j + 1
                i = i - 1
        i = i + 1
        
