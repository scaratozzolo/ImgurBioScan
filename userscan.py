'''
Created on Dec 27, 2017

@author: Scott Caratozzolo

I pledge my honor that I have abided by the Stevens Honor System - scaratoz
'''

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def user_scan():
    print('User scan started at: ' + str(datetime.now()))
    
    input_file = open('gallery.txt', 'r')
    
    users = ""
    for line in input_file:
        imgur = "https://www.imgur.com" + line.strip()
        r = requests.get(imgur)
        html_content = r.text
        soup = BeautifulSoup(html_content, "html.parser")
        for link in soup.find_all('a'):
            text = str(link.get('href'))
            if text.find("//imgur.com/user") > -1:
                if text.find("https://imgur.com") > -1:
                    pass
                else:
                    users += text[11:] + '\n'  
    
    output_file = open('users.txt', 'a')
    output_file.write(users)
    output_file.close()
        
    input_file.close()

        