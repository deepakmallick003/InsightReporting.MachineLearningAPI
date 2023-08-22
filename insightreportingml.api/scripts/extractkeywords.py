import spacy
import re
import logging
from rake_nltk import Rake

def extract_keywords(text, num_keywords=10):

    # Clean the text
    text = re.sub('[^a-zA-Z0-9]', ' ', text)
    text = re.sub(' +', ' ', text)

    # Load the English model
    nlp = spacy.load("en_core_web_sm")

    # Process the text
    doc = nlp(text)

    # Collect noun chunks
    noun_chunks = list(doc.noun_chunks)

    # Combine noun chunks with the original text
    extended_text = " ".join(chunk.text for chunk in noun_chunks) + " " + text

    # Extract keywords using RAKE
    # Initialize RAKE with a maximum phrase length of 3 words
    rake = Rake(max_length=3)
    rake.extract_keywords_from_text(text)
    ranked_phrases = rake.get_ranked_phrases_with_scores()

    # Filter out keywords with unwanted entity types
    keywords = []
    for score, phrase in ranked_phrases:
        entities = nlp(phrase).ents
        keep_phrase = all(ent.label_ not in [
                          "PERSON", "CARDINAL", "DATE", "TIME"] for ent in entities)
        if keep_phrase:
            keywords.append(phrase.lower())
        if len(keywords) >= num_keywords:
            break

    # Combine keywords into a single string
    combined_keywords = ";".join(keyword for keyword in keywords)

    return combined_keywords
