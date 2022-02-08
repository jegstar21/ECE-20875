# Arguments:
#  filename: name of file to read in
# Returns: a list of strings
# each string is one line in the file,
# and all of the characters should be lowercase, have no newlines, and have both a prefix and suffix of '__' (2 underscores)
# Notes: make sure to pad the beginning and end of the string with '_'
#       make sure the string does not contain newlines
#       make sure to convert the string to lower-case
#       so "Hello World" should be turned into "__hello world__"
# hints: https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
#       https://docs.python.org/3/library/stdtypes.html#str.splitlines
def getFormattedText(filename):
    # fill in
    lines = []

    with open(filename, "r") as x:
        for l in x.readlines():

            y = len(l)
            for_line = l.replace("\n", "")
            for_line = l.ljust(y + 1, "_")
            for_line = l.rjust(y + 1, "_")
            lines.append(for_line.lower())

    return lines


# Arguments:
#  line: a string of text
# Returns: a list of 3-character n-grams
def getNgrams(line):
    # fill in
    nGrams = []

    for i, a in enumerate(line[: len(line) - 2]):
        nGrams.append(line[i : i + 3])

    return nGrams


# Arguments:
#  filename: the filename to create an n-gram dictionary for
# Returns: a dictionary
#  where ngrams are the keys and the count of that ngram is the value.
# Notes: Remember that getFormattedText gives you a list of lines, and you want the ngrams from
#       all the lines put together.
#       You should use getFormattedText() and getNgrams() in this function.
# Hint: dict.fromkeys(l, 0) will initialize a dictionary with the keys in list l and an
#      initial value of 0
def getDict(filename):
    # fill in
    nGramDict = {}

    for a in getFormattedText(filename):
        nGrams = getNgrams(a)

        for b in nGrams:
            if b not in nGramDict:
                nGramDict[b] = 1
            else:
                nGramDict[b] += 1

    return nGramDict


# Arguments:
#   filename: the filename to generate a list of top N (most frequent n-gram, count) tuples for
#   N: the number of most frequent n-gram tuples to have in the output list.
# Returns: a list of N tuples
#   which represent the (n-gram, count) pairs that are most common in the file.
#   To clarify, the first tuple in the list represents the most common n-gram, the second tuple the second most common, etc...
# You may find the following StackOverflow post helpful for sorting a dictionary by its values:
# Also consider the dict method popitem()
# https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
def topNCommon(filename, N):
    commonN = []

    dictionary = getDict(filename)
    fix = {
        a: b for a, b in sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    }
    commonN = [(a, b) for a, b in list(fix.items())[:N]]

    return commonN


########################################## Checkpoint, can test code above before proceeding #############################################

# Arguments:
#   fileNamesList: a list of filepath strings for the different language text files to process
# Returns: a list of dictionaries
#   where each dictionary corresponds to one of the filepath strings.
#   Each dictionary in the list
#   should have keys corresponding to the n-grams, and values corresponding to the count of the n-gram
# Hint: Use functions defined in previous step.
def getAllDicts(fileNamesList):
    langDicts = []

    for name in fileNamesList:
        langDicts.append(getDict(name))

    return langDicts


# Arguments:
#   listOfDicts: A list of dictionaries where the keys are n-grams and the values are the count of the n-gram
# Returns: an alphabetically sorted list containing all of the n-grams across all of the dictionaries in listOfDicts (note, do not have duplicates n-grams)
# Notes: It is recommended to use the "set" data type when doing this (look up "set union", or "set update" for python)
#   Also, for alphabetically sorted, we mean that if you have a list of the n-grams altogether across all the languages, and you call sorted() on it, that is the output we want
def dictUnion(listOfDicts):

    unionNGrams = []
    unionNGrams = [list(a.keys()) for a in listOfDicts]
    unionNGrams = [b for c in unionNGrams for b in c]
    unionNGrams = sorted(list(set(unionNGrams)))

    return unionNGrams


# Arguments:
#   langFiles: list of filepaths of the languages to compare testFile to.
# Returns a sorted list of all the n-grams across the languages
# Note: Use previous two functions.
def getAllNGrams(langFiles):
    allNGrams = []

    totalDict = getAllDicts(langFiles)
    allNGrams = dictUnion(totalDict)

    return allNGrams


########################################## Checkpoint, can test code above before proceeding #############################################

# Arguments:
#   testFile: mystery file's filepath to determine language of
#   langFiles: list of filepaths of the languages to compare testFile to.
#   N: the number of top n-grams for comparison
# Returns the filepath of the language that has the highest number of top 10 matches that are similar to mystery file.
# Note/Hint: depending how you implemented topNCommon() earlier, you should only need to call it once per language, and doing so avoids a possible error
def compareLang(testFile, langFiles, N):
    langMatch = ""

    test = topNCommon(testFile, N)
    found = 0

    for l in langFiles:
        a = 0
        top = topNCommon(l, N)
        for b in top:
            for c in test:
                a += 1

        if a > found:
            found = a
            langMatch = l

    return langMatch


if __name__ == "__main__":
    from os import listdir
    from os.path import isfile, join, splitext

    # Test topNCommon()
    path = join("ngrams", "english.txt")
    print(topNCommon(path, 10))

    # Compile ngrams across all 6 languages and determine a mystery language
    path = "ngrams"
    fileList = [f for f in listdir(path) if isfile(join(path, f))]
    pathList = [
        join(path, f) for f in fileList if "mystery" not in f
    ]  # conditional excludes mystery.txt
    print(getAllNGrams(pathList))  # list of all n-grams spanning all languages

    testFile = join(path, "mystery.txt")
    print(compareLang(testFile, pathList, 20))  # determine language of mystery file
