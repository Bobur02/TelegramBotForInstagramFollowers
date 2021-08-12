import keep_alive
import os
import telebot
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import time

keep_alive.keep_alive()

API_KEY = os.environ['API_KEY']
email = os.environ['email']
password = os.environ['emailpass']
bot = telebot.TeleBot(API_KEY)

options = Options()
options.headless = True
#browser = webdriver.Firefox()
time.sleep(3)
browser = webdriver.Firefox(options=options)


@bot.message_handler(commands=['openbrowser'])
def openBrowser(message):
  newbrowser = webdriver.Firefox()
  time.sleep(3)
  bot.reply_to(message, "Browser opened")
  browser=newbrowser


@bot.message_handler(commands=['test'])
def hello(message):
    bot.send_message(message.chat.id, "i'm ready for some work")


@bot.message_handler(commands=['login'])
def login(message):
  try:
    bot.reply_to(message, "Starting... ")
    browser.get('https://instagram.com/')
    time.sleep(3)
    usernameInput = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[name='username']")))
    passwordInput = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[name='password']")))
    usernameInput.clear()
    time.sleep(1)
    passwordInput.clear()
    time.sleep(1)
    usernameInput.send_keys(email)
    time.sleep(1)
    passwordInput.send_keys(password)
    time.sleep(2)
    log_in = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[type='submit']"))).click()
    time.sleep(2)
    bot.reply_to(message, "I'm logged in!\nI still have to close 2 pop-ups, will take about 2 mins so please hang on... ")
    try:
      notNow = WebDriverWait(browser, 60).until(
          EC.element_to_be_clickable(
              (By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
      bot.reply_to(message, "First pop-up was closed")
    except Exception as e:
      bot.reply_to(message, "ERROR encountered when trying to close First pop-up ")
    try:
      notNow2 = WebDriverWait(browser, 120).until(
          EC.element_to_be_clickable(
              (By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
      bot.reply_to(message, "Secont pop-up was closed\nDone, I'm logged in!")
    except Exception as e:
      bot.reply_to(message, "ERROR encountered when trying to close Second pop-up ")
  except Exception as e:
    print(e,type(e))
    bot.reply_to(message, "Something went wrong, please try again!")


def follow_request(message):
    request = message.text.split()
    if len(request) < 2 or request[0].lower() not in "follow":
        return False
    else:
        return True


@bot.message_handler(func=follow_request)
def follow(message):
  try:
      accoutToFollow = message.text.split()[1]
      bot.reply_to(message, "Starting to follow " + accoutToFollow +"'s followers'")
      search = WebDriverWait(browser, 10).until(
          EC.element_to_be_clickable(
              (By.CSS_SELECTOR, "input[placeholder='Search']")))
      search.clear()
      search.send_keys(accoutToFollow)
      time.sleep(2)
      search.send_keys(Keys.ENTER)
      time.sleep(1)
      #search.send_keys(Keys.ENTER)
      #time.sleep(3)
      followers = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "followers"))).click()
      bot.reply_to(message, "Followers list opened")
      scroll_box = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div/div/div[2]")))
      last_ht, ht = 0, 1
      bot.reply_to(message, "Start scrolling followers list")
      while last_ht != ht:
          last_ht = ht
          time.sleep(1.5)
          ht = browser.execute_script("""arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight;
                    """, scroll_box)
          bot.reply_to(message, ht)
      bot.reply_to(message, "Finished scrolling the followers list")
      buttons = browser.find_elements_by_xpath("//button[contains(.,'Follow')]")
      time.sleep(2)
      bot.reply_to(message, "Starting to follow")
      counter = 0
      for i in range(len(buttons)):
          if buttons[i].text == 'Follow':
              if counter%10 == 0:
                bot.reply_to(message, counter + " accounts followed")
              # Use the Java script to click on follow because after the scroll down the buttons will be un clickeable unless you go to it's location
              browser.execute_script("arguments[0].click();", buttons[i])
              counter +=1
              # getFollowersUI.targetAccountName_4.setText("Following " + i + "/" + numberToFollow + " accounts")

              time.sleep(1.5)
  except Exception as e:
    bot.reply_to(message, "Something went wrong, please try again!")

try:
  bot.polling()
except Exception as e:
  print(e)
