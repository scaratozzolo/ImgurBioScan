'''
Created on Dec 29, 2017

@author: Scott
'''
from bs4 import BeautifulSoup
import sys
import urllib.request
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
import time
from datetime import datetime


class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
#         print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


def scan():
    """Scans the front page of Imgur and pulls any href to a gallery image. Stores list of all images in a text file."""
    print('Gallery scan started at: ' + str(datetime.now()))

    page_obj = {}   
    page_obj['fp'] = Page('https://www.imgur.com')
    soup = BeautifulSoup(page_obj['fp'].html, 'lxml')         #Get content from Imgur.com
    
    gallery = ""
    for link in soup.find_all('a', {'class':'image-list-link'}):     #checks all hrefs for a gallery link.
        text = link.get('href')
        gallery += text + '\n'

    output_file = open('gallery.txt', 'w')      #Store gallery images in text file
    output_file.write(gallery)
    output_file.close()
    
    
    
    """Scan all gallery images found in text file for Imgur users"""
    print('User scan started at: ' + str(datetime.now()))
    
    users = ''

    input_file = open('gallery.txt', 'r')       #get gallery image links
    for line in input_file:
        page_obj[line] = Page('https://www.imgur.com' + line.strip())
    
    for key in page_obj:
        soup = BeautifulSoup(page_obj[key].html, 'html.parser')
        for link in soup.find_all('a', {'class':'comment-username'}):
            users += link.get('href') + '\n'
            
    output_file = open('users.txt', 'a')        #writes users to text file
    output_file.write(users)
    output_file.close()
    
    input_file.close()
    repeat_users()
    
   

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
    

    
profile_obj = {}
parsed_obj = {}
bios = {}           #used for bio_scan()
parsed_bios = {}   

def bio_scan():
    """Takes list of users stored in a text file and scans the contents of their Imgur profiles for their bios"""
    print('Bio scan started at: ' + str(datetime.now()))
    
    
    input_file = open('UsersDict.txt', 'r')     #get users from file
    
    for user in input_file:
        if user in parsed_obj:
            continue
        else:
            profile_obj[user] = Page('https://www.imgur.com' + user.strip())
            parsed_obj[user] = 'Parsed'
    
    input_file.close()
           
    for username in profile_obj:
        if username.strip()[6:] in parsed_bios:     #checks if user has already been seen before
            continue
     
        soup = BeautifulSoup(profile_obj[username].html, 'lxml')        #get contents from profile page
        
        if soup.find('div', {'id' : 'account-bio'}) == None:      #checks if user has a bio
            parsed_bios[username.strip()[6:]] = 'Parsed'
        else:                                   #if user has a bio and hasn't been seen then they are added to dictionary
            parsed_bios[username.strip()[6:]] = 'Parsed'
            bios[username.strip()[6:]] = soup.find('div', {'id' : 'account-bio'}).text
    
    for user in bios:       #prints bio for every user found in dictionary
        if bios[user].find('front page') > -1 or bios[user].find('get it to the front page') > -1 or bios[user].find('get this to the front page') > -1 or bios[user].find('screenshot this') > -1:     #searches found bios for keywords
            print(user + ': \n' + bios[user] + '\n')

    

if __name__ == '__main__':

    print('Scanning started at: ' + str(datetime.now()))    
    for i in range(1,11):  #run 100 times
        scan()              #performs gallery and user scans
        bio_scan()          #performs bio scan
        print('Finished scan ' + str(i) + ' at: ' + str(datetime.now()) + '\n')
        time.sleep(3600)    #wait 1 hour before first operation
    print('Scanning finished at: ' + str(datetime.now()))         