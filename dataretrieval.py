from bsddb3 import db
import filecreator
import indexing
import re

''' Initializing Berkeley databases
    Creates databases for the index files generated by indexing.py
'''
def getCursor(type):

    adsCurs = 0
    termsCurs = 1
    pdateCurs = 2
    pricesCurs = 3

    database = db.DB()


    # Database for ads
    if type == adsCurs:
        adsFile = "ad.idx"
        database.open(adsFile, None, db.DB_HASH, db.DB_CREATE)

	# Database for terms
    elif type == termsCurs:
        termsFile = "te.idx"
        #database.set_flags(db.DB_DUP)
        database.open(termsFile, None, db.DB_BTREE, db.DB_CREATE)

	# Database for pdates
    elif type == pdateCurs:
        pdatesFile = "da.idx"
        #database.set_flags(db.DB_DUP)
        database.open(pdatesFile, None, db.DB_BTREE, db.DB_CREATE)

    # Database for prices
    elif type == pricesCurs:
        pricesFile = "pr.idx"
        #database.set_flags(db.DB_DUP)
        database.open(pricesFile, None, db.DB_BTREE, db.DB_CREATE)

    return database, database.cursor()

def grammar(input,outputFormat):
# grammar to check if the user's input complies with the format. can be used to determine if its a date query, location query, etc...
    alphanumeric = "[0-9a-zA-Z_-]"
    numeric = "[0-9]"
    date = "[0-9]{4}/[0-9]{2}/[0-9]{2}"
    datePrefix = "date[\\s]*(?:=|>|<|>=|<=)"
    dateQuery = "{}[\\s]*{}".format(datePrefix, date)
    price = "{}+".format(numeric)
    pricePrefix = "price[\\s]*(?:=|>|<|>=|<=)"
    priceQuery = "{}[\\s]*{}".format(pricePrefix, price)
    location = "{}+".format(alphanumeric)
    locationPrefix = "location[\\s]*="
    locationQuery = "{}[\\s]*{}".format(locationPrefix, location)
    cat = "{}+".format(alphanumeric)
    catPrefix = "cat[\\s]*="
    catQuery = "{}[\\s]*{}".format(catPrefix, cat)
    term = "{}+".format(alphanumeric)
    termSuffix = "%"
    termQuery = "{0}{1}|{0}".format(term, termSuffix)
    expression = "{}|{}|{}|{}|{}".format(dateQuery, priceQuery, locationQuery, catQuery, termQuery)
    query = "\\A({0})(?:[\\s]({0}))*\\Z".format(expression)

    inputquery = re.match(query, input)
    if inputquery:
        id = set(allAds())
        inputexpr = re.findall(expression,inputquery.group())
        for expr in inputexpr:
            print(expr)
            if re.match(dateQuery,expr) != None:
                pass
            elif re.match(priceQuery,expr) != None:
                pass
            elif re.match(locationQuery,expr) != None:
                resultid = set(locationCheck(re.findall(location,expr)[1]))
            elif re.match(catQuery,expr) != None:
                resultid = set(catagoryCheck(re.findall(cat,expr)[1]))
            print(id,resultid)
            id = id & resultid
            print(list(id))
        ads = adSearch(id,outputFormat)
        for ad in ads:
            print(ad)
    else:
        print("Invalid query")
''' Preparing files for Berkeley DB usage
    From a record input, this function generates .txt files for ads, terms, pdates, and prices
    These .txt files are then indexed into .idx files
'''
def prepFile():
	filecreator.main()
	indexing.main()

def allAds():
    db,curs = getCursor(0)
    iter = curs.first()
    id = list()
    while iter:
        id.append(iter[0])
        iter = curs.next()
    return id


def queryBreakdown(query):
# separates operators from words regardless of spacing. still unsure of where to use it
	phrases = re.findall(r"\w+", query)
	operators = re.findall(r">=|<=|=|<|>", query)

def priceCheck(op,num):
    db,curs = getCursor(3)
    id = list()
    if op == ">":
        result = curs.set_range(num.encode("utf-8"))
        result = curs.next()
    elif op == ">=":
        result = curs.set_range(num.encode("utf-8"))
    elif op == "<":
        result = curs.set_range(max = num.encode("utf-8"))
        result = curs.next()
    elif op == "<=":
        result = curs.set_range(max = num.encode("utf-8"))
    elif op == "=":
        result = curs.set(num.encode("utf-8"))
        while(result != None):
            id.append(result[1].decode("utf-8"))
            result = curs.next_dup()
        return id
    while(result != None):
        id.append(result[1].decode("utf-8"))
        result = curs.next()
    return id

def dateCheck(op,date):
    db,curs = getCursor(2)
    id = list()
    if op == ">":
        result = curs.set_range(date.encode("utf-8"))
        result = curs.next()
    elif op == ">=":
        result = curs.set_range(date.encode("utf-8"))
    elif op == "<":
        result = curs.set_range(max = date.encode("utf-8"))
    elif op == "<=":
        result = curs.set_range(max = date.encode("uft-8"))
    elif op == "=":
        result = curs.set(date.encode("utf-8"))
        while(result != None):
            id.append(result[1].decode("utf-8"))
            result = curs.next_dup()
        return id
    while(result != None):
        id.append(result[1].decode("utf-8"))
        result = curs.next()
    return id

def locationCheck(loc):
    db,curs = getCursor(2)
    iter = curs.first()
    id = list()
    while iter:
        items = iter[1].decode("utf-8").split(",")
        if e.findall(loc,items[1]) != None:
            id.append(items[0])
        iter = curs.next()
    return id

def catagoryCheck(cat):
    db,curs = getCursor(2)
    iter = curs.first()
    id = list()
    while iter:
        items = iter[1].decode("utf-8").split(",")
        print(items[1],cat)
        print(re.findall(cat,items[1]))
        if re.findall(cat,items[1]) != None:
            id.append(items[0])
        iter = curs.next()
    return id

def termCheck(term):
    db,curs = getCursor(1)
    id = list()
    if term[-1] == '%':
        result = curs.set_range(term.encode("utf-8"))
        while (result[0].decode("utf-8")[0:len(term)-1] == term):
            id.append(result[1].decode("utf-8"))
            result = curs.next()
        return id
    else:
        result = curs.set(term.encode("utf-8"))
        while(result != None):
            id.append(result[1].decode("utf-8"))
            result = curs.next()
        return id

def adSearch(idlist,output):
    db,curs = getCursor(0)
    result = list()
    if output == "full":
        for id in idlist:
            result.append(db.get(id))
        return result
    #NOT COMPLETE NEED TO CHANGE
    elif output == "brief":
        #for id in idlist:
            #result.append(db.get(id.encode("utf-8")))
        #return result
        return 1

def main():
    prepFile()
    outputFormat = "full"

    print("Welcome to Kijiji\n")
    print('Type "help" for list of available commands\n')
    while(True):
        userInput = input("What would you like to do? ").lower()
        if (userInput == "help"):
            print("Enter query, change format, quit\n")

        elif (userInput == "enter query"):
            #queryBreakdown(input("Query: "))
            grammar(input("Query: "),outputFormat)

        elif (userInput == "change format"):
            outputFormat = input("(full/brief): output=").lower()
            print("Format has been changed to %s\n" % outputFormat)

        elif (userInput == "quit"):
            break

if __name__ == "__main__":
	main()
