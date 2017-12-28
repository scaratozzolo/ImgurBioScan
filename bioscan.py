'''
Created on Dec 27, 2017

@author: Scott Caratozzolo

I pledge my honor that I have abided by the Stevens Honor System - scaratoz
'''
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime


#subs = ["https://www.imgur.com","https://imgur.com/t/The_More_You_Know", "https://imgur.com/t/Science_and_Tech", "https://imgur.com/t/Gaming"]
def gallery_scan():
    print('Gallery scan started at: ' + str(datetime.now()))
    
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
    
    output_file = open('gallery.txt', 'w')
    output_file.write(gallery)
    output_file.close()


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
    repeat_users()


def repeat_users():
    print('Removing repeat users...')
    
    users = []
    input_file = open('users.txt', 'r')
    input_file2 = open('UsersDict.txt', 'r')
    
    for line in input_file:
        users.append(line)
        
    for line2 in input_file2:
        users.append(line2)
        
    users = set(users)
    
    input_file.close()
    input_file2.close()
    
    output_file = open('UsersDict.txt', 'w')
    
    for user in users:
        output_file.write(user)
        
    output_file.close()
    
    input_file = open('users.txt', 'w')
    input_file.close()
    
    

def bio_scan():
    print('Bio scan started at: ' + str(datetime.now()))
    input_file = open('UsersDict.txt', 'r')
    
    bios = {}
    parsed_bios = {}
    for user in input_file:
        imgur = 'https://www.imgur.com' + user.strip()
        r = requests.get(imgur)
        html_content = r.text
        soup = BeautifulSoup(html_content, "html.parser")
        
        if user.strip()[6:] in parsed_bios:
            pass
        elif soup.find('div', {'id' : 'account-bio'}) == None:
            parsed_bios[user.strip()[6:]] = 'Parsed'
        else:
            parsed_bios[user.strip()[6:]] = 'Parsed'
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

