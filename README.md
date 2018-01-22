# ImgurBioScan
Some people on Imgur like to add things like "screenshot this and get it to the front page" to their bios. This very basic and crappily thrown together python program attempts to find users and bios like this.

The program uses BeautifulSoup4 to help with scraping webpages and Selenium to load the pages.

To install them:
```
$ pip install requests
$ pip install beautifulsoup4
$ pip install selenium
```

At the moment it scans the front page to get current gallery images and their uploaders. I'm afraid that when the Imgur front page comes out of beta this will no longer work, so for the time being it's also being used to create a dictionary of Imgur usernames.

Any questions or concerns feel free to contact me.


