import requests, os, sys, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd



url = "https://www.trip.com"
# print(os.getcwd())
driver = webdriver.Firefox(executable_path=os.getcwd()+'\geckodriver.exe')
driver.window_handles[0]
driver.get(url)

def get_hotel_details(hotel_card,country,date, window):
    hotel = hotel_card.find_element_by_class_name('select').click()
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[int(window)])
    name = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[3]/section[1]/div[2]/div[1]/section[1]/h1').text

    star_list = driver.find_elements_by_xpath('/html/body/div[2]/div[1]/div[3]/section[1]/div[2]/div[1]/section[1]/i')
    star_rating = len(star_list)+1
    room_list = driver.find_element_by_class_name('roomlist')
    room_detail_list = room_list.find_elements_by_class_name('roomlist-baseroom-cardB')
    data_list = []
    for room_detail in room_detail_list:
        room_name = room_detail.find_element_by_class_name('roomname')
        tax_price = room_detail.find_element_by_class_name('note')
        amanities = room_detail.find_element_by_xpath('/html/body/div[2]/div[1]/div[3]/div[1]/div[4]/div/div/div[1]/div[2]/div/div/div/div/div[1]/div[1]/span/span')
        data = {'Country':country,'Date':date,'Hotel Name':name,'Star Rating':star_rating,'Room Name':room_name.text,'Amanities':amanities.text,'Price':tax_price.text}
        print('*'*10)
        print(country)
        print(date)
        print(name)
        print(star_rating)
        print(room_name.text)
        print(tax_price.text)
        print(amanities.text)
        data_list.append(data)
    df = pd.DataFrame(data_list)
    df.to_csv('file.csv', index = False, header=True)


def increase_room_count(count):
    rooms = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div/div[2]/div/div[2]/div/div/div/ul/li[3]/div/div[3]/div[1]/div/span[2]')
    if count != int(rooms.text):
        increase_rooms = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div/div[2]/div/div[2]/div/div/div/ul/li[3]/div/div[3]/div[1]/div/span[3]').click()
        increase_room_count(count)

def increase_adult_count(count):
    adults = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div/div[2]/div/div[2]/div/div/div/ul/li[3]/div/div[3]/div[2]/div/span[2]')
    if count != int(adults.text):
        increase_adults = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div/div[2]/div/div[2]/div/div/div/ul/li[3]/div/div[3]/div[2]/div/span[3]').click()
        increase_adult_count(count)

def increase_child_count(count):
    childs = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div/div[2]/div/div[2]/div/div/div/ul/li[3]/div/div[3]/div[3]/div/span[2]')
    if count != int(childs.text):
        increase_childs = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div/div[2]/div/div[2]/div/div/div/ul/li[3]/div/div[3]/div[3]/div/span[3]').click()
        increase_child_count(count)


def select_date(split_date,split_month):
    # print(split_date,split_month)
    month_elements = [driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div/div[2]/div/div[2]/div/div/div/ul/li[2]/div/div[4]/div/div[1]/div[1]/h3')]
    if month_elements[0].text.strip() == split_month:
        month_list_element = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div/div[2]/div/div[2]/div/div/div/ul/li[2]/div/div[4]/div/div[1]/div[1]')
        # print(month_list_element)
        day_elements = month_list_element.find_elements_by_xpath('/html/body/div[1]/div[4]/div[3]/div/div[2]/div/div[2]/div/div/div/ul/li[2]/div/div[4]/div/div[1]/div[1]/div/ul/li')
        for i in day_elements:
            if i.text == split_date:
                i.click()
                break
    else:
        next_month = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div/div[2]/div/div[2]/div/div/div/ul/li[2]/div/div[4]/div/div[1]/span[2]').click()
        select_date(split_date,split_month)

def sort_date(date_given):
    checkin_split_date = date_given.split('-')
    checkin_split_year = checkin_split_date[1].split(' ')
    select_date(checkin_split_date[0],checkin_split_date[1].strip())


country = 'Beijing'
date = '25-Nov 2020'
destination = driver.find_element_by_id('hotels-destination')
destination.send_keys(country)
time.sleep(4)
check_in = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div/div[2]/div/div[2]/div/div/div/ul/li[2]/div/div[1]/input').click()
sort_date(date)
sort_date('5-Dec 2020')

stay_choice = driver.find_element_by_class_name('choice').click()
rooms = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div/div[2]/div/div[2]/div/div/div/ul/li[3]/div/div[3]/div[1]/div/span[2]')
no_of_rooms = 1
no_of_adults = 2
no_of_childs = 0
increase_room_count(no_of_rooms)
increase_adult_count(no_of_adults)
increase_child_count(no_of_childs)

search = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div/div[2]/div/div[2]/div/div/div/ul/li[4]/div').click()
time.sleep(5)

hotels_list = driver.find_element_by_class_name('long-list')
hotel_data_list = hotels_list.find_elements_by_class_name('with-decorator-wrap')
get_hotel_details(hotel_data_list[0],country,date,1)
# for hotel_data in hotel_data_list:
#     window = 1
#     get_hotel_details(hotel_data,country,date,window)
#     window += 1




# checkin_string_date = '2-Nov 2020'
# checkin_split_date = checkin_string_date.split('-')
# checkin_split_year = checkin_split_date[1].split(' ')
# print(checkin_split_date)

# select_date(checkin_split_date[0],checkin_split_date[1].strip())
#
# checkout_string_date = '30-Nov 2020'
# checkout_split_date = checkout_string_date.split('-')
# checkout_split_year = checkout_split_date[1].split(' ')
# select_date(checkout_split_date[0],checkout_split_date[1].strip())
