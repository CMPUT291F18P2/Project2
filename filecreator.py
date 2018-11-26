import fileparser
import re

'''  Create a file called pdates.txt; for specifics see below

    Parameters:
        dataDict (dict) - Dictionary with all information in regards to writing

    Returns:
        f1 ('_io.TextIOWrapper') - reference to the written file, probably don't
                            actually need this file

    Pdate is in the format as follows: date:aid,cat,loc
'''
def createPdate(dataDict):
    f1 = open("pdates.txt", 'w+')
    for ad in dataDict.values():
        date = ad[1][1]
        aid = ad[0][1]
        cat = ad[3][1]
        loc = ad[2][1]
        f1.write('%s:%s,%s,%s\n' % (date, aid, cat, loc))
    f1.close()
    return f1

'''  Create a file called terms.txt; for specifics see below

    Parameters:
        dataDict (dict) - Dictionary with all information in regards to writing

    Returns:
        f1 ('_io.TextIOWrapper') - reference to the written file, probably don't
                            actually need this file

    Terms is in the format as follows: (Ti or Desc Word):aid
    A lot of parsing needs to be done, and fltrWriteWords is called to do a
    lot of that parsing.  First we parse by white space, that is done in this
    function.  After we parse by white space, everything else is done by
    fltrWriteWords for all words in ti and all words in desc

'''
def createTerms(dataDict):
    f1 = open("terms.txt", 'w+')
    parsingTerms1 = "[ ]"
    for ad in dataDict.values():
        # Grab all the data we need
        tiList = filter(None, re.split(parsingTerms1, ad[4][1]))
        descList = filter(None, re.split(parsingTerms1, ad[5][1]))
        aid = ad[0][1]
        fltrWriteWords(tiList, aid, f1)
        fltrWriteWords(descList, aid, f1)
    f1.close()
    return f1

''' Filter and write the given list to a file

    Parameters:
        givenList (list) - the list to iterate through and possible parse
        aid (str) - the Ad ID used to write to file
        f1 ('_io.TextIOWrapper') - reference to file we are writing to

    Returns:
        None

    External References:
        https://stackoverflow.com/questions/21023901/how-to-split-at-all-special-characters-with-re-split
        https://stackoverflow.com/questions/1059559/split-strings-with-multiple-delimiters

    So, first we replace some characters and make everyting lower case.
    After, we remove any special characters formatted as "&#Numbers;" that
    might be in the wordself.  After removing special characters, we parse the
    word again with any special characters as we are supposed to.  Any words
    that remain with length larger than two are written to file

'''
def fltrWriteWords(givenList, aid, f1):
    # Credit to:
    # https://stackoverflow.com/questions/21023901/how-to-split-at-all-special-characters-with-re-split
    parsingTerms2 = '[`=~!@#$%^&*()+\[\]{};\'\\:"|<,./<>?]'
    for word in givenList:
        # Modify word
        word = word.lower()
        word = word.replace("&apos;", "'")
        word = word.replace("&quot;", '"')
        word = word.replace("&amp", "&")
        word = rmvSpecialChars(word)
        # Parsing word again
        # Credit given to:
        # https://stackoverflow.com/questions/1059559/split-strings-with-multiple-delimiters
        subWords = filter(None, re.split(parsingTerms2, word))
        for sWord in subWords:
            if len(sWord) > 2:
                f1.write('%s:%s\n' % (sWord, aid))
    return

''' Remove all special characters from a given word

    Parameters:
        word (str) - the string to manipulate and remove special characters in

    Returns:
        word (str) - the modified string with special characters removed

    Removes special characters in the format "&#Numbers;",
    i.e. "&#039;"

'''
def rmvSpecialChars(word):
    # Strip any special characters we may of not found
    while "&#" in word:
        sIndex = word.find("&#")
        eIndex = sIndex+3
        while word[sIndex+2:eIndex].isdigit():
            eIndex += 1
        word = word[:sIndex] + word[eIndex:]
    return word


'''  Create a file called prices.txt; for specifics see below

    Parameters:
        dataDict (dict) - Dictionary with all information in regards to writing

    Returns:
        f3 ('_io.TextIOWrapper') - reference to the written file, probably don't
                            actually need this file

    prices is in the format as follows: price:aid,cat,loc
'''
def createPrices(dataDict):
    f3 = open("prices.txt", 'w+')
    for ad in dataDict.values():
        price = ad[6][1]
        aid = ad[0][1]
        cat = ad[3][1]
        loc = ad[2][1]
        tw1 = "{}".format(price).rjust(12)
        tw = tw1 + ":{},{},{}".format(price, aid,cat,loc)
        print("tw is {}".format(tw))
        f3.write(tw)

        # f3.write('%s:%s,%s,%s\n' % (price, aid, cat, loc))
    f3.close()
    return f3

'''  Create a file called ads.txt; for specifics see below

    Parameters:
        dataDict (dict) - Dictionary with all information in regards to writing

    Returns:
        f4 ('_io.TextIOWrapper') - reference to the written file, probably don't
                            actually need this file

    Ads is in the format as follows:
        aidData:<ad><aid>aidData</aid><date>dateData</date><loc>locData</loc>
            <cat>catData</cat><ti>tiData</ti><desc>descData</desc>
            <price>priceData</price></ad>
'''
def createAds(dataDict):
    f4 = open("ads.txt", 'w+')
    for ad in dataDict.values():
        aid = ad[0][1]
        date = ad[1][1]
        loc = ad[2][1]
        cat = ad[3][1]
        ti = ad[4][1]
        desc = ad[5][1]
        price = ad[6][1]
        ws = "{}:<ad><aid>{}</aid><date>{}</date><loc>{}</loc><cat>{}</cat><ti>{}</ti><desc>{}</desc><price>{}</price></ad>\n".format(
                aid, aid, date, loc, cat, ti, desc, price)
        f4.write(ws)
    f4.close()
    return f4


def main():
    file = input('Enter name of file to be prepped: ')
    # dataDict format: 0aid, 1date, 2loc, 3cat, 4ti, 5desc, 6price
    dataDict = fileparser.parsefile(file)
    f1 = createPdate(dataDict)
    f2 = createTerms(dataDict)
    f3 = createPrices(dataDict)
    f4 = createAds(dataDict)

if __name__ == "__main__":
    main()
