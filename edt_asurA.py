#! /usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import os
import datetime
import logging
import dotenv
from dotenv import load_dotenv
from calendar import monthrange

logging.basicConfig(filename='/var/log/EDTBot/edt.log', level=logging.INFO)
logging.warning(str(datetime.datetime.today()) + ' : Search EDT ASUR A')

os.chdir('/home/userbot/EDTBot/')

try:
    load_dotenv()
    login_gpu = os.getenv('LOGIN_GPU')
    mdp_gpu = os.getenv('MDP_GPU')

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument("--window-size=1920,1080")

    site = "https://iut-gpu.unice.fr/"

    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)

    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day + 2
    num_days = monthrange(year, month)[1]

    if day > num_days:
        month += 1
        day = 1
    week = datetime.date(year, month, day).isocalendar()[1]

    try:
        driver.get(site)
        driver.maximize_window()
    except:
        logging.error(str(datetime.datetime.today()) + ' : !! Site unreachable !!')

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

    edt_grp = driver.find_element_by_link_text('EDT Groupes')
    edt_grp.click()

    select = Select(driver.find_element_by_name('filiere'))
    select.select_by_value('LP-ASSR')

    select2 = Select(driver.find_element_by_name('groupe'))
    select2.select_by_value('ASUR-A')

    week_nbr = int(week)

    while (driver.find_element_by_name('btn_sem_' + str(week_nbr)).value_of_css_property("cursor") != "pointer") :
        if week_nbr >= 52 :
            week_nbr = 1
        else:
            week_nbr += 1

    if week_nbr >= 30:
        week_nbr = os.getenv('SEMAINE_NBR')
    
    semaine = driver.find_element_by_name('btn_sem_' + str(week_nbr))
    date_semaine = driver.find_element_by_name('btn_sem_' + str(week_nbr)).get_attribute("title")
    semaine.click()

    for i in range(1,10):
        encres = driver.find_elements_by_tag_name('a')
        encres[14].click()

    reduire = driver.find_elements_by_id('#1')[1]
    reduire.click()

    with open('./images/asurA.png', 'wb') as file:
        img = driver.find_element_by_xpath('//*[@id="entryform"]/table')
        file.write(img.screenshot_as_png)

    os.environ["SEMAINE_NBR"] = str(week_nbr)
    dotenv.set_key('/home/userbot/DiscordBot/.env', "SEMAINE_NBR", os.environ["SEMAINE_NBR"])

    os.chmod("/home/userbot/DiscordBot/.env", 0o711)

    os.environ["WEEK_DATE"] = str(date_semaine)
    dotenv.set_key('/home/userbot/DiscordBot/.env', "WEEK_DATE", os.environ["WEEK_DATE"])

    logging.info(str(datetime.datetime.today()) + ' : Done')
    logging.info(str(datetime.datetime.today()) + ' : Finished without error')
except:
    logging.error(str(datetime.datetime.today()) + ' : !! ERROR !!')

driver.close()
logging.warning(str(datetime.datetime.today()) + ' : END EDT ASUR A')