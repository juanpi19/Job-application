from bs4 import BeautifulSoup
import requests
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

password = 'Jpjhs14.'
email = "juanpablacho19@gmail.com"
PATH = "/Users/juanpih19/Library/Mobile Documents/com~apple~CloudDocs/selenium/chromedriver"

#final_list = pd.DataFrame({'Job Title': [], 'Company Name': [], 'Location': [], 'link':  []})
#final_list.to_csv('final_list.csv', index=False)

class easyApply:
    def __init__(self):
        self.password = password
        self.email = "juanpablacho19@gmail.com"
        self.driver = webdriver.Chrome(PATH)
        self.keywords = "marketing advertising miami"

    def log_in(self):
        self.driver.get("https://www.linkedin.com")
        time.sleep(3)
        username = self.driver.find_element_by_id('session_key')
        username.send_keys(self.email)
        password = self.driver.find_element_by_id('session_password')
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(1)
        remember_button = self.driver.find_element_by_class_name("btn__primary--large")
        remember_button.click()

    def accesing_job_list(self):
        #jobs_button = self.driver.find_element_by_xpath('//*[@id="ember33"]/span')
        jobs_button = self.driver.find_element_by_link_text('Jobs')
        jobs_button.click()
        time.sleep(1)
        skill = self.driver.find_element_by_class_name('jobs-search-box__text-input')
        skill.send_keys(self.keywords)
        skill.send_keys(Keys.RETURN)


    def scroll_down(self):
        self.driver.maximize_window()
        self.driver.execute_script("window.scrollBy(0,2000)","")


    def job_titles(self):
        src = self.driver.page_source
        soup = BeautifulSoup(src, features="lxml")
        linkedin_jobs = soup.find('section', class_='jobs-search__left-rail')
        #titles = linkedin_jobs.find_all(class_='full-width artdeco-entity-lockup__title ember-view')
        titles = linkedin_jobs.find_all(class_='disabled ember-view job-card-container__link job-card-list__title')
        job_list = []
        for title in titles:
            job_list.append(title.text)
        # find company name
        time.sleep(1)
        companies = linkedin_jobs.find_all(class_ = 'artdeco-entity-lockup__subtitle ember-view')
        company_list = []
        for company in companies:
            company_list.append(company.text)
        # find location
        time.sleep(1)
        location = linkedin_jobs.find_all(class_= 'artdeco-entity-lockup__caption ember-view')
        location_list = []
        for l in location:
            location_list.append(l.text)
        # find links
        time.sleep(1)
        links = linkedin_jobs.find_all('a', class_='disabled ember-view job-card-container__link job-card-list__title')
        link_list = []
        for link in links:
            link_list.append("http://www.linkedin.com" + link['href'])


        new_jobs = pd.DataFrame({'Job Title': job_list, 'Company Name': company_list, 'Location': location_list, 'link':  link_list})
        new_jobs['Is Recommended?'] = new_jobs['Job Title'].str.contains('Data')
        df = pd.read_csv("final_list.csv")
        final_list = pd.concat([new_jobs, df ])
        final_list.to_csv("final_list.csv", index=False)

    def close_page(self):
        self.driver.quit()







if __name__ == "__main__":
    bot = easyApply()
    bot.log_in()
    time.sleep(5)
    bot.accesing_job_list()
    time.sleep(5)
    bot.scroll_down()
    time.sleep(5)
    bot.job_titles()
    time.sleep(5)
    bot.close_page()
