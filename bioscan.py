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


browser = webdriver.Chrome('chromedriver.exe')      #starts the chromedriver and opens the browser


gallery = []
users = []

def gallery_scan():
    """Scans the front page of Imgur and pulls any href to a gallery image. Stores list of all images in a text file."""
    print('Gallery scan started at: ' + str(datetime.now()))
    
    global gallery
    is_gallery = False  #Default for if there is a saved gallery
    
    
    SAVED_GALLERY_PATH = Path('SaveData/saved-gallery.p')   #Path object to saved gallery file
    if SAVED_GALLERY_PATH.is_file():                        #checks if the object is a file, ie. if it exists
        gallery = pickle.load(open('SaveData/saved-gallery.p', 'rb'))   #loads the gallery pickle file containing all the links to the gallery images
        is_gallery = True   #sets gallery to true meaning there is a saved gallery
        
    if is_gallery:      #if saved gallery is loaded, prints how many images were loaded
        print(str(len(gallery)) + ' saved images loaded')
    else:   #if no saved gallery is found, browser loads imgur and scrolls to bottom specified number of times, then gathers all gallery image links and stores them in the pickle file 
        browser.get('https://www.imgur.com')        
        elm = browser.find_element_by_tag_name('html')
        for _ in range(10):
            elm.send_keys(Keys.END)
            time.sleep(1)
        
        soup = BeautifulSoup(browser.page_source, 'lxml')         #Get content from Imgur.com
         
        num_images = 0
        for link in soup.find_all('a', {'class':'image-list-link'}):     #checks all hrefs for a gallery link.
            text = link.get('href')
            gallery.append(text.strip())
            num_images += 1
            
        print(str(num_images) + ' images added')
    
    pickle.dump(gallery, open('SaveData/saved-gallery.p', 'wb')) #saving gallery images to file

    
def user_scan():   
    """Scan all gallery images found in text file for Imgur users"""
    print('User scan started at: ' + str(datetime.now()))
    
    global users
    
    SAVED_USERS_PATH = Path('SaveData/saved-users.p')   #default path for saved users file
    SAVED_LAST_IMAGE = Path('SaveData/last-image.p')    #default path for saved last image
    if SAVED_USERS_PATH.is_file():      #checks if saved user file exists
        users = list(pickle.load(open('SaveData/saved-users.p', 'rb')))   #loads saved users to users
    else:
        users = []
        
    if SAVED_LAST_IMAGE.is_file():  #if there is a last image file, the user scan continues from that last file
        last_image = pickle.load(open('SaveData/last-image.p', 'rb'))
        if gallery.index(last_image) == len(gallery)-1: #if the last image is the last image of the whole gallery, prints how many saved users were loaded
            print(str(len(users)) + ' saved users loaded')
        else:   #if last image is not last image in saved gallery then it continues scanning for users from that last image
            print(str(len(users)) + ' saved users loaded, picking up from where we left off...')
            index = gallery.index(last_image)
            num_images = len(gallery[:index])
            for image in gallery[index:]:
                browser.get('https://www.imgur.com' + image)    #opens page in browser
                soup = BeautifulSoup(browser.page_source, 'lxml')
                
                for link in soup.find_all('a', {'class':'comment-username'}):   #get all users from image page
                    text = link.get('href')
                    users.append(text.strip())
                
                num_images += 1    
                if num_images % 100 == 0 and num_images != 0: #console loading stuff
                    print('\n' + str(num_images) + '/' + str(len(gallery)) + ' images parsed at ' + str(datetime.now()))
                elif num_images % 10 == 0:
                    print(" . ", end="")
                pickle.dump(image, open('SaveData/last-image.p', 'wb')) #save last image
        
                pickle.dump(users, open('SaveData/saved-users.p', 'wb'))    #save users for that image
        
    else:
        num_images = 0
        for image in gallery:
            browser.get('https://www.imgur.com' + image)    #opens page in browser
            soup = BeautifulSoup(browser.page_source, 'lxml')
            
            for link in soup.find_all('a', {'class':'comment-username'}):   #get all users from image page
                text = link.get('href')
                users.append(text.strip())
            
            num_images += 1    
            if num_images % 100 == 0 and num_images != 0: #console loading stuff
                print('\n' + str(num_images) + '/' + str(len(gallery)) + ' images parsed at ' + str(datetime.now()))
            elif num_images % 10 == 0:
                print(" . ", end="")
            pickle.dump(image, open('SaveData/last-image.p', 'wb')) #save last image
    
            pickle.dump(users, open('SaveData/saved-users.p', 'wb'))    #save users for that image
       
    repeat_users()
    update_UsersDict()
    
def repeat_users():
    """From a list of users pulled from text file, removes all repeat users and stores new list of users in new text file"""
    print('\nRemoving repeat users for ya...')
    
    global users
    
    users = set(pickle.load(open('SaveData/saved-users.p', 'rb')))  #removes repeat users from the current list of users and saves it back into user file
    pickle.dump(users, open('SaveData/saved-users.p', 'wb'))
    
    print('All gone...')  


bios = {}           #used for bio_scan()
parsed_bios = {} 


def bio_scan():
    """Takes list of users stored in a text file and scans the contents of their Imgur profiles for their bios"""
    print('Bio scan started at: ' + str(datetime.now()) + '\n')
    
    global bios
    global parsed_bios
    global users
    
    users = pickle.load(open('SaveData/saved-users.p', 'rb'))
    
    num_pros = 0
    num_users = len(users)
    
    SAVE_BIOS_PATH = Path("SaveData/bios.p")        #path object to saved bios
    SAVE_PARSED_BIOS = Path("SaveData/bios.p")      #path object to saved parsed_bios
    if SAVE_BIOS_PATH.is_file() and SAVE_PARSED_BIOS.is_file(): #if both paths are files then they are saved to variables
        parsed_bios = pickle.load(open( "SaveData/parsed-bios.p", "rb" ))
        bios = pickle.load(open( "SaveData/bios.p", "rb" ))
        print('Picking up from where we left off...')
        num_pros = len(parsed_bios)
    
    
    
           
    for username in users:
        if username.strip()[6:] in parsed_bios:     #if user has already been parsed, skips
            continue
        
        browser.get('https://www.imgur.com' + username.strip()) #goes to profile in browser
        soup = BeautifulSoup(browser.page_source, 'lxml')        #get contents from profile page
        
        if soup.find('div', {'id' : 'account-bio'}) == None:      #checks if user has a bio
            parsed_bios[username.strip()[6:]] = 'Parsed'
        else:                                   #if user has a bio and hasn't been paresed then they are added to dictionary
            parsed_bios[username.strip()[6:]] = 'Parsed'
            bios[username.strip()[6:]] = soup.find('div', {'id' : 'account-bio'}).text
        
        num_pros += 1
        if num_pros % 1000 == 0 and num_pros != 0:  #console loading stuff
            print(' . \n' + str(num_pros) + '/' + str(num_users) + ' profiles parsed at ' + str(datetime.now()))
        elif num_pros % 100 == 0:
            print(" . ", end="")
        
        pickle.dump(parsed_bios, open( "SaveData/parsed-bios.p", "wb" ))    #saves parsed_bios to file
        pickle.dump(bios, open( "SaveData/bios.p", "wb" ))                  #saves bios to file
            
    print('\n' + str(num_pros) + ' total profiles parsed \n')
    
    
def print_bios():
    """Prints all bios with matching keywords to console and saves to bios.txt"""
    global bios
    
    printed_fp_bios = {}
    printed_nude_bios = {}
    
    SAVED_PRINTED_FP = Path('SaveData/printed-fp-bios.p')
    SAVED_PRINTED_NUDE = Path('SaveData/printed-nude-bios.p')
    
    if SAVED_PRINTED_FP.is_file() and SAVED_PRINTED_NUDE.is_file():
        printed_fp_bios = pickle.load(open('SaveData/printed-fp-bios.p', 'rb'))
        printed_nude_bios = pickle.load(open('SaveData/printed-nude-bios.p', 'rb'))
    
    printed_bios = 0
    fp = 0
    nude = 0
    for user in bios:       #prints bio for every user found in dictionary
        
        if bios[user].find('front page') > -1 or bios[user].find('get it to the front page') > -1 or bios[user].find('get this to the front page') > -1 \
         or bios[user].find('screenshot this') > -1 or bios[user].find('screencap') > -1 or bios[user].find('screen cap') > -1 or bios[user].find('screen shot') > -1: #searches found bios for keywords
            if not user in printed_fp_bios:
                txt = user + ': \n' + bios[user] + '\n' + '-' * 100
                print(txt)
                printed_fp_bios[user] = txt
                printed_bios += 1
                fp += 1
            
        if bios[user].find('nudes') > -1 or bios[user].find('nudies') > -1 or bios[user].find('NSFW') > -1 or bios[user].find('boobs') > -1:     #searches found bios for keywords
            if not user in printed_nude_bios:
                txt = user + ': \n' + bios[user] + '\n' + '-' * 100
                print(txt)
                printed_nude_bios[user] = txt
                printed_bios += 1
                nude += 1
           
    pickle.dump(printed_fp_bios, open('SaveData/printed-fp-bios.p', 'wb'))
    pickle.dump(printed_nude_bios, open('SaveData/printed-nude-bios.p', 'wb'))          
    print(str(len(bios)) + ' bios found')
    print(str(printed_bios) + ' new bios printed, ' + str(fp) + ' front page bios printed, ' + str(nude) + ' nude bios printed')


def update_UsersDict():
    """Updates the main User Dictionary with new users found"""
    
    global users
    users = list(pickle.load(open('SaveData/saved-users.p', 'rb'))) #loads new users
    
    input_file = open('UsersDict.txt', 'r')
    
    old = 0
    for line in input_file:         #adds old users to new users
        users.append(line.strip())
        old += 1
    input_file.close()
    
    users = set(users)     #removes repeats
    new = 0
    
    output_file = open('UsersDict.txt', 'w')
    user_text = '' 
    for user in users:      #writes all users back to UserDict.txt
        user_text += user + '\n'
        new += 1
    output_file.write(user_text) 
    output_file.close()
    
    print(str(new-old) + ' users added to the User Dictionary...How cool')
    pickle.dump(users, open('SaveData/saved-users.p', 'wb')) #saves all users to file
    
    
    
def delete_save_data():
    """Deletes specified files"""
    os.remove("SaveData/saved-gallery.p")
    os.remove("SaveData/saved-users.p")
    os.remove("SaveData/last-image.p")


def main():
    
    if not os.path.exists('SaveData'):      #checks for SaveData directory and creates it
        os.makedirs('SaveData')
        
    SAVED_USER_DICT = Path('UsersDict.txt')
    if not SAVED_USER_DICT.is_file():
        f = open('UsersDict.txt', 'w+')
        f.close
     
    print('Scanning started at: ' + str(datetime.now()))    #main program 
    for i in range(10):
        gallery_scan()
        user_scan()
        bio_scan()   
        delete_save_data()
        print('Finished scan ' + str(i+1) + ' at: ' + str(datetime.now()) + '\n')
        time.sleep(1800)
    print('Scanning finished at: ' + str(datetime.now()))
    
    print_bios() 
    browser.quit() #closes browser
    
     
    

    
if __name__ == '__main__':
    main()
    
