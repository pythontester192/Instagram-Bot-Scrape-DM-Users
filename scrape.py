import os
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CM
from getpass import getpass


# FOR TESTING ==================
#username = ''
#password = ''
# ==============================

ELEMENTS_TIMEOUT = 15
FOLLOW_DATA_LOADING_TIMEOUT = 50


def scrape(): 

    username = input('Enter Your Username: ')
    password = input('Enter Your Password: ')



    options = webdriver.ChromeOptions()
    # TODO: invoking in headless removes need for GUI
    # options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument("--log-level=3")

    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/535.19"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    bot = webdriver.Chrome(executable_path=CM().install(), options=options)
    bot.set_window_size(600, 1000)

    bot.get('https://www.instagram.com/accounts/login/')

    time.sleep(2)

    print("Logging in...")

    user_element = WebDriverWait(bot, ELEMENTS_TIMEOUT).until(
        EC.presence_of_element_located((
            By.XPATH, '/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/div/label')))
            

    user_element.send_keys(username)

    pass_element = WebDriverWait(bot, ELEMENTS_TIMEOUT).until(
        EC.presence_of_element_located((
            By.XPATH, '/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[2]/div/label')))

    pass_element.send_keys(password)

    login_button = WebDriverWait(bot, ELEMENTS_TIMEOUT).until(
        EC.presence_of_element_located((
            By.XPATH, '/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[3]/button')))

    time.sleep(0.4)


    login_button.click()

    time.sleep(5)

    user_target = input('Enter Your Target Username: ')

    bot.get('https://www.instagram.com/{}/'.format(user_target))

    time.sleep(5)

    # stats = bot.find_elements_by_class_name("_ac2a")
    # num_followers = float((stats[1].text).replace(',', '.'))

    # print('Followers: ' + str(num_followers))


    target_followers=int(input('Enter How many followers you want to scrape (make sure the value is integer): '))



    # getting followers
    if target_followers > 0:
        bot.get('https://www.instagram.com/{}/followers/'.format(user_target))

        time.sleep(3.5)

        ActionChains(bot).key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT).perform()
        ActionChains(bot).key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT).perform()

    print('Scraping followers...')

    followers = set()

    not_loading_count = 0
    prev = 0
    while len(followers) < target_followers:

        ActionChains(bot).send_keys(Keys.END).perform()

        time.sleep(5)

        more_followers = bot.find_elements_by_xpath(
        "//a[@class='qi72231t nu7423ey n3hqoq4p r86q59rh b3qcqh3k fq87ekyn bdao358l fsf7x5fv rse6dlih s5oniofx m8h3af8h l7ghb35v kjdc1dyq kmwttqpk srn514ro oxkhqvkx rl78xhln nch0832m cr00lzj9 rn8ck1ys s3jn8y49 icdlwmnq notranslate _a6hd']")
        
        followers.update(more_followers)

        #print(len(followers))
        if len(followers) == prev:
            not_loading_count += 1
        else:
            not_loading_count = 0
        if not_loading_count == FOLLOW_DATA_LOADING_TIMEOUT:
            break
        prev = len(followers)

    users_followers = set()
    c = 0
    for i in followers:
        if i.get_attribute('href'):
            c += 1
            follower = i.get_attribute('href').split("/")[3]
            print(i.get_attribute('href'))
            users_followers.add(follower)
            #print (c, ' ', follower)
        else:
            continue        

    print('Saving to file...')
    print('[DONE] - Your followers are saved in usernames.txt file')

    with open('infos/usernames.txt', 'w') as file:
        file.write('\n'.join(users_followers) + "\n")

    print('Exiting...')

if __name__ == '__main__':
    scrape()
