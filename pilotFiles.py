import re

def keywordQuery(queryTerms, index):
    item = queryTerms[index]
    oIndex = index
    functions = set([">=", "<=", "=", "<", ">"])
    if item == "price":
        print("Found keyword price")
        index +=1
        n1Item = queryTerms[index]
        # print("n1Item is {}".format(n1Item))
        if n1Item in functions:
            index +=1
            n2Item = queryTerms[index]
            # print("n2Item is {}".format(n2Item))
            # Perfect formatting, so we just return
            if n2Item.isnumeric():
                # print("Returning: {} {} {}".format(item, n1Item, n2Item))
                return ([item, n1Item, n2Item], True, index)
            else: return (None, False, oIndex)
        # Looks for OPNUMBER situations, i.e. >30 or <=25 etc.
        elif not n1Item.isalpha() and not n1Item.isnumeric():
            opType = None
            for op in functions:
                if op in n1Item:
                    # Handle case where op is >= or <= and we find 1/2 ops involved
                    if op == "=" or op == "<" or op == ">" and opType == "<=" or opType == ">=":
                        continue
                    # Weird format, i.e. <40>=30 (invalid)
                    elif opType != None: return(None, False, oIndex)
                    opIdx = n1Item.find(op)
                    opType = op
            # We either found one or none
            # print("opType is {} and has length of {}".format(opType, len(opType)))
            if opType == None:
                print("ERROR:")
                return(None, False, oIndex)
            elif n1Item.find(opType) != 0:
                print("ERROR:")
                return(None, False, oIndex)
            elif n1Item[len(opType):].isnumeric():
                print("Good!")
                return([item, n1Item[0:len(opType)], n1Item[len(opType):]], True, index)
            else:
                print("ERROR:")
                return(None, False, oIndex)
        # Else, we have an error
        else:
            print("ERROR:")
            return(None, False, oIndex)

    elif item == "cat" or item == "location":
        pass
    elif item == "date":
        pass

    return (None, False, oIndex)


def queryBreakdown(query):
# separates operators from words regardless of spacing. still unsure of where to use it
	# phrases = re.findall(r"\w+", query)
	# operators = re.findall(r">=|<=|=|<|>", query)
    queryTerms = query.split()
    # print("the query Terms are {}".format(queryTerms))

    # for item in queryTerms:
    #     print("item is {}, is it alpha - {} is it numeric - {}".format(
    #         item, item.isalpha(), item.isnumeric() ))
    # print('')

    keywords = set(["price", "cat", "location", "date"])
    goodQueries = list()
    index = 0
    while index < len(queryTerms):
        item = queryTerms[index]
        if item in keywords:
            # print("{} is a keyword".format(item))
            # goodQ is a boolean, True if add to list of queries, false ignore
            # index is well, index, so we can keep iterating
            # nQuery is the query, formatted as:
            # ['keyword', 'op', 'number'] i.e. ['price', '=', '50']
            (nQuery, goodQ, index) = keywordQuery(queryTerms, index)
            print("We got returned {}, {}, {}".format(nQuery, goodQ, index))

        index += 1
    print('')

    return

def main():
    outputFormat = "full"
    print('Welcome to Kijiji')
    print('Type "help" for list of avaliable commands\n')
    while True:
        userInput = input("What would you like to do?  ").lower()
        if userInput == "help":
            print("Enter query, change format, quit")
        elif userInput == "enter query":
            queryBreakdown(input("Query: "))
        elif userInput == "change format":
            outputFormat = input("(full/brief): output=".lower())
        elif userInput == "quit":
            break
    return
if __name__ == "__main__":
	main()
