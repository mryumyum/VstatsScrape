import os
import time
import re
import pickle
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
driver = webdriver.Chrome()

# DURING THIS TIME YOU NEED TO CHANGE THE CURRENCY FROM YEN TO DOLLARS AND TIME TO UST MANUALLY IN THE WEBSITE SETTINGS
driver.get('https://vt.poi.cat/settings')
time.sleep(30)

#year = input('Please enter the year you want to collect')
year = '2022'

sel_date_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(("xpath", "//button[contains(@class, '!rounded-full ng-tns-c1284214496-13 mdc-button mdc-button--outlined mat-mdc-outlined-button mat-unthemed mat-mdc-button-base')]")))
sel_date_button.click()
time.sleep(1)

sel_year_cont_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(("xpath", "//button[contains(@class, 'mat-calendar-period-button mdc-button mat-mdc-button mat-unthemed mat-mdc-button-base')]")))
sel_year_cont_button.click()
time.sleep(1)


sel_year_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(("xpath", f"//button[contains(@aria-label, '{year}')]")))
sel_year_button.click()
time.sleep(1)


first_month_year = 'January ' + f'{year}'
sel_month_button =  WebDriverWait(driver, 10).until(EC.presence_of_element_located(("xpath", f"//button[contains(@aria-label, '{first_month_year}')]")))
sel_month_button.click()
time.sleep(1)

first_of_month = 'January 1, ' + f'{year}'
sel_first_button =  WebDriverWait(driver, 10).until(EC.presence_of_element_located(("xpath", f"//button[contains(@aria-label, '{first_of_month}')]")))
sel_first_button.click()
time.sleep(1)

sel_year_cont_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(("xpath", "//button[contains(@class, 'mat-calendar-period-button mdc-button mat-mdc-button mat-unthemed mat-mdc-button-base')]")))
sel_year_cont_button.click()
time.sleep(1)


sel_year_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(("xpath", f"//button[contains(@aria-label, '{year}')]")))
sel_year_button.click()
time.sleep(1)

last_month_year = 'December ' + f'{year}'
sel_month_button =  WebDriverWait(driver, 10).until(EC.presence_of_element_located(("xpath", f"//button[contains(@aria-label, '{last_month_year}')]")))
sel_month_button.click()
time.sleep(1)

last_of_month = 'December 31, ' +  f'{year}'
sel_sec_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(("xpath", f"//button[contains(@aria-label, '{last_of_month}')]")))
ActionChains(driver).key_down(Keys.SHIFT).click(sel_sec_button).key_up(Keys.SHIFT).perform()

time.sleep(5)


every_hundreth = 0
element = driver.find_element('xpath', '//body')

while True:
    
    # Element.send_keys(Keys.PAGE_DOWN)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)
    # Loading every 100 ticks drastically reduces collection time
    every_hundreth += 1
    # try:
    #     WebDriverWait(driver, 10).until(EC.presence_of_element_located(("xpath", "//img[contains(@loading, 'lazy')]")))
    # except:
    #     break  # not more posts were loaded - exit the loop
    
    
    if every_hundreth%10 == 0:
        
        stop_element = driver.find_elements("xpath", "//div[contains(@class, 'mat-h3 font-medium ng-star-inserted')]")[-1].text
        print(stop_element)
        
        if f'{year}/01/01' in stop_element:
            
            elems = driver.find_elements("xpath", "//a[@href]")
            print("The number of elements is: " + str(len(elems)))
            print("Now collecting Links")
            holo_raw_data = [elem.get_attribute("href") for elem in elems if '/youtube-stream' in elem.get_attribute("href")]
            #print(filtered_urls)
            print("The length of the raw data is: " + str(len(holo_raw_data)))
            #pickle.dump(holo_raw_data, open(f'vstats_URL_{year}.pkl','wb'))
            year_col = True
            print(f'YEAR {year} COLLECTED')
            
            # Removes duplicates, but does not preserve the order
            # res = [*set(holo_raw_data)]
            # print(len(res))
            
            # Removes duplicates while preserving order of original list since we want them chronologically
            seen = set()
            seen_add = seen.add
            holo_ref_data = [x for x in holo_raw_data if not (x in seen or seen_add(x))]
            
            print(len(holo_ref_data))
            driver.quit()

pickle.dump(holo_raw_data, open(f'vstats_URL_RAW_2022.pkl','wb'))
pickle.dump(holo_ref_data, open(f'vstats_URL_2022.pkl','wb'))