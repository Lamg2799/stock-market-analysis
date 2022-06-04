import pandas as pd
import re
import string
import pickle
import spacy

MODEL_FILE_PATH = './model/model.pkl'

def clean_sentence(sentence):
    """
    Cleans a sentence before it is tokenized to make tokenization processing easier.

    Args:
        sentence: A string to be pre-processed.

    Returns:
        The input sentence as a string after pre-processing.
    """
    # Remove digits
    sentence = ''.join([char for char in sentence if not char.isdigit()])
    # Remove html text
    sentence = re.sub('<[^<]+?>', '', sentence)
    
    return sentence

def spacy_tokenizer(sentence):
    """
    Utilizes spaCy to tokenize, convert words to root words, in lowercase in a sentence, while removing stop words and punctuations. 
    This function is utilized by the count vectorizer to transform sentences as a numpy array into a format that can be ingested by
    clf machine learning model.

    Args:
        sentence: A string to be tokenized.

    Returns:
        A list of tokens that pertain to a processed set of words in a sentence.
    """
    punctuations = string.punctuation
    nlp = spacy.load('en_core_web_sm')
    stop_words = spacy.lang.en.stop_words.STOP_WORDS
    # tokenize
    tokens = nlp(sentence)
    # Get root words and lowercase
    tokens = [word.lemma_.lower().strip() for word in tokens]
    # Remove stop words and punctuations
    tokens = [word for word in tokens if word not in stop_words and word not in punctuations]
    
    return tokens

def predict_sentences(sentences):
    """
    Predicts whether or not sentences are of positive or negative sentiment.

    Args:
        sentences: a list of string sentences for predictions.

    Returns:
        a list of predictions (positive or negative).
    """
    # Work done in sentiment_analysis.ipynb. Model and count vectorizer imported here.
    try:
        with open(MODEL_FILE_PATH, 'rb') as f:
            clf, count_vect = pickle.load(f)
    except FileNotFoundError:
        print(MODEL_FILE_PATH + ' was not found in this directory.')
        exit()
    except Exception as e: 
        print('An error has occurred while attempting to retrieve the model and count vectorizer: ', e)
        exit()
    sentences_cleaned = [clean_sentence(sentence) for sentence in sentences]
    sentences_series = pd.Series(sentences_cleaned)
    sentences_numpy_array = sentences_series.to_numpy()
    sentences_transformed = count_vect.transform(sentences_numpy_array)
    sentences_predictions = clf.predict(sentences_transformed)

    return sentences_predictions
