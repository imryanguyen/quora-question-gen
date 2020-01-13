"""
Created on Fri Jan 3 23:17:06 2019
@author: Ryan Nguyen
"""

import time
from bs4 import BeautifulSoup
from selenium import webdriver
import argparse
import sys
import praw
from prawcore import NotFound, PrawcoreException
import csv
import datetime as dt
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys


email = "nduc.anh@gmail.com"
pwd = "DAcgl4nt@"
driver = webdriver.Chrome("/Users/ducn/.wdm/drivers/chromedriver/79.0.3945.36/mac64/chromedriver")
askbar_css = ""


def get_questions():
    subreddit = 'AskReddit'
    questions = []

    r = requests.get(
        'http://www.reddit.com/r/{}.json'.format(subreddit),
        headers={'user-agent': 'Mozilla/5.0'}
    )

    # view structure of an individual post
    # print(json.dumps(r.json()['data']['children'][0]))

    for post in r.json()['data']['children']:
        questions.append(post['data']['title'])
    return questions


def login(email, pw):
    print("Logging in...")
    driver.get("http://quora.com")
    form = driver.find_element_by_class_name('regular_login')
    username = form.find_element_by_name('email')
    username.send_keys(email)
    time.sleep(5)

    password = form.find_element_by_name('password')
    password.send_keys(pw)
    time.sleep(5)

    password.send_keys(Keys.RETURN)
    print("Logged in successfully.")
    time.sleep(10)
    # LOGIN FINISHED

def post_questions(questions_list):
    global askbar_css
    counter = 0


    # Iterate through qlist ask questions till no more
    for question in qlist:
        try:
            print(question)
            driver.get("http://quora.com")
            soup = BeautifulSoup(driver.page_source, "lxml")

            # Find all text areas
            blox = soup.find_all("textarea")

            # Find polymorphic id string for Ask Question entry field
            for x in blox:
                try:
                    placeholder = x["placeholder"]
                    # Fix this later
                    if placeholder.__contains__("Ask or Search Quora"):
                        askbar_css = "#" + x["id"]
                        print(askbar_css)
                except:
                    pass

            # Fix this later
            askbutton = "#" + soup.find(class_="AskQuestionButton")["id"]

            # Type out Question
            driver.find_element_by_css_selector(askbar_css).send_keys(question)

            # Wait for askbutton to become clickable
            time.sleep(.2)  # Fix later
            try:
                driver.find_element_by_css_selector(askbutton).click()
            except:
                # Click Failed # Fix later
                pass

            # Find the popup
            while True:
                try:
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    popExists = soup.find(class_="Modal AskQuestionModal")
                    break
                except:
                    pass
            soup = BeautifulSoup(driver.page_source, "lxml")
            popup = "#" + soup.find(class_="submit_button modal_action")["id"]
            driver.find_element_by_css_selector(popup).click()

            for x in range(0, 17):
                time.sleep(.1)
                try:
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    popExists = soup.find(class_="PMsgContainer")  # Found Popup

                    if str(popExists).__contains__("You asked"):  # big no no
                        counter += 1
                        break
                except:
                    pass
            print("counter=>", counter)

        except Exception as e:
            print(e)
            print("ERROR")
            pass


def main():
    qlist = get_questions()
    login(email, pwd)
    post_questions(qlist)
    

if __name__ == "__main__":
    main()