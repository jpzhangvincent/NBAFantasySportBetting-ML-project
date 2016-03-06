import re
from bs4 import BeautifulSoup
import urllib2
import pandas
import csv

def readURLs(file="numberfirev3.txt"):
    retList = []
    with open(file) as file:
        for line in file:
            line=line.strip()
            retList.append(line)
    return retList


def scrapeTable(url,writer):
    match = re.search(r'(\d+-\d+-\d+)',url)
    date = match.group(1)
    page = urllib2.urlopen(url)

    soup = BeautifulSoup(page.read(),"lxml")
    print(url)
    table = soup.find_all('table', attrs={'class':'data-table'})
    if(len(table)>1):
        table=table[1]
    else:
        return

    table_head = table.find("thead")
    heading = table_head.find("tr").find_all("th")
    table_body = table.find("tbody",attrs={'id':'game-data'})
    rows = table_body.find_all("tr")



    for row in rows[:-1]:
        cols = row.find_all('td')
        cols = [date]+[ele.text.strip() for ele in cols]
        writer.writerow(cols)







listOfURLs= readURLs()


u_cols = ['Date','PlayerName','Position', 'Salary', 'Pts', 'R', 'A','S','T','B','FP']
writer=csv.writer(open("numberFireBestTeam.csv",'wb'))
writer.writerow(u_cols)
# scrapeTable("https://www.numberfire.com/nba/news/6962/yesterday-s-perfect-nba-dfs-lineup-sunday-11-29-15",writer)


for url in listOfURLs:
    scrapeTable(url,writer)