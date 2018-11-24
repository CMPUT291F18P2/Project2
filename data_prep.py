import xml.etree.ElementTree as ET

def createTerms(root):
    f1 = open("terms.txt", 'w+')
    for ad in list(root):
        terms = []
        aid = ad.find('aid').text

        ti = ad.find('ti').text
        if "&#" in ti: print(ti)
        tiList = ti.split()
        for word in tiList:
            if len(word) > 2:
                terms.append(word.lower())

        desc = ad.find('desc').text
        if "&#" in desc: print(ti)
        descList = desc.split()
        for word in descList:
            if len(word) > 2:
                terms.append(word.lower())

        for words in terms:
            f1.write('%s:%s\n' % (words, aid))
    f1.close()
    return f1

def createPdate(root):
    f2 = open("pdates.txt", 'w+')
    for ad in list(root):
        date = ad.find('date').text
        aid = ad.find('aid').text
        cat = ad.find('cat').text
        loc = ad.find('loc').text
        f2.write('%s:%s,%s,%s\n' % (date, aid, cat, loc))
    f2.close()
    return f2

def createPrices(root):
    f3 = open("prices.txt", 'w+')
    for ad in list(root):
        price = ad.find('price').text
        aid = ad.find('aid').text
        cat = ad.find('cat').text
        loc = ad.find('loc').text
        f3.write('{}%s:%s,%s,%s\n'.format('          ') % (price, aid, cat, loc))
    f3.close()
    return f3

def createAds(root):
    f4 = open("ads.txt", 'w+')
    for ad in list(root):
        aid = ad.find('aid').text
        date = ad.find('date').text
        loc = ad.find('loc').text
        cat = ad.find('cat').text
        ti = ad.find('ti').text
        desc = ad.find('desc').text
        price = ad.find('price').text
        f4.write('%s:%s,%s,%s,%s,%s,%s\n' % (aid, date, loc, cat, ti, desc, price))
    f4.close()
    return f4

def main():
    file = input('Enter name of file to be prepped: ')
    tree = ET.parse(file)
    root = tree.getroot()
    createTerms(root)
    createPdate(root)
    createPrices(root)
    createAds(root)

if __name__ == "__main__":
    main()
