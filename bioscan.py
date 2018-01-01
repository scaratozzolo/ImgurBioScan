'''
Created on Dec 29, 2017

@author: Scott Caratozzolo

https://github.com/scaratozzolo/ImgurBioScan
'''
import os
import time
import pickle
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pathlib import Path


browser = webdriver.Chrome('chromedriver.exe')


gallery = []
users = []

def gallery_scan():
    """Scans the front page of Imgur and pulls any href to a gallery image. Stores list of all images in a text file."""
    print('Gallery scan started at: ' + str(datetime.now()))
    
    global gallery
    is_gallery = False
    #Todo: save pickles during parsing, add way to check who has been added and who hasnt
    
    SAVED_GALLERY_PATH = Path('SaveData/saved-gallery.p')
    if SAVED_GALLERY_PATH.is_file():
        gallery = pickle.load(open('SaveData/saved-gallery.p', 'rb'))
        is_gallery = True
        
    if is_gallery:
        print(str(len(gallery)) + ' saved images loaded')
    else:
        browser.get('https://www.imgur.com')
        elm = browser.find_element_by_tag_name('html')
        for _ in range(5):
            elm.send_keys(Keys.END)
            time.sleep(1)
        
        soup = BeautifulSoup(browser.page_source, 'lxml')         #Get content from Imgur.com
         
        num_images = 0
        for link in soup.find_all('a', {'class':'image-list-link'}):     #checks all hrefs for a gallery link.
            text = link.get('href')
            gallery.append(text.strip())
            num_images += 1
            
        print(str(num_images) + ' images added')
    
    pickle.dump(gallery, open('SaveData/saved-gallery.p', 'wb'))

    
def user_scan():   
    """Scan all gallery images found in text file for Imgur users"""
    print('User scan started at: ' + str(datetime.now()))
    
    global users
    
    SAVED_USERS_PATH = Path('SaveData/saved-users.p')
    SAVED_LAST_IMAGE = Path('SaveData/last-image.p')
    if SAVED_USERS_PATH.is_file():
        users = pickle.load(open('SaveData/saved-users.p', 'rb'))
        if SAVED_LAST_IMAGE.is_file():
            last_image = pickle.load(open('SaveData/last-image.p', 'rb'))
            if gallery.index(last_image) == len(gallery)-1:
                print(str(len(users)) + ' saved users loaded')
            else:
                print(str(len(users)) + ' saved users loaded, picking up from where we left off...')
                index = gallery.index(last_image)
                num_images = len(gallery[:index])
                for image in gallery[index:]:
                    browser.get('https://www.imgur.com' + image)
                    soup = BeautifulSoup(browser.page_source, 'lxml')
                    
                    for link in soup.find_all('a', {'class':'comment-username'}):
                        text = link.get('href')
                        users.append(text.strip())
                    
                    num_images += 1    
                    if num_images % 100 == 0 and num_images != 0:
                        print('\n' + str(num_images) + '/' + str(len(gallery)) + ' images parsed at ' + str(datetime.now()))
                    elif num_images % 10 == 0:
                        print(" . ", end="")
                    pickle.dump(image, open('SaveData/last-image.p', 'wb'))
            
                    pickle.dump(users, open('SaveData/saved-users.p', 'wb')) 
        
    else:
        num_images = 0
        for image in gallery:
            browser.get('https://www.imgur.com' + image)
            soup = BeautifulSoup(browser.page_source, 'lxml')
            
            for link in soup.find_all('a', {'class':'comment-username'}):
                text = link.get('href')
                users.append(text.strip())
            
            num_images += 1    
            if num_images % 100 == 0 and num_images != 0:
                print('\n' + str(num_images) + '/' + str(len(gallery)) + ' images parsed at ' + str(datetime.now()))
            elif num_images % 10 == 0:
                print(" . ", end="")
            pickle.dump(image, open('SaveData/last-image.p', 'wb'))
    
            pickle.dump(users, open('SaveData/saved-users.p', 'wb'))
       
    repeat_users()
    
def repeat_users():
    """From a list of users pulled from text file, removes all repeat users and stores new list of users in new text file"""
    print('\nRemoving repeat users for ya...')
    
    global users
    
    users = set(pickle.load(open('SaveData/saved-users.p', 'rb')))
    
    print('All gone...')  


bios = {}           #used for bio_scan()
parsed_bios = {} 


def bio_scan():
    """Takes list of users stored in a text file and scans the contents of their Imgur profiles for their bios"""
    print('Bio scan started at: ' + str(datetime.now()) + '\n')
    
    global bios
    global parsed_bios
    global users
    
    SAVE_BIOS_PATH = Path("SaveData/bios.p")
    SAVE_PARSED_BIOS = Path("SaveData/bios.p")
    if SAVE_BIOS_PATH.is_file() and SAVE_PARSED_BIOS.is_file():
        parsed_bios = pickle.load(open( "SaveData/parsed-bios.p", "rb" ))
        bios = pickle.load(open( "SaveData/bios.p", "rb" ))
        users = pickle.load(open('SaveData/saved-users.p', 'rb'))
    
    num_users = len(users)
    num_pros = 0
           
    for username in users:
        if username.strip()[6:] in parsed_bios:     #checks if user has already been seen before
            continue
        
        browser.get('https://www.imgur.com' + username.strip())
        soup = BeautifulSoup(browser.page_source, 'lxml')        #get contents from profile page
        
        if soup.find('div', {'id' : 'account-bio'}) == None:      #checks if user has a bio
            parsed_bios[username.strip()[6:]] = 'Parsed'
        else:                                   #if user has a bio and hasn't been seen then they are added to dictionary
            parsed_bios[username.strip()[6:]] = 'Parsed'
            bios[username.strip()[6:]] = soup.find('div', {'id' : 'account-bio'}).text
        
        num_pros += 1
        if num_pros % 100 == 0 and num_pros != 0:
            print('\n' + str(num_pros) + '/' + str(num_users) + ' profiles parsed at ' + str(datetime.now()))
        elif num_pros % 10 == 0:
            print(" . ", end="")
        
        pickle.dump(parsed_bios, open( "SaveData/parsed-bios.p", "wb" ))
        pickle.dump(bios, open( "SaveData/bios.p", "wb" ))
            
    print('\n' + str(num_pros) + ' total profiles parsed')
    
    for user in bios:       #prints bio for every user found in dictionary
        if bios[user].find('front page') > -1 or bios[user].find('get it to the front page') > -1 or bios[user].find('get this to the front page') > -1 or bios[user].find('screenshot this') > -1 or bios[user].find('screencap') > -1 or bios[user].find('screen cap') > -1 or bios[user].find('screen shot') > -1:     #searches found bios for keywords
            print(user + ': \n' + bios[user] + '\n')
            print('-' * 100)
    print(str(len(bios)) + ' bios found')


def update_UsersDict():
    
    global users
    users = pickle.load(open('SaveData/saved-users.p', 'rb'))
    
    old = len(users)
    
    input_file = open('UsersDict.txt', 'r')
    for line in input_file:
        users.append(line.strip())
    input_file.close()
    
    users = set(users)
    
    new = len(users)
    
    output_file = open('UsersDict.txt', 'w')  
    for user in users:
        output_file.write(user + '\n') 
    output_file.close()
    
    print(str(new-old) + ' users added to the User Dictionary...How cool')
    
    
    
def delete_save_data():
    os.remove("SaveData/saved-gallery.p")
    os.remove("SaveData/saved-users.p")
    os.remove("SaveData/last-image.p")


def main():
    
    if not os.path.exists('SaveData'):
        os.makedirs('SaveData')
     
    print('Scanning started at: ' + str(datetime.now()))
    for i in range(1,5):
        gallery_scan()
        user_scan()
        bio_scan()
        print('Finished scan ' + str(i) + ' at: ' + str(datetime.now()) + '\n')
        time.sleep(1800)
    print('Scanning finished at: ' + str(datetime.now()))
     
    browser.quit()
    update_UsersDict()
    delete_save_data()

    
    
if __name__ == '__main__':
    main()
    