# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.chrome.options import Options
import unittest, time, re
import json
from resource import cookies
from resource import ids
from resource import dateTime
import nose,sqlite3
import facebook

db=sqlite3.connect("d://HelloWorldDb")
cursor=db.cursor()

class Uids(unittest.TestCase):
    def setUp(self):
        #disble images
        chrome_options = Options()
        chrome_options.add_experimental_option( "prefs", {'profile.default_content_settings.images': 2})
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
               
#        options=[]
#        options.append('--load-images=false')
#        self.driver=webdriver.PhantomJS(executable_path='C:\\Users\\VUGON\\Desktop\\phantomjs-2.0.0-windows\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe',service_args=options)
        #self.driver.implicitly_wait(30)

    def test_uids(self):
        driver = self.driver
        driver.get("https://www.facebook.com")
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        self._uids(driver)
            
    def _search(self,driver):
        driver.get("https://www.facebook.com/search/str/uber%2Btaxi/keywords_top")
        
        if(driver.title=="Content Not Found"):
            return
        data=[]
        lengthBreak=[]
        length=0        
        
        numberOfUid=driver.find_element_by_xpath("//*/h3[contains(@class,'_52ja')]").text
        numberOfUid=float(numberOfUid[numberOfUid.index("(")+1:len(numberOfUid)-1].replace(",",""))
        while(True):
            subDriver1=driver.find_elements_by_xpath("//*/div[contains(@id,'member_')]")
            lengthBreak.append(len(subDriver1))
            if (numberOfUid>39):
                if(lengthBreak.count(max(set(lengthBreak)))>2 and len(data)>39) or len(lengthBreak)>77: 
                    break
            else :
                if(lengthBreak.count(max(set(lengthBreak)))>1):
                    break
            subDriver1=subDriver1[length+1:len(subDriver1)]
            for uidItem in subDriver1:
                driver.execute_script("window.scrollBy(0,10000);")
                uid=uidItem.get_attribute("id")
                uid=uid[uid.index("_")+1:len(uid)]
                try:
                    name=uidItem.find_element_by_tag_name("h1").text
                except:
                    name=uidItem.find_element_by_tag_name("h3").text
                element={'uid':uid,'name':name}
                length=len(data)
                if(element not in data):
                    data.append(element)
                    cursor.execute('''INSERT OR IGNORE INTO ID_LIST (ID,NAME) VALUES(?,?)''',[uid,name] )
                    db.commit()
                    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    nose.main()
