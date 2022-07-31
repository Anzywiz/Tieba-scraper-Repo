import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException


def get_links(url):
    """Opens the url provided and gets all 50 links to  various post on the page"""
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    try:
        driver.get(url)
    except TimeoutException:
        print("This is the link that caused the TimeoutException in 'get_links': " + url)

    # Animating slow scroll, could be irrelevant here though
    y = 1000
    # get scroll height
    last_height = (driver.execute_script("return document.body.scrollHeight"))
    for timer in range(0, 50):
        driver.execute_script('window.scrollTo(0, ' + str(y) + ')')
        y += 1000
        time.sleep(1)
        if y >= last_height:
            break
        else:
            continue

    list_of_tags = []
    html_soup = BeautifulSoup(driver.page_source, 'html.parser')
    for link_tags in html_soup.find_all('a', class_="j_th_tit", attrs={'rel': 'noopener'}):
        link_tag = link_tags.get('href')
        list_of_tags.append('https://tieba.baidu.com' + link_tag)
    return list_of_tags


def find_last_page_number(link):
    """Opens the Tieba link provided and gets the last page number
    which would be helpful to automatically loop through all the pages and
    extract the relevant data"""

    # open chrome driver
    driver = webdriver.Chrome()
    driver.set_window_size(520, 350)
    driver.implicitly_wait(1)
    try:
        # make request
        driver.get(link)
    except TimeoutException:
        print("This is the link that cause the TimeoutException in 'find_last_page_num': " + link)

    # parse and extract the data we need
    html_stew = BeautifulSoup(driver.page_source, 'html.parser')
    total_page_num_div = html_stew.find('li', class_="l_reply_num")
    children_div = total_page_num_div.findChildren()
    return int(children_div[1].text)

