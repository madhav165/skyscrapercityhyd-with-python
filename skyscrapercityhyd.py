#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
import re

global URL

def set_url():
    global URL
    URL = "http://www.skyscrapercity.com/showthread.php?t=459134&page=698"

def get_html():
    with urllib.request.urlopen(URL) as response:
        return response.read();

def get_posts(html_doc):
    soup = BeautifulSoup(html_doc, 'lxml')
    title = soup.title.string.strip()
    usernames = []
    posts = []
    tempuns = soup.findAll('a', class_='bigusername')
    for x in tempuns:
        usernames.append(x.string.strip())
    tempps = soup.findAll('div', id=re.compile('^post_message_.*'))
    for x in tempps:
        posts.append(x.text.strip())
    return (title, zip(usernames, posts))

def print_posts(title, posts):
    print("\n===== "+title+" =====\n")
    for x in posts:
        print("==="+str(x[0])+"===\n\n"+str(x[1])+"\n")

set_url()
html_doc = get_html()
title, posts = get_posts(html_doc)
print_posts(title, posts)
