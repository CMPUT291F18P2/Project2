#from bsddb3 import db

'''Function Testing
Input:
ads.txt -   Text file with lines for each ad; a:rec | a as adid,
            rec as adrecord
Output:
ad.idx -    An index file which is a hash index on ads.txt with
            adid as key and adrecord as data
'''
def adshash(file):
    f = open(file,'r')

import subprocess

pipe = subprocess.Popen(["perl", "break.pl"],stdin = open('ads.txt','r'),stdout = subprocess.PIPE)
pipe2 = subprocess.Popen(["db_load","-T","-t","hash","ad.idx"],stdin = pipe.stdout)
pipe = subprocess.Popen(["perl", "break.pl"],stdin = open('terms.txt','r'),stdout = subprocess.PIPE)
pipe2 = subprocess.Popen(["db_load","-T","-t","btree","te.idx"],stdin = pipe.stdout)
pipe = subprocess.Popen(["perl", "break.pl"],stdin = open('pdates.txt','r'),stdout = subprocess.PIPE)
pipe2 = subprocess.Popen(["db_load","-T","-t","btree","da.idx"],stdin = pipe.stdout)
pipe = subprocess.Popen(["perl", "break.pl"],stdin = open('prices.txt','r'),stdout = subprocess.PIPE)
pipe2 = subprocess.Popen(["db_load","-T","-t","btree","pr.idx"],stdin = pipe.stdout)