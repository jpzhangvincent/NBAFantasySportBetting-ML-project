from bs4 import BeautifulSoup
import urllib2
from datetime import date, datetime, timedelta


def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta


for result in perdelta(date(2015, 11, 16), datetime.now().date(), timedelta(days=1)):

    url = 'http://rotoguru1.com/cgi-bin/hyday.pl?game=dk&mon=%s&day=%s&year=%s&scsv=1'%(result.month,result.day,result.year)
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read(),"lxml")
    table = soup.find("pre").getText()
    # with open("%s.csv"%(result), "w") as text_file:
    #     text_file.write(table)




