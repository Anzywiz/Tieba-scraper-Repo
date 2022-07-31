from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time
from My_Tieba_Functions import get_links
from My_Tieba_Functions import find_last_page_number
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# writing the header of the csv file
file = open('tieba_blah9.csv', 'a', newline='', encoding='UTF8')
writer = csv.writer(file)
writer.writerow(["NAME", 'LINK TO PROFILE', 'IMAGE', "POST(COMMENT/REPLY)", "DATE POSTED", "PHONE USED", "LINK TO POST"])

# getting links to all the post on the page using my custom fxn "get_links"
# NB The links to the post on the page are not constant and changes from time to time
url_given = "https://tieba.baidu.com/f?kw=%E5%AE%81%E5%BE%B7%E6%97%B6%E4%BB%A3%E6%96%B0%E8%83%BD%E6%BA%90&ie=utf-8"
links = get_links(url_given)
print(links)
for link in links:
    print(link)

    # saving the links to a txt file, should in case the pc crashes the last link can be retrieved
    with open("links_printed.txt", 'a') as file_object:
        file_object.write(link + '\n')

    # To get the last page of a particular link
    # using my find_last_page function
    last_page = find_last_page_number(link)

    driver = webdriver.Chrome()
    driver.set_window_size(520, 350)

    # Using the last page value to know the number of pages
    # then moving to the NEXT page by Looping through
    for page_number in range(1, last_page + 1):
        url = link
        page = url + '?pn=' + str(page_number)
        try:
            driver.implicitly_wait(1)
            driver.get(page)
            wait_factor = WebDriverWait(driver, 1).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "l_post j_l_post l_post_bright  ")
                )
            )
            if wait_factor:
                continue

        except TimeoutException:
            print("This is the page that ended in TimeoutException in 'Tieba' " + page)
            with open('tieba_timeouts_links.txt', 'a') as file_object:
                file_object.write(page + '\n')
            pass

        # animating slow scrolling to load DATES..
        # since dates would only load when you slowly scroll passed them towards the bottom of the page
        # Analyse the page and you would find out
        y = 1000
        last_height = (driver.execute_script("return document.body.scrollHeight"))
        for timer in range(0, 50):
            driver.execute_script('window.scrollTo(0, ' + str(y) + ')')
            y += 1000
            time.sleep(2)
            if y >= last_height:
                break
            else:
                continue

        html_soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Getting  the comments infos
        for each_post in html_soup.find_all('div', class_="l_post"):
            row = []
            name = each_post.find('li', class_="d_name").find('a', attrs={'alog-group': "p_author"}, class_=
            'p_author_name')
            try:
                row.append(name.text)
            except AttributeError:
                row.append(name)

            name_link = each_post.find('a', class_='p_author_name')
            try:
                row.append('https://tieba.baidu.com:' + name_link.get('href'))
            except AttributeError:
                pass

            image = each_post.find('img')
            row.append('https:' + image.get('src'))

            post = each_post.find('div', class_="d_post_content")
            try:
                row.append(post.text)
            except AttributeError:
                row.append('Oops!.. not in this tag')

            date = each_post.find('ul', class_="p_tail")
            try:
                ul_children = date.findChildren()
                row.append(ul_children[2].text)
            except AttributeError:
                row.append(date)

            phone_type = each_post.find('a', class_="p_tail_wap")
            try:
                row.append(phone_type.text)
            except AttributeError:
                row.append(phone_type)

            # append the link to the comment page
            row.append(page)

            writer.writerow(row)
            print(row)

        # Getting replies to comments infos
        for reply in html_soup.find_all("li", class_="lzl_single_post"):
            reply_row = []

            name = reply.find("a", class_='at', attrs={'target': '_blank'})
            try:
                reply_row.append(name.text)
            except AttributeError:
                pass

            # link to profile
            try:
                reply_row.append("https://tieba.baidu.com:" + name.get('href'))
            except AttributeError:
                pass

            image = reply.find('img')
            try:
                reply_row.append("https:" + image.get('src'))
            except AttributeError:
                pass

            reply_txt = reply.find('span', class_="lzl_content_main")
            try:
                reply_row.append(reply_txt.text)
            except AttributeError:
                pass

            date = reply.find('span', class_="lzl_time")
            try:
                reply_row.append(date.text)
            except AttributeError:
                pass

            reply_row.append("Replies have no phone data")

            reply_row.append(page)

            writer.writerow(reply_row)
            print(reply_row)















