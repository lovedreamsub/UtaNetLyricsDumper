# -*- coding: UTF-8 -*-
import urllib.request
from urllib.parse import quote
import re
import os, sys
import locale
import gettext
from bs4 import BeautifulSoup

def getTable(url):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36")

    # Handle errors
    try:
        html = urllib.request.urlopen(req).read()
    except urllib.error.HTTPError:
        print("Wrong Input or Network Issue, please check")
        exit()

    soup = BeautifulSoup(html, "html.parser")
    contents = soup.find('tbody').findAll('tr')

    # Find search results
    tables = soup.findAll('tbody')
    tab = tables[0]
    return tab

def showSongList(tab):
    songID = []
    id = 1

    # Print song list
    print("ID\tLink\t\tTitle\t\t\t\t\tArtist")
    mat = "{:32}\t"
    for tr in tab.findAll('tr'):
        link = tr.findAll('a')[0];
        print(id, end = '\t')
        id += 1
        songID.append(re.findall('/song/(.*)/',link.get('href')))
        print(link.get('href'), end = '\t')
        for td in tr.findAll('td')[0:2]:
            print (mat.format(td.getText()), end = ''),
        print()
    return songID

def dlLyric(songID):
    # Decide which to download
    inID = int(input("Which one do you want to download? (Enter ID): "))
    submitID = songID[inID - 1]
    targetURL = "https://www.uta-net.com/song/" + submitID[0]

    # A simple COPY-AND-PASTE job
    def Html(url):
        html = urllib.request.urlopen(url)
        return html.read().decode('utf-8')

    respone = BeautifulSoup(Html(targetURL),"html.parser")
    title = respone.find("h2").getText()
    artist = respone.find("span",itemprop="byArtist name").getText()
    filetitle=artist+" - "+title
    text = respone.find("div",id="kashi_area")
    t = BeautifulSoup(str(text).replace("<br>","\n").replace("<br/>","\n"),"html.parser").getText()
    j = filetitle.find('&#039;')

    if j != -1:
        filetitle = filetitle.replace("&#039;","'")
    else:
        filetitle = filetitle

    finalname = re.sub('[/\\\\:*?<>|]', '', filetitle)
    path = sys.path[0]

    lrc = open(finalname+'.txt', 'w', encoding='utf-8')
    lrc.write(t)
    lrc.close()
    print("LRC file has been ouput to " + path + "\\" + finalname + ".txt")

if __name__ == "__main__":
    print("========================================")
    print("|        UTA-NET LYRICS FETCHER        |")
    print("|                                      |")
    print("|                 Author: JinShuai     |")
    print("|                         A1exMinatoooo|")
    print("|                         kuma         |")
    print("========================================")

    findRequest = input("Please enter a song name: ")
    url = "https://www.uta-net.com/search/?Keyword=" + quote(findRequest) + "&x=0&y=0&Aselect=2&Bselect=3"
    tb = getTable(url)
    songID = showSongList(tb)
    dlLyric(songID)