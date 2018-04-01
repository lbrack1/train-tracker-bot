from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
from sys import exit
from bs4 import BeautifulSoup
import os

################################################################################
#
# FUNCTION TO SCRAPE RAILDAR
#
################################################################################

def scrape_raildar(config, out_time, return_time, path):
    
    # Open chrome and navigate to website
    url = 'https://raildar.co.uk/login'
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(1)
    
    # Login to raildar
    loginform_username = browser.find_element_by_name("_username")
    loginform_password = browser.find_element_by_name("_password")
    loginform_username.send_keys(config['username'])
    loginform_password.send_keys(config['password'])
    login_attempt = browser.find_element_by_id("login-form")
    login_attempt.submit()
    
    # Verfiy logged in 
    if "stat" not in browser.current_url:
        print("login failed. Terminating process.")
        exit(0)
    
    # Navigate to delay repay page    
    browser.find_element_by_css_selector("i.fa.fa-lg.fa-fw.fa-search").click()
    browser.find_element_by_xpath('//*[@title="Delay Repay"]').click()
    
    form_page = browser.find_element_by_id("content")
    time.sleep(5)
    
    start_st_form = browser.find_element_by_id("CommuterForm_startCrs")
    return_st_form = browser.find_element_by_id("CommuterForm_endCrs")
    
    print("Entering Form Details:")
    print("start station: " + config['start_station']) 
    start_st_form.send_keys(config['start_station'])
    time.sleep(5)
    browser.find_element_by_id('ui-id-1').click()
    
    print("return station: " + config['return_station']) 
    return_st_form.send_keys(config['return_station'])
    time.sleep(5)
    browser.find_element_by_id('ui-id-2').click()
    
    print("month: " + config['month'])
    select_month = Select(browser.find_element_by_id('CommuterForm_dt'))
    select_month.select_by_visible_text(config['month'])
    
    print("days of week: " + config['dow'])
    select_day = Select(browser.find_element_by_id('CommuterForm_dow'))
    select_day.select_by_visible_text(config['dow'])
    
    print("out time: " + out_time )
    select_outtime = Select(browser.find_element_by_id('CommuterForm_outTime'))
    select_outtime.select_by_visible_text(out_time)
    
    print("return time:" + return_time)
    select_returntime = Select(browser.find_element_by_id('CommuterForm_returnTime'))
    select_returntime.select_by_visible_text(return_time)
    
    #Submit form
    browser.find_element_by_id("CommuterForm").submit()
    
    # Wait for form to be submitted
    time.sleep(3)
    
    # Select data html element
    data_page_html = form_page.get_attribute("innerHTML")
    
    #while "loading..." in data_page_html:
    #    time.sleep(1)
    #    data_page_html = form_page.get_attribute("innerHTML")
    #    print data_page_html
    
    if "Table shows minutes delayed at destination" not in data_page_html: 
        time.sleep(3)
        data_page_html = form_page.get_attribute("innerHTML")
        
    if "Table shows minutes delayed at destination" not in data_page_html: 
        print data_page_html
        print("form submit failed. Terminating process.")
        exit(0)
    
    browser.close()
    
    # Parse the html as string and save to files
    soup = BeautifulSoup(data_page_html, 'lxml')
    os.chdir(path + "/raw")
    with open("html" + config['month'] + "_" + out_time + "_" + return_time + ".html", "w") as file:
        file.write(str(soup)) 


