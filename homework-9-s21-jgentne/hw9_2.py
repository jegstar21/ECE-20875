from helper import remove_punc
from nltk.stem import PorterStemmer
import numpy as np
import nltk
from nltk.corpus import stopwords


# Clean and lemmatize the contents of a document
# Takes in a file name to read in and clean
# Return a list of words, without stopwords and punctuation, and with all words stemmed
# NOTE: Do not append any directory names to doc -- assume we will give you
# a string representing a file name that will open correctly
def readAndCleanDoc(doc):

    # 1. Open document, read text into *single* string

    with open(doc, "r") as i:
        document = i.read()

    # 2. Tokenize string using nltk.tokenize.word_tokenize
    # docs = myfile.splitlines()

    nltk.download("punkt")
    token = nltk.tokenize.word_tokenize(document)

    # 3. Filter out punctuation from list of words (use remove_punc)

    filtered = remove_punc(token)

    # 4. Make the words lower case
    # 5. Filter out stopwords

    nltk.download("stopwords")
    cutoff = stopwords.words("english")
    cleaning = [words.lower() for words in filtered if words.lower() not in cutoff]

    # 6. Stem words

    stemwords = PorterStemmer()

    words = [stemwords.stem(x) for x in cleaning]

    return words


# Builds a doc-word matrix for a set of documents
# Takes in a *list of filenames*
#
# Returns 1) a doc-word matrix for the cleaned documents
# This should be a 2-dimensional numpy array, with one row per document and one
# column per word (there should be as many columns as unique words that appear
# across *all* documents. Also, Before constructing the doc-word matrix,
# you should sort the wordlist output and construct the doc-word matrix based on the sorted list
#
# Also returns 2) a list of words that should correspond to the columns in
# docword
def buildDocWordMatrix(doclist):
    # 1. Create word lists for each cleaned doc (use readAndCleanDoc)
    word = []
    doc = []

    cleaned = [readAndCleanDoc(files) for files in doclist]

    for document in cleaned:
        for words in document:
            if not (words in word):
                word.append(words)

    word.sort()

    for document in cleaned:
        vector = [0] * len(word)

        for words in document:
            i = word.index(words)
            vector[i] += 1
        doc.append(vector)

    # 2. Use these word lists to build the doc word matrix

    docword = np.array(doc)
    wordlist = word

    return docword, wordlist


# Builds a term-frequency matrix
# Takes in a doc word matrix (as built in buildDocWordMatrix)
# Returns a term-frequency matrix, which should be a 2-dimensional numpy array
# with the same shape as docword
def buildTFMatrix(docword):

    # fill in

    tf = docword / (np.sum(docword, axis=1)[:, np.newaxis])

    return tf


# Builds an inverse document frequency matrix
# Takes in a doc word matrix (as built in buildDocWordMatrix)
# Returns an inverse document frequency matrix (should be a 1xW numpy array where
# W is the number of words in the doc word matrix)
# Don't forget the log factor!
def buildIDFMatrix(docword):

    # fill in

    idf = np.log10(docword.shape[0] / (np.sum(docword > 0, axis=0)).reshape(1, -1))

    return idf


# Builds a tf-idf matrix given a doc word matrix
def buildTFIDFMatrix(docword):
    # fill in

    tfidf = buildTFMatrix(docword) * buildIDFMatrix(docword)

    return tfidf


# Find the three most distinctive words, according to TFIDF, in each document
# Input: a docword matrix, a wordlist (corresponding to columns) and a doclist
# (corresponding to rows)
# Output: a dictionary, mapping each document name from doclist to an (ordered
# list of the three most common words in each document
def findDistinctiveWords(docword, wordlist, doclist):
    distinctiveWords = {}
    # fill in
    # you might find numpy.argsort helpful for solving this problem:
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.argsort.html

    for i in range(len(doclist)):
        finalSort = np.argsort(-buildTFIDFMatrix(docword)[i, :])[:3]
        distinctiveWords[doclist[i]] = np.array(wordlist)[finalSort]

    return distinctiveWords


if __name__ == "__main__":
    from os import listdir
    from os.path import isfile, join, splitext

    ### Test Cases ###
    directory = "lecs"
    path1 = join(directory, "1_vidText.txt")
    path2 = join(directory, "2_vidText.txt")

    # Uncomment and recomment ths part where you see fit for testing purposes

    print("*** Testing readAndCleanDoc ***")
    print(readAndCleanDoc(path1)[0:5])
    print("*** Testing buildDocWordMatrix ***")
    doclist = [path1, path2]
    docword, wordlist = buildDocWordMatrix(doclist)
    print(docword.shape)
    print(len(wordlist))
    print(docword[0][0:10])
    print(wordlist[0:10])
    print(docword[1][0:10])
    print("*** Testing buildTFMatrix ***")
    tf = buildTFMatrix(docword)
    print(tf[0][0:10])
    print(tf[1][0:10])
    print(tf.sum(axis=1))
    print("*** Testing buildIDFMatrix ***")
    idf = buildIDFMatrix(docword)
    print(idf[0][0:10])
    print("*** Testing buildTFIDFMatrix ***")
    tfidf = buildTFIDFMatrix(docword)
    print(tfidf.shape)
    print(tfidf[0][0:10])
    print(tfidf[1][0:10])
    print("*** Testing findDistinctiveWords ***")
    print(findDistinctiveWords(docword, wordlist, doclist))
