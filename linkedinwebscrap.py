
#Created on Sep 13, 2019

#@author: Jeremy Cheung

import unittest
import time
import csv
import pandas as pd
import re
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome("Drivers/chromedriver77/chromedriver.exe")
        # ENTER DRIVER INSTALL LOCATION
    def test_search_in_linkedin(self):
        driver = self.driver
        driver.get("http://www.linkedin.com")
        time.sleep(2)
        elementclicktologin = driver.find_element_by_class_name("nav__button-secondary")
        elementclicktologin.click()
        time.sleep(2)
        
        
        #username and password enter
        username=driver.find_element_by_id("username")
        username.send_keys("ENTER EMAIL HERE")
       # elem.send_keys(Keys.RETURN)
        password=driver.find_element_by_id("password")
        # getting password from text file 
        with open('test.txt', 'r') as myfile: 
            passwordfile = myfile.read().replace('\n', '') 
        password.send_keys(passwordfile)
        time.sleep(2)
        
        loginelement=driver.find_element_by_class_name("login__form_action_container ")
        loginelement.click()
       # assert "No results found." not in driver.page_source
        
        driver.get("https://www.linkedin.com/jobs/")
        
        searchjobs=driver.find_element_by_id("jobs-search-box-keyword-id-ember37")
        searchjobs.send_keys("engineer")
        
        searchlocation=driver.find_element_by_id("jobs-search-box-location-id-ember37")
        searchlocation.send_keys("toronto")
        searchlocation.send_keys(Keys.RETURN)
        
        time.sleep(10)
        
        
        titlelist=[]
        companylist=[]
        joblist=[]
        urllist=[]
        window_before = driver.window_handles[0]
        
        for page in range(1,2):
            for iteratore in range(1,5):
                try:
                    listofjobs=driver.find_element_by_xpath("/html/body/div[6]/div[5]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div/ul/li["+str(iteratore)+"]/div")
                    listofjobs.click()    
        
                    time.sleep(2)
        
                    title=driver.find_element_by_xpath("/html/body/div[6]/div[5]/div[3]/section[1]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div[1]/div/div[3]/a/h1").text
                    print(title)
                    titlelist.append(title)
                
                    company=driver.find_element_by_xpath("/html/body/div[6]/div[5]/div[3]/section[1]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div[1]/div/div[3]/div[1]/a").text
                    print(company)
                    companylist.append(company)
            
                    try:
                        jobdescription=driver.find_element_by_id("job-details").text
                        print(jobdescription)
                        joblist.append(jobdescription)
                        #industry=re.search(r"[fF]u?l?l?\s*-[tT]i?m?e?"),jobdescription)           
                    except Exception:
                        pass
                    
                    
                        window_before = driver.window_handles[0]
                        print(window_before)
                    
                    try:
                        entry=driver.find_element_by_xpath('//*[contains(@data-control-name,"shareProfileThenExternalApplyControl")]')
                        entry.click()
                    
                        window_after = driver.window_handles[iteratore]
                        driver.switch_to_window(window_after)
                    
                        url=driver.current_url
                        print(url)
                        print('first test')
                        '''
                        if url==None:
                            try:
                                entry1=driver.find_element_by_xpath('//*[contains(@class,"jobs-apply-button--top-card ember-view")]')
                                entry1.click()
                                url=driver.current_url
                                print(url)
                                print('second test')
                                window_after2 = driver.window_handles[2]
                                driver.switch_to_window(window_after2)
                                
                            except Exception:
                                pass
                            
                        else:
                            try:
                                entry2=driver.find_element_by_xpath('//*[contains(@class,"jobs-s-apply jobs-s-apply--fadein inline-flex mr2 ember-view")]')
                                entry2.click()
                                url=driver.current_url
                                print(url)
                                print('third test')
                                window_after3 = driver.window_handles[3]
                                driver.switch_to_window(window_after3)
                            except Exception:
                                pass
                        '''   
                        urllist.append(url)
                        driver.switch_to_window(window_before)
                        
                    except Exception:
                        pass  
                
                except Exception:
                    pass 
                
            driver.switch_to_window(window_before)
                  
            print(titlelist)
            print(companylist)
            print(joblist)
            print(urllist)
            
            finallist = pd.DataFrame(list(zip(titlelist, companylist, joblist,urllist)),columns=['Title','Company','Job Description','Url: '])
            jobsearch_data = finallist.to_csv('jobsearchlist.csv', index=False)
            
        pagestring='Page'+str(page)
        pagebutton=driver.find_element_by_xpath('//*[contains(@aria-label,pagestring)]')
        pagebutton.click()   
                    
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()