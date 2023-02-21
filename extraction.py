import spacy

excluded_tags = {"ADJ", "ADV"}


nlp = spacy.load('en_core_web_sm')
sentences=["""Each Member State shall adopt a national cybersecurity strategy that provides for the strategic objectives, the resources required to achieve those objectives, and appropriate policy and regulatory measures, with a view to achieving and maintaining a high level of cybersecurity."""]

def remove_tags(doc):
    new_sentences = []
    for sentence in sentences:
        new_sentence = []
        for token in nlp(sentence):
            if token.pos_ not in excluded_tags:
                new_sentence.append(token.text)
        new_sentences.append(" ".join(new_sentence))
        return new_sentences


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

for sentence in sentences:
    doc = nlp(sentence)
    removed = remove_tags(doc)
    
    final  = ' '.join(map(str,removed))

    print(final)
    
    final = nlp(final)

    subject_phrase = get_subject_phrase(final)
    object_phrase = get_object_phrase(final)
    print("Subject ->", subject_phrase)
    print("Object ->", object_phrase)