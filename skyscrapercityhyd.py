#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
import re
import os
import contextlib
import locale

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
                                headers={'User-Agent': '''Mozilla/5.0 
                                         (X11; Linux x86_64) 
                                          AppleWebKit/537.36 (KHTML, like Gecko) 
                                          Chrome/53.0.2774.3 Safari/537.36'''})
    with contextlib.closing(urllib.request.urlopen(req)) as f:
        return f.read().decode('ISO-8859-1')

def remove_attrs(soup, whitelist=tuple()):
    for tag in soup.findAll(True):
        for attr in [attr for attr in tag.attrs if attr not in whitelist]:
            del tag[attr]
    return soup

def get_all_links(soup):
    links_list = ''
    for link_soup in soup.findAll('a'):
        link  = link_soup.get('href')
        if (link.split('.')[0] != 'showthread'):
            links_list = links_list + '\n'+ link
    return links_list

def get_posts(html_doc):
    soup = BeautifulSoup(html_doc, 'lxml')
    title = soup.title.string.strip()
    lastpage = title.split()[7]
    set_last_page (lastpage)
    usernames = []
    posts = []
    user_append = usernames.append
    post_append = posts.append
    tempuns = soup.findAll('a', class_='bigusername')
    for x in tempuns:
        user_append(x.string.strip())
    tempps = soup.findAll('div', id=re.compile('^post_message_.*'))
    for y in tempps:
        if (y.table is None):
            links_list = get_all_links(y)
            post_append (y.text.strip()+links_list)
        else:
            quotes = y.findAll('table')
            quote_text_list = ''
            for quote in quotes:
                links_list = get_all_links(quote)
                quote = remove_attrs(quote)
                quote_text="\x1B[3m"+quote.text.strip()+links_list+"\x1B[23m\n"
                y.div.decompose()
                quote_text_list+=str(quote_text)+'\n'
            post_append(quote_text_list+y.text.strip())
    return (title, zip(usernames, posts))

def print_posts(title, posts):
    print ("\033[1m"+title+"\033[0m\n")
    for x in posts:
        print("\033[1m"+str(x[0])+"\033[0m\n")
        print(str(x[1])+"\n")

set_url()
html_doc = get_html()
title, posts = get_posts(html_doc)
print_posts(title, posts)
