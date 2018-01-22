'''
Created on Dec 29, 2017

@author: Scott Caratozzolo

@version: 2.2.3

https://github.com/scaratozzolo/ImgurBioScan
'''
import sys
import os
import time
import pickle
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from builtins import int

#change version from numbers to strings and test strings

print('''
              ImgurBioScan 
         by Scott Caratozzolo
                v2.2.3
    
https://github.com/scaratozzolo/ImgurBioScan
''')

browser = webdriver.Chrome('chromedriver.exe')      #starts the chromedriver and opens the browser

r = requests.get("https://scaratozzolo.github.io/ImgurBioScan/version.json")
version_control = json.loads(r.content)

latest_version = version_control['version_number']
version_name = version_control['version_name']
version_readable = version_control['version']

version = 223
DEFAULT_SETTINGS = {'run_time_loop': 10, 'fp_loop': 10, 'sleep_time': 3600, 'only_new_bios': True, 'bio_keywords': ['front page', 'get it to the front page', 'get this to the front page', 'screen cap', 'screen shot', 'screencap', 'screenshot this'], 'version': version}

settings = {}

def load_settings():
    """Loads the setting of the program"""
    global settings
    
    PATH_TO_SETTINGS = Path('SaveData/settings.p')
    
    if PATH_TO_SETTINGS.is_file():
        settings = pickle.load(open('SaveData/settings.p', 'rb'))
    else:
        settings = DEFAULT_SETTINGS
        print('Default settings loaded')
        pickle.dump(settings, open('SaveData/settings.p', 'wb'))
        
        
    if version < 220:
        print("Version incompatible. Save data won't work. Please download latest version, {} \n https://github.com/scaratozzolo/ImgurBioScan/releases/tag/{}".format(version_readable, version_readable))
        browser.quit()
        sys.exit()
    elif int(latest_version) > version:
        print("New version available. Latest version is {} \n https://github.com/scaratozzolo/ImgurBioScan/releases/tag/{}".format(version_readable, version_readable))
        print()
    elif settings['version'] < version:
        settings['version'] = version
    
        
        
    print('Current Settings: \n')
    print('The program will run: ' + str(settings['run_time_loop']) + ' times\n')
    print('The gallery scan will go to the bottom of the front page: ' + str(settings['fp_loop']) + ' times\n')
    print('The program will wait: ' + str(settings['sleep_time']) + ' seconds between each new scan\n')
    print('Program will only print new bios: ' + str(settings['only_new_bios']) + '\n')
    print('The bio scan will look for these keywords: ', end='')
    for keyword in settings['bio_keywords']:
        if settings['bio_keywords'].index(keyword) == len(settings['bio_keywords'])-1:
            print(keyword)
        else:
            print(keyword + ', ', end='')
    
    
    while True:
        cont = input('\nWould you like to run with these settings? Type r to reset settings to default. (y/n/r)\n')
        if cont == 'y':
            break
        elif cont == 'n':
            change_settings()
            break
        elif cont == 'r':
            settings = DEFAULT_SETTINGS
            print('Settings reset to default')
            break
        else:
            print('Invalid Input')
            


def change_settings():
    """Change the settings for the program"""
    global settings
    global same_keywords
    
    #change run_time_loop setting
    while True:
        print('How many times would you like the program to run? Current setting is: ' + str(settings['run_time_loop']) + ' times. Press enter to leave current setting.')
        answer = input()
        try:
            if answer == '':
                break
            elif isinstance(int(answer), int):
                if int(answer) <= 0:
                    print('Please enter a positive whole number')
                else:
                    settings['run_time_loop'] = int(answer)
                    print('Program will run: ' + str(settings['run_time_loop']) + ' times')
                    break
            else:
                print('Please enter a positive whole number')
        except Exception:
            print('Please enter a positive whole number')
            
    #change fp_loop setting
    while True:
        print('How many times would you like the gallery scan to go to the bottom of the front page? Current setting is: ' + str(settings['fp_loop']) + ' times. Press enter to leave current setting.')
        answer = input()
        try:
            if answer == '':
                break
            elif isinstance(int(answer), int):
                if int(answer) <= 0:
                    print('Please enter a positive whole number')
                else:
                    settings['fp_loop'] = int(answer)
                    print('Gallery scan will go to bottom: ' + str(settings['fp_loop']) + ' times')
                    break
            else:
                print('Please enter a positive whole number')
        except Exception:
            print('Please enter a positive whole number')
            
    #change sleep_time setting
    while True:
        print('How long do you want to program between each scan (in seconds)? Current setting is: ' + str(settings['sleep_time']) + ' seconds. Press enter to leave current setting.')
        answer = input()
        try:
            if answer == '':
                break
            elif isinstance(int(answer), int):
                if int(answer) <= 0:
                    print('Please enter a positive whole number')
                else:
                    settings['sleep_time'] = int(answer)
                    print('Program will wait: ' + str(settings['sleep_time']) + ' seconds')
                    break
            else:
                print('Please enter a whole number')
        except Exception:
            print('Please enter a whole number')
            
            
    #change only_new_bios setting
    while True:
        print('Do you want to only print new bios (y/n)? Current setting is: ' + str(settings['only_new_bios']) + ' . Press enter to leave current setting.')
        answer = input()
        try:
            if answer == '':
                break
            elif answer == 'y':
                settings['only_new_bios'] = True
                print('Program will only print new bios')
                break
            elif answer == 'n':
                settings['only_new_bios'] = False
                print('Program will print all bios')
                break
            else:
                print("Enter 'y' or 'n' or leave blank")
        except Exception:
            print("Enter 'y' or 'n' or leave blank")
            
    #change bio_keywords setting
    keywords = []
    while True:
        print('What keywords do you want the program to search for? Current keywords are: ', end='')
        for keyword in settings['bio_keywords']:
            if settings['bio_keywords'].index(keyword) == len(settings['bio_keywords'])-1:
                print(keyword + '. Press enter to leave current keywords or when finished. Press enter after each word or phrase')
            else:
                print(keyword + ', ', end='')
        
        answer = input()
        if answer == '':
            break
        else:
            keywords.append(answer)
            while True:
                answer = input()
                if answer == '':
                    break
                else:
                    keywords.append(answer)
            
            same_keywords = False
            settings['bio_keywords'] = keywords
            break
        
    pickle.dump(settings, open('SaveData/settings.p', 'wb'))
        
    
def check_save_data():
    
    if os.path.isfile('SaveData/saved-gallery.p') or os.path.isfile('SaveData/saved-users.p') or os.path.isfile('SaveData/last-image.p'):
        print('Save data found. Would you like to load it? (y/n)')
        
        while True:
            answer = input()
            if answer == 'y':
                break
            elif answer == 'n':
                delete_save_data()
                break
            else:
                print('Invalid Input')



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
        for _ in range(settings['fp_loop']):
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
    global gallery
    
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
            
    gallery = []
       
    repeat_users()
    update_UsersDict()
    
def repeat_users():
    """From a list of users pulled from text file, removes all repeat users and stores new list of users in new text file"""
    print('\nRemoving repeat users for ya...')
    
    global users
    
    users = list(set(pickle.load(open('SaveData/saved-users.p', 'rb'))))  #removes repeat users from the current list of users and saves it back into user file
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
        parsed_bios = pickle.load(open("SaveData/parsed-bios.p", "rb" ))
        bios = pickle.load(open("SaveData/bios.p", "rb" ))
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
    

same_keywords = True

def print_bios():
    """Prints all bios with matching keywords to console and saves to bios.txt"""
    #For printed bios: printed bios with current keywords. save keywords to printed bios dictionary, check if theyre the same as current keywords, if not print everything
    global bios
    
    printed_bios = {}
    
    SAVED_PRINTED_BIOS = Path('SaveData/printed-bios.p')
    
    if SAVED_PRINTED_BIOS.is_file():
        printed_bios = pickle.load(open('SaveData/printed-bios.p', 'rb'))
    
                                            
    printed = 0
    
    for user in bios:       #prints bio for every users
        for keyword in settings['bio_keywords']:
            if bios[user].find(keyword) > -1: #searches found bios for keywords
                if settings['only_new_bios'] and same_keywords:
                    if not user in printed_bios:
                        txt = user + ': \n' + bios[user] + '\n' + '=' * 100
                        print(txt)
                        printed_bios[user] = 'Printed'
                        printed += 1
                else:
                    txt = user + ': \n' + bios[user] + '\n' + '=' * 100
                    print(txt)
                    printed_bios[user] = 'Printed'
                    printed += 1

           
    pickle.dump(printed_bios, open('SaveData/printed-bios.p', 'wb'))          
    print(str(len(bios)) + ' bios found')
    
    if settings['only_new_bios']:
        print(str(printed) + ' new bios printed')
    else:
        print(str(printed) + ' bios printed')


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
        
    load_settings()
    check_save_data()
    
     
    print('Scanning started at: ' + str(datetime.now()))    #main program 
    for i in range(settings['run_time_loop']):
        gallery_scan()
        user_scan()
        bio_scan()   
        delete_save_data()
        print('Finished scan ' + str(i+1) + ' at: ' + str(datetime.now()) + '\n')
        if i > 1:
            time.sleep(settings['sleep_time'])
    print('Scanning finished at: ' + str(datetime.now()) + '\n')
    print('='*100)
    
    print_bios() 
    browser.quit() #closes browser
    
     
    

    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Program terminated early')
        browser.quit()
    except Exception as e:
        print(str(e))
        browser.quit()
        

    