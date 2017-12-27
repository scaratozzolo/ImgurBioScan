'''
Created on Dec 27, 2017

@author: Scott Caratozzolo

I pledge my honor that I have abided by the Stevens Honor System - scaratoz
'''

import requests
from bs4 import BeautifulSoup

#subs = ["https://www.imgur.com","https://imgur.com/t/The_More_You_Know", "https://imgur.com/t/Science_and_Tech", "https://imgur.com/t/Gaming"]
def gallery_scan():
    r = requests.get("https://www.imgur.com")
    html_content = r.text
    soup = BeautifulSoup(html_content, "html.parser")
    
    users = ""
    gallery = ""
    for link in soup.find_all('a'):
        text = link.get('href')
        if text.find("/user") > -1:
            users += text + '\n'
        elif text.find("/gallery") > -1 and len(text) <= 16:
            if text == "/gallery/custom" or text == '/gallery/random':
                pass
            else:
                gallery += text + '\n'      
              
    output_file = open('users.txt', 'a')
    output_file.write(users)
    output_file.close()
    
    output_file = open('gallery.txt', 'a')
    output_file.write(gallery)
    output_file.close()