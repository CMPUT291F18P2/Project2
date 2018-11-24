'''
    NOTE:  This file won't be included, but it can be used to make sure
    that files are the same.  I.e. make sure our version of terms is the same
    as the prof's version of terms.  Simply changed what f1 and f2 are, and
    then just run the file.  The different lines will be printed


'''


rten = "10records.txt"
rthou = "1000records.txt"
ads = "ads.txt"
adsten = "ads10records.txt"
adsthou = "ads1000records.txt"
pdates = "pdates.txt"
pdatesten = "pdates10records.txt"
pdatesthou = "pdates1000records.txt"
prices = "prices.txt"
pricesten = "prices10records.txt"
pricesthou = "prices1000records.txt"
terms = "terms.txt"
termsten = "terms10records.txt"
termsthou = "terms1000records.txt"

# Only modify these two lines, or add new files above
f1 = terms
f2 = termsthou

with open(f1) as f:
    t1 = f.read().splitlines()
    t1s = set(t1)

with open(f2) as f:
    t2 = f.read().splitlines()
    t2s = set(t2)

#in file1 but not file2
print("Only in {}".format(f1))
for diff in t1s-t2s:
    print(t1.index(diff), diff)

#in file2 but not file1
print("Only in {}".format(f2))
for diff in t2s-t1s:
    print(t2.index(diff), diff)
