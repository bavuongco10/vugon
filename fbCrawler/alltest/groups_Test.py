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

groups=[]
db=sqlite3.connect("d://HelloWorldDb")
cursor=db.cursor()

class Groups(unittest.TestCase):
    def setUp(self):
        #disble images
        chrome_options = Options()
        chrome_options.add_experimental_option( "prefs", {'profile.default_content_settings.images': 2})
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
#        options=[]
#        options.append('--load-images=false')
#        self.driver=webdriver.PhantomJS(executable_path='C:\\Users\\VUGON\\Desktop\\phantomjs-2.0.0-windows\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe',service_args=options)
        #self.driver.implicitly_wait(30)
        self.base_url = "https://m.facebook.com/profile.php?v=info&id=100001150323526&nocollections=1"

    
    def test_groups(self):
        driver = self.driver
        driver.get("https://m.facebook.com")
#        driver.find_element_by_name("email").clear()
#        driver.find_element_by_name("email").send_keys("facebookAccount['user']")
#        driver.find_element_by_name("pass").clear()
#        driver.find_element_by_name("pass").send_keys("facebookAccount['password']") #insert password
#        driver.find_element_by_name("login").click()
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        for id in ids:
            self._groups(driver,id)
        self._writeData(groups)            
            
    def _writeData(self,groups):        
            with open('d:\\fbData\\groups_'+dateTime+'.txt', 'a+') as f:
                f.write(json.dumps(groups))
                f.closed
                
    def _groups(self,driver,id):
        driver.get("https://m.facebook.com/timeline/app_collection/?collection_token="+id+"%3A2361831622%3A66")
        if(driver.title=="Content Not Found"):
            return
            
        data=[]
        lengthBreak=[]
        length=0
        numberOfGroups=int(driver.find_element_by_class_name("_52jg").text.replace(",",""))
        while(True):
            subDriver1=driver.find_elements_by_xpath("//*/div[contains(@id,'66:')]")
            lengthBreak.append(len(subDriver1))
            if (numberOfGroups>12):
                if(lengthBreak.count(max(set(lengthBreak)))>2 and len(data)>12) or len(lengthBreak)>77: 
                    break
            else :
                if(lengthBreak.count(max(set(lengthBreak)))>1):
                    break
            subDriver1=subDriver1[length:len(subDriver1)]
            for groupItem in subDriver1:
                driver.execute_script("window.scrollBy(0,10000);")
                link=groupItem.find_element_by_class_name("touchable").get_attribute("href")
                link=link[30:len(link)]
                members=groupItem.find_element_by_class_name("_558d").text
                members=float(members[0:members.index(" ")].replace(",",""))
                group={'link':link,'memebers':members,'numberOfGroups':numberOfGroups}
                cursor.execute('''INSERT OR IGNORE INTO GROUPS VALUES(?,?)''',[link,members] )
                cursor.execute('''INSERT OR IGNORE INTO PEOPLE_GROUP VALUES(?,?)''',[id,link] )
                db.commit()
                if(group not in data):
                    data.append(group)
                length=len(data)
                    
                    
        groups.append({'id':id,'data':data})
        print("Groups_"+id+":"+str(len(data))+"/"+str(numberOfGroups))
        print(str(ids.index(id)+1)+"/"+str(len(ids)))
                    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    nose.main()
