'''
Created on Dec 27, 2017

@author: Scott Caratozzolo

I pledge my honor that I have abided by the Stevens Honor System - scaratoz
'''
from imgur.galleryscan import gallery_scan
from imgur.userscan import user_scan
import requests
from bs4 import BeautifulSoup


def bio_scan():
    input_file = open('users.txt', 'r')
    
    bios = {}
    for user in input_file:
        imgur = 'https://www.imgur.com' + user.strip()
        r = requests.get(imgur)
        html_content = r.text
        soup = BeautifulSoup(html_content, "html.parser")
        
        if soup.find('div', {'id' : 'account-bio'}) == None:
            pass
        else:
            bios[user.strip()[6:]] = soup.find('div', {'id' : 'account-bio'}).text
    
    for user in bios:
        if bios[user].find('front page') > -1 or bios[user].find('get it to the front page') > -1 or bios[user].find('get this to the front page') > -1 or bios[user].find('screenshot this') > -1:
            print(user + ': \n' + bios[user] + '\n')

    input_file.close()


gallery_scan()
user_scan()
bio_scan()