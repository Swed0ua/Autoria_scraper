from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import traceback
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import datetime
import json
from conf import URLS

from post_data import post_request_data

def browser_init():
    browser = webdriver.Chrome(ChromeDriverManager().install())
    return browser


def get_json_data():
    with open('result.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def set_json_data(data):
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

glob_ind = 0

def program (LINKs):
    global glob_ind
    browser = browser_init()
    for LINK in LINKs:
        time.sleep(2)
        browser.get(LINK)

        pages_count = int(browser.find_elements(By.CLASS_NAME, 'page-link')[-2].text)

        result = []

        for page_ind in range(1, pages_count+1):
            print(f'GET DATA WITH PAGE {page_ind} ---->')
            browser.get(f'{LINK}&page={page_ind}')
            print(f'{LINK}&page={page_ind}')
            time.sleep(1)
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')

            items = soup.find_all(class_='ticket-item')

            for item in items:
                try:
                    item_title_area = item.find(class_='ticket-title').find('a')
                    item_title = item_title_area.text.strip()
                    item_url = item_title_area.get('href')
                    browser.get(item_url)
                    print('Start scrapping ' + item_url)
                    time.sleep(0.1)

                    imgs_list = browser.find_element(By.CLASS_NAME, 'carousel-inner').find_elements(By.TAG_NAME, 'source')

                    img_src_text = ''

                    for img_item in imgs_list:
                        img_src_text += f"{img_item.get_attribute('srcset')},"
                    img_src_text = img_src_text[:-1]
                    main_img_src_text = imgs_list[0].get_attribute('srcset')

                    print(f'Imgs count : {len(imgs_list)}')

                    html = browser.page_source
                    soup = BeautifulSoup(html, 'html.parser')

                    tech_info_html = soup.find_all(class_='technical-info')[-1].find('dl')
                    try:
                        tech_info_items = tech_info_html.find_all('dd')

                        tech_info_text = ''
                        for tech_item in tech_info_items:
                            tech_info_text += f'{tech_item.text} \n'

                        tech_info_text = tech_info_text[:-1]
                    except:
                        tech_info_text = ''

                    try:
                        desc_bit = browser.find_element(By.CLASS_NAME, 'under-head').text
                    except:
                        desc_bit = ''

                    try:
                        full_desc = browser.find_element(By.CLASS_NAME, 'full-description').text
                    except:
                        full_desc = ''

                    try:
                        label_vin = browser.find_element(By.CLASS_NAME, 'label-vin').text
                    except:
                        label_vin = ''

                    try:
                        state_num_area = browser.find_element(By.CLASS_NAME, 'state-num')
                        state_num_add = state_num_area.find_element(By.TAG_NAME, 'span').text.strip()
                        state_num = state_num_area.text.replace(state_num_add, '').strip()
                    except:
                        state_num = ''
                        

                    try:
                        show_num_btn = browser.find_element(By.CLASS_NAME, 'phone_show_link')
                        browser.execute_script("arguments[0].click();", show_num_btn)
                        time.sleep(0.5)
                        is_vis_nim = True
                        while is_vis_nim:
                            phone_num = browser.find_element(By.CLASS_NAME, 'phone').text.replace('+38', '').replace('(','').replace(')','')
                            if phone_num.find('xxx-xx-xx') == -1:
                                is_vis_nim = False
                            else:
                                time.sleep(1) 
                                
                    except:
                        phone_num = ''

                    
                    price = browser.find_element(By.CLASS_NAME, 'price_value').find_element(By.TAG_NAME, 'strong').text

                    try:
                        author =browser.find_element(By.CLASS_NAME, 'seller_info_name').text
                    except:
                        author =''

                    # race = ''
                    # try:
                    #     race_area = browser.find_element(By.ID, 'details').find_element(By.CLASS_NAME, 'mhide')
                    #     race_label = race_area.find_element(By.CLASS_NAME, 'label').text.strip()
                    #     if race_label == 'Пробіг':
                    #         race += race_area.find_element(By.CLASS_NAME, 'argument').text.strip()
                    # except:
                    #     exec

                    race = browser.find_element(By.CLASS_NAME, 'base-information').text.replace('пробіг', '').strip()

                    prod_id = browser.find_element(By.TAG_NAME, 'body').get_attribute('data-auto-id')
                    item_data = {
                        'regionid':'6',
                        'phone': phone_num.replace(' ', '').strip(),
                        'id':prod_id,
                        'name': item_title.split('  ')[0],
                        'year': item_title.split('  ')[-1],
                        'race':race.replace('тис. км', '').replace(' ', '').strip(),
                        'price':price.replace('$', '').replace(' ', '').strip(),
                        'url':item_url,
                        'img':str(main_img_src_text),
                        'desc':full_desc.replace('\n', ''),
                        'fio':author
                    }

                    # result.append(item_data)
                    # set_json_data(result)
                    print(f'Result item num - {glob_ind}')
                    print(item_data)
                    post_request_data(item_data)
                    glob_ind += 1
                except Exception as e:
                    print(f'Error -> {e}')
                    time.sleep(5)
            
            

program(URLS)