#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
import re

global URL

def set_url():
    global URL
    lastpage = get_last_page()
    URL = "http://www.skyscrapercity.com/showthread.php?t=459134&page="+str(lastpage+1)

def get_last_page():
    with open('/home/madhav/git/skyscrapercityhyd-with-python/finalpage.txt', 'r') as f:
        return int(f.readlines()[0])

def set_last_page(last_page):
    with open('/home/madhav/git/skyscrapercityhyd-with-python/finalpage.txt', 'w') as f:
        f.write(last_page)

def get_html():
    with urllib.request.urlopen(URL) as response:
        return response.read();

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
    for x in tempps:
        posts.append(x.text.strip().replace("\t","").replace("\n\n\n","\n"))
    return (title, zip(usernames, posts))

def print_posts(title, posts):
    print("\n===== "+title+" =====\n")
    for x in posts:
        print("==="+str(x[0])+"===\n\n"+str(x[1])+"\n")

set_url()
html_doc = get_html()
title, posts = get_posts(html_doc)
print_posts(title, posts)
