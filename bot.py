from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.common.exceptions import NoSuchElementException


import os
import time
import random


options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

totalLikes = 0

hashtags = ["doodlesofinstagram", "sociallyawkward", "millenials", "comicoftheday", "inmyhead", "comicstrip", "microtales", "thoughts",
             "stories", "wordporn",
            "wordsmith", "musings"]


comments = ['Nice one',
            'I love your profile',
            'Your feed is an inspiration',
            'Just incredible',
            'This is something amazing',
            'Love your posts',
            'Looks awesome',
            'Getting inspired by you',
            'Yes!',
            'You just get me.',
            'so subtle yet...',
            'Tips hat!',
            'Just wanna say, this is beautiful',
            'how do you get these Ideas?',
            'In love with your feed',
            'Dope.',
            'Damn...',
            'you nailed it.',
            'respect.',
            'this is lovely']


class InstaBot:
    def __init__(self, username, password, xsum):
        self.username = username
        self.password = password
        self.xsum = xsum
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.driver.get('https://www.instagram.com/')
        self.login()

    def login(self):
        time.sleep(5)
        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        # time.sleep(5)
        self.driver.find_element_by_xpath("//div[contains(text(), 'Log In')]").click()

    def searchTag(self, tag):
        time.sleep(5)
        self.driver.get('https://www.instagram.com/explore/tags/' + tag + '/')

    def choosePic(self):
        # time.sleep(5)
        pageno = random.randint(1, 2)
        if(pageno == 1):
            xcoord = random.randint(1, 3)
        elif(pageno == 2):
            xcoord = random.randint(1, 15)

        ycoord = random.randint(1, 3)

        self.xsum += xcoord
        
        self.scroll_down(xcoord)
        time.sleep(5)


        picPath1 = '//*[@id="react-root"]/section/main/article/div[' + str(pageno) + ']/div/div/div[' + \
            str(xcoord) + ']/div[' + str(ycoord) + ']'


        picPath2 = '//*[@id="react-root"]/section/main/article/div[' + str(pageno) + ']/div/div[' + \
            str(xcoord) + ']/div[' + str(ycoord) + ']'

        self.likepic(picPath1, picPath2)

    def likepic(self, picpath1, picpath2):

        try:
            time.sleep(7)
            self.driver.find_element_by_xpath(picpath1).click()

        except NoSuchElementException:
            time.sleep(7)
            self.driver.find_element_by_xpath(picpath2).click()

        # self.driver.find_element_by_xpath(picpath).click()

        # time.sleep(5)

        if(self.checkLike() == True):
            # time.sleep(7)
            self.driver.find_element_by_xpath(
                '/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button').click()
            
            self.checkComment()
        else:
            self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/button').click()


    def commentpic(self):

        time.sleep(5)
        commentArea = self.driver.find_element_by_class_name('Ypffh')
        commentArea.click()

        time.sleep(5)
        commentArea = self.driver.find_element_by_class_name('Ypffh')
        commentArea.click()

        commentno = random.randint(0, len(comments))
        commentArea.send_keys(comments[commentno])
        # time.sleep(5)
        self.driver.find_element_by_xpath(
            '/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/button').click()


    def follow(self):
        # time.sleep(5)

        try:
            self.driver.find_element_by_xpath('//button[text()="follow"]').click()
            # time.sleep(5)
            self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/button').click()
            # time.sleep(5) 
        except NoSuchElementException:
            self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/button').click()
            # time.sleep(5)        
        

    
    def checkComment(self):
        # time.sleep(5)
        commcnt = len(self.driver.find_elements_by_xpath('//button[text()="Reply"]'))
        if(commcnt < 5):
            self.commentpic()

        self.follow()


    def checkLike(self):
        time.sleep(5)

        likeno = 0

        try:
            if(self.driver.find_element_by_xpath(
                '/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/span/text()') == ' views'):
                likeno = 0

        except NoSuchElementException:

            if(self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div/button').text == '1 like'):
                likeno = 1

            elif(self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div/button').text == 'like this'):
                likeno = 0

            else:
                likeno = int(self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div/button/span').text.replace(',', ''))


        
            
        # time.sleep(5)
        heart = self.driver.find_element_by_css_selector("[aria-label=Like]")
        if(likeno < 500 and heart.get_attribute("fill") == "#262626"):
            return True
        else:
            return False

    def scroll_down(self, xcoord):

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        if(self.xsum < 25):
            while xcoord + 2 > 0:
                xcoord = xcoord - 1
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = self.driver.execute_script(
                    "return document.body.scrollHeight")

                if new_height == last_height:
                    break
                last_height = new_height

    
    # def checkVisit(self):
    #     time.sleep(5)

    #     heart = self.driver.find_element_by_css_selector("[aria-label=Like]")

    #     if(heart.get_attribute("fill") == "#262626"):
    #         return True
    #     else:
    #         return False




if __name__ == "__main__":

    xsum = 0
    igbot = InstaBot('siddhantscookups', 'AlphaQuartz123@', xsum)
    
    for tag in hashtags:
        igbot.searchTag(tag)
        for pic in range(0, 10):
            igbot.choosePic()

    

