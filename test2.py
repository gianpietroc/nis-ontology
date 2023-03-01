
import spacy
from tika import parser

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


excluded_tags = stopwords.words()

nlp = spacy.load('en_core_web_sm')

def get_articles_name():
    articles = []
    #for i in range(7, 36):
    for i in range(5, 7):
        article = "\n\nArticle " + str(i)
        start = data.find(article)

        end = data.find("1.", start)
        var = data[start:end]

        var = var.replace("Article " + str(i), "")
        var = var.strip()

        articles.append(var)

    return (articles)


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

input_n = input("Enter 1 for GDPR, 2 FOR NIS:")

if (input_n == "1"):
    parsed_pdf = parser.from_file("gdpr.pdf")
    space = ""
    start_a = 5
    end_a = 20

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

        articles.append(var)

    return (articles)

articles = get_articles_name()
to_remove1 = "Official Journal of the European Union"
to_remove2 = "OJ L 241, 17.9.2015, p. 1"

#for u in range(0, len(articles)-1):
for u in range(0, 1):
    article = find_between(
        data, space + articles[u] + space, space + articles[u+1]+ space)

    articles_dict = article.split("\n\n")

    i = 0

    while i < len(articles_dict):
        print("---",articles_dict[i])
        print()
        if (to_remove1 in articles_dict[i] or to_remove2 in articles_dict[i] or articles_dict[i] == ""):
            print("Removed ---",articles_dict[i])        
            del articles_dict[i]
        else:
            i = i + 1

    i = 0
    while i < len(articles_dict) - 1:
        ch = "(a)"
        j = 1

        sentences = articles_dict[i].split(".")

        for t in range(1, len(sentences)):
            if (sentences[t] == ""):
                continue
            else:
                print("Part:", i, sentences[t])
                doc = nlp(sentences[t])

                removed = remove_tags(doc)
                final = ' '.join(map(str, removed))
                final_nlp = nlp(final)
                subject_phrase = get_subject_phrase(final_nlp)

                print("Subject", i, "-->", subject_phrase)

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

        i = i + 1
        print()