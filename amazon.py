from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import logging
import selenium
import time
from logging import handlers

fileHandler = handlers.RotatingFileHandler(filename='amazonbotlog.txt',maxBytes=50000000,backupCount=10)
consoleHandler = logging.StreamHandler()

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('amazon')
formater = logging.Formatter('%(asctime)s %(message)s')

logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)
fileHandler.setFormatter(formater)
consoleHandler.setFormatter(formater)

logger.info("Welcome")

driver = webdriver.Chrome()
driver.get("https://www.amazon.com")
signLine = driver.find_element_by_id("nav-link-accountList")
signLine.click()

###### comment out this block and uncomment next block for autologin
while True: #wait for sign in
    try:
        searchbar = driver.find_element_by_id('twotabsearchtextbox')
    except selenium.common.exceptions.NoSuchElementException:
        time.sleep(2)
        logger.info("Please login ...")
    else:
        break

print("Thanks. Let me take it from here. Grab a beer and just watch ...")

# time.sleep(60)
# elem = driver.find_element_by_id("ap_email")
# elem.send_keys("myemail")
# elem.send_keys(Keys.RETURN)
# elem_pass = driver.find_element_by_id("ap_password")
# elem_pass.send_keys("mypassword")
# elem_pass.send_keys(Keys.RETURN)


driver.get("https://www.amazon.com/ga/giveaways?pageId=1")

for j in range(1,132):
    for i in range(1,25):
        no_cont = False
        try:
            time.sleep(0.5)
            item = driver.find_element_by_id("giveaway-item-"+str(i))
            item.click()
            time.sleep(2)
        except Exception as er:
            print(er)
            continue

        #you can just get logged out to switch accounts page for some reason, see if you are being asked to switch account
        #and then login again by clicking the button
        try:

            switch_accounts = driver.find_element_by_class_name("a-text-left")
            if not switch_accounts.text == "Switch accounts":
                raise Exception("Some other a-text-left caught") #ignroe and continue
            else:
                logger.info("Account got forced signed out. Getting in Again")
                account = driver.find_element_by_class_name('a-row')
                account.click()
                time.sleep(2)
        except:
            pass

        #driver.get("https://www.amazon.com/ga/p/b8ec883387ad98ac?nav=amz&fsrc=glp&return_to=https%3A%2F%2Fwww.amazon.com%2Fga%2Fgiveaways%3FpageId%3D2&ref_=aga_p_vg_lp_p2_g16_nodup_dgv#ln-yt")
        logger.info(str(j)+":"+str(i)+": Processing: " + driver.current_url)
        try:
            tt = driver.find_element_by_id('title')
            result = tt.text
            logger.info(result)
            driver.get("https://www.amazon.com/ga/giveaways?pageId=" + str(j))
            continue
        except selenium.common.exceptions.NoSuchElementException:
           pass

        try:
            video = driver.find_element_by_id("airy-container")
            logger.info("attempting video playback and wating 30 seconds")
            video.click()
            time.sleep(35)
        except:
            try:
                video = driver.find_element_by_id("youtube-container")
                logger.info("attempting youtube playback and wating 30 seconds")
                video.click()
                time.sleep(35)
            except:
                try:
                    box = driver.find_element_by_id("giveaway-social-container")
                    logger.info("Attempting box click and waiting 5 seconds")
                    box.click()
                    time.sleep(10)
                    no_cont = True
                except:
                    pass

        if not no_cont:
            try:
                cont = driver.find_element_by_name("continue")
                logger.info("Attempting to press continue")
                cont.click()
                time.sleep(10)
            except selenium.common.exceptions.ElementNotVisibleException:
                logger.info("Item not visible, trying again in 10 sec")
                time.sleep(35)
                try:
                    cont = driver.find_element_by_name("continue")
                    cont.click()
                    time.sleep(1)
                except:
                    pass
            except:
                pass

        try:
            switch_accounts = driver.find_element_by_class_name("a-text-left")
            if not switch_accounts.text == "Switch accounts":
                raise Exception("Some other a-text-left caught")  # ignroe and continue
            else:
                logger.info("Account got forced signed out. Getting in Again")
                account = driver.find_element_by_class_name('a-row')
                account.click()
                time.sleep(15)  # something not right
        except:
            pass

        try:
            tt = driver.find_element_by_id('title')
            result = tt.text
        except selenium.common.exceptions.NoSuchElementException:
            result = "Unknown result"
            time.sleep(2)  # something not right
            #might have logged out


        logger.info("Result: " +result)
        url = driver.current_url
        logger.info(url+" : "+result)
        time.sleep(1)
        driver.get("https://www.amazon.com/ga/giveaways?pageId=" + str(j))

    driver.get("https://www.amazon.com/ga/giveaways?pageId=" + str(j+1))


