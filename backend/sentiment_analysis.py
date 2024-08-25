import sys
import json
import nltk
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
from textblob import TextBlob

# Download required NLTK data
nltk.download('wordnet')
nltk.download('punkt')

# Initialize stemmer and lemmatizer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def load_word_list(file_path):
    with open(file_path, mode='rt', encoding='utf-8') as file:
        return set(file.read().splitlines())

# Load your word lists
pos_words = load_word_list('pos_words.txt')
neg_words = load_word_list('neg_words.txt')

def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def correct_spelling(sentence):
    blob = TextBlob(sentence)
    return str(blob.correct())

def analyze_sentiment(sentence, pos_words, neg_words):
    corrected_sentence = correct_spelling(sentence)
    words = nltk.word_tokenize(corrected_sentence.lower())
    pos_count = 0
    neg_count = 0
    pos_words_input = set()
    neg_words_input = set()

    for word in words:
        stemmed_word = stemmer.stem(word)
        lemmatized_word = lemmatizer.lemmatize(word, get_wordnet_pos(word))

        if lemmatized_word in pos_words:
            pos_count += 1
            pos_words_input.add(lemmatized_word)
        elif lemmatized_word in neg_words:
            neg_count += 1
            neg_words_input.add(lemmatized_word)

    if pos_count > neg_count:
        sentiment = 'positive'
    elif neg_count > pos_count:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    return sentiment, pos_count, neg_count, pos_words_input, neg_words_input

def analyze_text(text, pos_words, neg_words):
    # Tokenize the input into sentences
    sentences = nltk.sent_tokenize(text)
    results = []

    for sentence in sentences:
        sentiment, pos_count, neg_count, pos_words_input, neg_words_input = analyze_sentiment(sentence, pos_words, neg_words)
        results.append({
            'sentence': sentence,
            'sentiment': sentiment,
            'positive_count': pos_count,
            'negative_count': neg_count,
            'positive_words': list(pos_words_input),
            'negative_words': list(neg_words_input),
        })

    return results

if __name__ == "__main__":
    # Read input text from stdin
    input_text = sys.stdin.read()
    results = analyze_text(input_text, pos_words, neg_words)
    print(json.dumps(results, indent=4))
