import fileparser
import re

def createPdate(dataDict):
    f2 = open("pdates.txt", 'w+')
    for ad in dataDict.values():
        date = ad[1][1]
        aid = ad[0][1]
        cat = ad[3][1]
        loc = ad[2][1]
        f1.write('%s:%s,%s,%s\n' % (date, aid, cat, loc))
    f1.close()
    return f2

def createTerms(dataDict):

    # f1 = open("terms.txt", 'w+')
    for ad in dataDict.values():
        tiList = ad[4][1].split()
        aid = ad[0][1]
        # print(tiList)
        for word in tiList:
            if '.' in word or '/' in word:
                # pv = '/' in tiList
                # print("Found something in a word from ti: {}".format(word))
                # https://stackoverflow.com/questions/1059559/split-strings-with-multiple-delimiters
                wordList = filter(None, re.split("[.//]", word))
                # if pv: print("wordList is {}".format(wordList))
                # print("wordList is {}".format(wordList))
                for subWord in wordList:
                    # if pv: input("first word in wordList is {}".format(subWord))
                    if len(subWord) > 2 and checkWord(subWord):
                        pass

            elif len(word)>2 and checkWord(word):
                pass
                # f1.write('%s:%s\n' % (word, aid))
        descList = ad[5][1].split()
        # print(descList)
        for word in descList:
            if '.' in word or '/' in word:
                # pv = '/' in descList
                # print("Found something in a word from desc: {}".format(word))
                # https://stackoverflow.com/questions/1059559/split-strings-with-multiple-delimiters
                wordList = filter(None, re.split("[.//]", word))
                # if pv: print("wordList is {}".format(wordList))
                # print("wordList is {}".format(wordList))
                for subWord in wordList:
                    # if pv: input("first word in wordList is {}".format(subWord))
                    if len(subWord) > 2 and checkWord(subWord):
                        pass

            elif len(word)> 2 and checkWord(word):
                pass
        # f2.close()


def checkWord(word):
    while "&#" in word:
        print("Found &# in checkWord: {}".format(word))
        sIndex = word.find("&#")
        eIndex = sIndex+3
        while word[sIndex+2:eIndex].isdigit():
            eIndex += 1
        print("isolated code:{}".format(word[sIndex:eIndex]))
        word = word[:sIndex] + word[eIndex:]
        input("after editing, word is {}".format(word))
    if not word.isalnum():
        print("Found non-alnum in checkWord: {}".format(word))
        # https://stackoverflow.com/questions/1276764/stripping-everything-but-alphanumeric-chars-from-a-string-in-python
        word = re.sub(r'[^a-zA-Z0-9_-]', '', word)
        input("after editing, word is {}".format(word))
    if len(word) < 3:
        input("Found word w/ lenth of 2 or less in checkWord: {}".format(word))
    return len(word) > 2


def main():
    # dataDict format: 0aid, 1date, 2loc, 3cat, 4ti, 5desc, 6price
    file = input('Enter name of file to be prepped: ')
    dataDict = fileparser.parsefile(file)
    # f1 = createPdate(dataDict)
    f2 = createTerms(dataDict)

if __name__ == "__main__":
    main()
