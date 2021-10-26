#! /usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import os
import datetime
import logging
from dotenv import load_dotenv

logging.basicConfig(filename='/var/log/EDTBot/edt.log', level=logging.INFO)
logging.info(str(datetime.datetime.today()) + ' : Search EDT GEN')

os.chdir('/home/userbot/EDTBot/')

try:
    load_dotenv()

    login_gpu = os.getenv('LOGIN_GPU')
    mdp_gpu = os.getenv('MDP_GPU')


    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument("--window-size=1600,900")

    site = "https://iut-gpu.unice.fr/"

    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)

    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day + 2

    week = datetime.date(year, month, day).isocalendar()[1]

    driver.get(site)
    driver.maximize_window()

    login = driver.find_element_by_id("username")
    login.send_keys(login_gpu)

    passwd = driver.find_element_by_id("password")
    passwd.send_keys(mdp_gpu)

    connect_btn = driver.find_element_by_class_name("btn-submit")
    connect_btn.click()

    infos = driver.find_element_by_link_text('GPU')
    infos.click()

    edt = driver.find_element_by_link_text('Emplois du temps')
    edt.click()

    edt_grp = driver.find_element_by_link_text('EDT Filières')
    edt_grp.click()

    select = Select(driver.find_element_by_name('filiere'))
    select.select_by_value('LP-ASSR')


    week_nbr = int(week)

    while (driver.find_element_by_name('btn_sem_' + str(week_nbr)).value_of_css_property("cursor") != "pointer") :
        week_nbr += 1

    semaine = driver.find_element_by_name('btn_sem_' + str(week_nbr))
    date_semaine = driver.find_element_by_name('btn_sem_' + str(week_nbr)).get_attribute("title")
    semaine.click()


    for i in range(1,7):
        encres = driver.find_elements_by_tag_name('a')
        encres[14].click()


    reduire = driver.find_elements_by_id('#1')[1]
    reduire.click()

    with open('./images/gen.png', 'wb') as file:
        img = driver.find_element_by_id("entryform")
        file.write(img.screenshot_as_png)

    driver.close()

    logging.info(str(datetime.datetime.today()) + ' : Done')
except:
    logging.error(str(datetime.datetime.today()) + ' : !! ERROR !!')
