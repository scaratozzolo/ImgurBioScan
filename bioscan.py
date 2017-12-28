'''
Created on Dec 27, 2017

@author: Scott Caratozzolo

I pledge my honor that I have abided by the Stevens Honor System - scaratoz
'''
from galleryscan import gallery_scan
from userscan import user_scan
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime


def bio_scan():
    print('Bio scan started at: ' + str(datetime.now()))
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



print('Scanning started at: ' + str(datetime.now()))
for i in range(1,101):
    time.sleep(3600)
    gallery_scan()
    user_scan()
    bio_scan()
    print('Finished scan ' + str(i) + ' at: ' + str(datetime.now()) + '\n')
print('Scanning finished at: ' + str(datetime.now()))
