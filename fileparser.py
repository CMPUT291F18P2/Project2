# -*- coding: utf-8 -*-
'''
    NOTE:   I do not recommend touching anything in this file currently
            It works, and all we need to extract from it is dataDict which is
            a dictionary that has all the information from the file we had to
            read
'''


'''  Given a line, find the next tag

    Parameters:
        line (string) - the input line read from file
        cIndex (int)  - the current index of where we are in the line
        
    Returns:
        tag (string) - the tag found by the program within the set fo tags
        cIndex (int) - the current index of where we are in the line
        tagStatus (int) - 0 if tag not found, 1 if starting tag, 2 if ending tag

    i.e. given "ad><aid>1304786670</aid><date>2018/11/07</date><loc>Calga...."
    it will return 'ad'
    Because we have processed the '<' at the start, it won't appear
    We go until we find the next '>'
    
    set of tags: ad, aid, /aid, date, /date, loc, /loc, cat, /cat, ti, /ti,
        desc, /desc, price, /price, /ads
    Can also find other tags, but are ignored
    i.e. ?xml version="1.0" encoding="UTF-8"? and ads type="array"
'''
def findTag(line, cIndex):
    ocIndex = cIndex # Original index incase this fails
    tag = list()
    startTags = set(['ad', 'aid', 'date', 'loc', 'cat', 'ti', 'desc', 'price'])
    endTags = set(['ad','/ad', '/aid', '/date', '/loc', '/cat', '/ti', '/desc', '/price'])
    while cIndex < len(line):
        char = line[cIndex]
        if char != ">":
            # append characters to the string until we find the end of the tag
            tag.append(char)
            cIndex += 1
        else:
            # create a string from a list, and then set tagStatus
            tag = ''.join(tag)
            tagStatus = 0 # tag not found
            if tag in startTags: tagStatus = 1 # starting tag
            elif tag in endTags: tagStatus = 2 # ending tag
            return (tag, cIndex, tagStatus)
    return (None, ocIndex, False)


'''  Extract data from the line until the next tag is found, and sort it

    Parameters:
        line (string) - the input line read from file
        cIndex (int)  - the current index of where we are in the line
        tag (string) - the current tag for the data type, used later
        dataDict (dict) - the dictionary where all the info is stored
        aid (string) - the current UNIQUE AD ID used as a key in the dict
        
    Returns:
        aid (string) - the new/current UNIQUE AD ID used as a key in the dict
        cIndex (int) - the current index of where we are in the line
        dataDict (dict) - the updated dictionary where all info is stored
        
    i.e. given "54321</aid><date>2018/01/01</date></ad>" w/ tag = aid
    it will return a dict of { 54321: [('aid', 54321')] }
    of course the cIndex will be something and aid will be returned as 54321
'''
def extSortData(line, tag, cIndex, dataDict, aid=None):
    data = list()
    while cIndex < len(line):
        char = line[cIndex]
        if char != "<":
            # If not the start of a new tag, return append to the data set
            data.append(char)
            cIndex += 1
        else:
            # create a string from a list, sort the data in the dict
            data = ''.join(data)
            (dataDict, aid) = sortData(data, aid, dataDict, tag)
            return (cIndex, dataDict, aid)
    return (None, dataDict, aid)


'''  Put the information into the dict based on the tag and aid

    Parameters:
        data (string) - the data we are to add to the dictionary
        tag (string) - the current tag for the data type 
        dataDict (dict) - the dictionary where all the info is stored
        aid (string) - the current UNIQUE AD ID used as a key in the dict
        
    Returns:
        aid (string) - the new/current UNIQUE AD ID used as a key in the dict
        dataDict (dict) - the updated dictionary where all info is stored
        
    I'm hoping this is pretty easy to understand, let me know if it needs
    better comments
    Dictionary format is in extSortData function documentation
'''
def sortData(data, aid, dataDict, tag):
    # Just a bunch of if else statements to add information to the dictionary
    if tag == 'aid':
        aid = data
        dataDict[data] = [('aid', data)]
    elif tag == 'date':
        prevData = dataDict[aid]
        prevData.append( ('date', data))
        dataDict[aid] = prevData
    elif tag == 'loc':
        prevData = dataDict[aid]
        prevData.append( ('loc', data))
        dataDict[aid] = prevData
    elif tag == 'cat':
        prevData = dataDict[aid]
        prevData.append( ('cat', data))
        dataDict[aid] = prevData
    elif tag == 'ti':
        prevData = dataDict[aid]
        prevData.append( ('ti', data))
        dataDict[aid] = prevData
    elif tag == 'desc':
        # TODO: Fix the string problem, as in the spec, will do later
         prevData = dataDict[aid]
         prevData.append( ('desc', data))
         dataDict[aid] = prevData
    elif tag == 'price':
         prevData = dataDict[aid]
         prevData.append( ('price', data))
         dataDict[aid] = prevData
    return (dataDict, aid)  


'''  Parse the data given in xml format as specifized by the project

    Parameters:
        file(string) - the file from which we will parse line by line
        
    Returns:
        None
        
    Once given the data, we go through it line by line, looking for tags 
    and then the data that follows, and put it into a dictionary that we can
    then use to create the files required in the later phases.
'''
def parsefile(file):
    dataDict = dict()
    # Was suggested that we use 'with open(file)' via stackoverflow so I did
    with open(file) as file:
        for line in file:
            cIndex = 0
            # A while loop is used so we can change the index in many functions
            while cIndex < len(line):
                char = line[cIndex]
                # Search for the start of a tag
                if char == "<":
                    (tag, cIndex, tagStatus) = findTag(line, cIndex+1)
                    if tag == 'ad':
                        # initialize cAID, for use in the entire ad
                        cAID = None #Because a new ID is coming!
                        pass
                    elif tagStatus == 1:                 
                        (cIndex, dataDict, cAID) = extSortData(line, tag,
                            cIndex+1, dataDict, aid=cAID)
                cIndex += 1   
    print(dataDict)
    return

def main():
    file = '1000records.txt'
    parsefile(file)

if __name__ == "__main__":
    main()