#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
import re
import os
import contextlib

global URL

def set_url():
    global URL
    lastpage = get_last_page()
    URL = "http://www.skyscrapercity.com/showthread.php?t=459134&page="+str(lastpage+1)

def get_last_page():
    location = os.path.dirname(os.path.realpath(__file__))
    with open(location+'/finalpage.txt', 'r') as f:
        return int(f.readlines()[0])

def set_last_page(last_page):
    location = os.path.dirname(os.path.realpath(__file__))
    with open(location+'/finalpage.txt', 'w') as f:
        f.write(last_page)

def get_html():
    #ua = UserAgent()
    #ua.chrome
    req = urllib.request.Request(URL,
                                headers={'User-Agent': 'Mozilla/5.0 \
                                         (X11; Linux x86_64) \
                                          AppleWebKit/537.36 (KHTML, like Gecko) \
                                          Chrome/53.0.2774.3 Safari/537.36'})
    with contextlib.closing(urllib.request.urlopen(req)) as f:
        return f.read().decode('ISO-8859-1')

def remove_attrs(soup, whitelist=tuple()):
    for tag in soup.findAll(True):
        for attr in [attr for attr in tag.attrs if attr not in whitelist]:
            del tag[attr]
    return soup

def get_posts(html_doc):
    soup = BeautifulSoup(html_doc, 'lxml')
    title = soup.title.string.strip()
    lastpage = title.split()[7]
    set_last_page (lastpage)
    usernames = []
    posts = []
    tempuns = soup.findAll('a', class_='bigusername')
    for x in tempuns:
        usernames.append(x.string.strip())
    tempps = soup.findAll('div', id=re.compile('^post_message_.*'))
    for y in tempps:
        quote = y.find('table')
        if (quote is not None):
            quote = remove_attrs(quote)
            quote_text = '\t'+quote.text.strip().replace('\n','\n\t')+'\n\n'
            y.div.decompose()
            #posts.append('**********\n\n'+str(quote_text)+'\n\n**********\n\n'+y.text.strip())
            posts.append(str(quote_text)+y.text.strip())
        else:
            posts.append (y.text.strip())
    #for x in tempps:
    #    posts.append(x.text.strip().replace("\t","").replace("\n\n\n","\n"))
    return (title, zip(usernames, posts))

def print_posts(title, posts):
    print("\n===== "+title+" =====\n")
    for x in posts:
        print("==="+str(x[0])+"===\n\n"+str(x[1])+"\n")

set_url()
html_doc = get_html()
title, posts = get_posts(html_doc)
print_posts(title, posts)
