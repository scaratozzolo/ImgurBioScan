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
    """Scans the front page of Imgur and pulls any href to a gallery image. Stores list of all images in a text file."""
    print('Gallery scan started at: ' + str(datetime.now()))
    
    r = requests.get("https://www.imgur.com")
    html_content = r.text
    soup = BeautifulSoup(html_content, "html.parser")   #Get content from Imgur.com
    
    users = ""
    gallery = ""
    for link in soup.find_all('a'):     #checks all hrefs for a gallery link. also checks if there are any user links.
        text = link.get('href')
        if text.find("/user") > -1:
            users += text + '\n'
        elif text.find("/gallery") > -1 and len(text) <= 16:
            if text == "/gallery/custom" or text == '/gallery/random':
                pass
            else:
                gallery += text + '\n'      
              
    output_file = open('users.txt', 'a')        #Store users in text file
    output_file.write(users)
    output_file.close()
    
    output_file = open('gallery.txt', 'w')      #Store gallery images in text file
    output_file.write(gallery)
    output_file.close()


def user_scan():
    """Scan all gallery images found in text file for Imgur users"""
    print('User scan started at: ' + str(datetime.now()))
    
    input_file = open('gallery.txt', 'r')       #get gallery image links
    
    users = ""
    for line in input_file:
        imgur = "https://www.imgur.com" + line.strip()      #get content from gallery image link
        r = requests.get(imgur)
        html_content = r.text
        soup = BeautifulSoup(html_content, "html.parser")
        for link in soup.find_all('a'):         #checks all hrefs for user links
            text = str(link.get('href'))
            if text.find("//imgur.com/user") > -1:
                if text.find("https://imgur.com") > -1:
                    pass
                else:
                    users += text[11:] + '\n'
    
    output_file = open('users.txt', 'a')        #writes users to text file
    output_file.write(users)
    output_file.close()

    input_file.close()
    repeat_users()      #calls function to remove duplicate or repat users


def repeat_users():
    """From a list of users pulled from text file, removes all repeat users and stores new list of users in new text file"""
    print('Removing repeat users...')
    
    users = []
    input_file = open('users.txt', 'r')         #Get users from first text file
    input_file2 = open('UsersDict.txt', 'r')    #get users from second text file
    
    for line in input_file:     #adds users to list
        users.append(line)
        
    for line2 in input_file2:   #adds users to list
        users.append(line2)
        
    users = set(users)          #remove duplicate users
    
    input_file.close()
    input_file2.close()
    
    output_file = open('UsersDict.txt', 'w')    #opens text file for writing
    
    for user in users:          #writes new list of individual users to text file
        output_file.write(user)
        
    output_file.close()
    
    input_file = open('users.txt', 'w')     #overwrites text file to make it blank
    input_file.close()
    
    

def bio_scan():
    """Takes list of users stored in a text file and scans the contents of their Imgur profiles for their bios"""
    print('Bio scan started at: ' + str(datetime.now()))
    input_file = open('UsersDict.txt', 'r')     #get users from file
    
    bios = {}
    parsed_bios = {}
    for user in input_file:
        imgur = 'https://www.imgur.com' + user.strip()      
        r = requests.get(imgur)
        html_content = r.text
        soup = BeautifulSoup(html_content, "html.parser")       #get contents from profile page
        
        if user.strip()[6:] in parsed_bios:     #checks if user has already been seen before
            pass
        elif soup.find('div', {'id' : 'account-bio'}) == None:      #checks if user has a bio
            parsed_bios[user.strip()[6:]] = 'Parsed'
        else:                                   #if user has a bio and hasn't been seen then they are added to dictionary
            parsed_bios[user.strip()[6:]] = 'Parsed'
            bios[user.strip()[6:]] = soup.find('div', {'id' : 'account-bio'}).text
    
    for user in bios:       #prints bio for every user found in dictionary
        if bios[user].find('front page') > -1 or bios[user].find('get it to the front page') > -1 or bios[user].find('get this to the front page') > -1 or bios[user].find('screenshot this') > -1:
            print(user + ': \n' + bios[user] + '\n')

    input_file.close()



print('Scanning started at: ' + str(datetime.now()))    
for i in range(1,101):  #run 100 times
    time.sleep(3600)    #wait 1 hour before first operation
    gallery_scan()      #performs gallery scan
    user_scan()         #performs user scan
    bio_scan()          #performs bio scan
    print('Finished scan ' + str(i) + ' at: ' + str(datetime.now()) + '\n')
print('Scanning finished at: ' + str(datetime.now()))

