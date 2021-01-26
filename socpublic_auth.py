import random
import time
import os
# from proxylist import files
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
import speech_recognition as sr
import ffmpy
import requests
import urllib
import pydub
from fake_useragent import UserAgent

ua = UserAgent()
a = ua.random
user_agent = ua.random
print(type(user_agent))

def delay():
    time.sleep(random.randint(2, 4))
try:
    option = webdriver.ChromeOptions()
    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_argument('--disable-notifications')
    option.add_argument(f'--user-agent={user_agent}')
    # option.add_argument(f'--proxy-server={files}')
    driver = webdriver.Chrome(os.getcwd() + "/chromedriver", options=option)
    delay()
    driver.get("https://socpublic.com/auth_login.html")
    login = 'login'
    password = 'pass'
    delay()
    driver.find_element(By.NAME,'name').send_keys(login)
    delay()
    driver.find_element(By.NAME,'password').send_keys(password)
    delay()
    time.sleep(random.randint(60,120))
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_xpath('//iframe[contains(@src, "google.com/recaptcha")]')))
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))).click()
    # driver.switch_to.default_content()
    delay()
    driver.switch_to.default_content()
    frames=driver.find_element_by_xpath("/html/body/div[6]/div[4]").find_elements_by_tag_name("iframe")
    driver.switch_to.frame(frames[0])
    delay()
    # 'recaptcha-audio-button'
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, 'recaptcha-audio-button'))).click()
    delay()
    #get the mp3 audio file
    src = driver.find_element_by_id("audio-source").get_attribute("src")
    print("[INFO] Audio src: %s"%src)
    #download the mp3 audio file from the source
    urllib.request.urlretrieve(src, os.getcwd()+"/sample.mp3")
    sound = pydub.AudioSegment.from_mp3(os.getcwd()+"/sample.mp3")
    sound.export(os.getcwd()+"/sample.wav", format="wav")
    sample_audio = sr.AudioFile(os.getcwd()+"/sample.wav")
    r= sr.Recognizer()
    with sample_audio as source:
        audio = r.record(source)
    #translate audio to text with google voice recognition
    key=r.recognize_google(audio)
    print("[INFO] Recaptcha Passcode: %s"%key)
    delay()
    time.sleep(5)
    driver.find_element_by_id("audio-response").send_keys(key.lower())
    driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
    driver.switch_to.default_content()
    delay()
    time.sleep(5)
    driver.find_element_by_id("recaptcha-demo-submit").click()
    delay()

    driver.find_element_by_id("recaptcha-audio-button").click()
    delay()
    driver.switch_to.default_content()
    frames= driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(frames[-1])
    delay()
except Exception as e:
    print(e)
finally:
    driver.close()
    driver.quit()
