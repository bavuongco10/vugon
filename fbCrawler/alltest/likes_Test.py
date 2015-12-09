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

likes=[]
db=sqlite3.connect("d://HelloWorldDb")
cursor=db.cursor()
class Likes(unittest.TestCase):
    def setUp(self):
        #disble images
        chrome_options = Options()
        chrome_options.add_experimental_option( "prefs", {'profile.default_content_settings.images': 2})
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
#        options=[]
#        options.append('--load-images=false')
#        self.driver=webdriver.PhantomJS(executable_path='C:\\Users\\VUGON\\Desktop\\phantomjs-2.0.0-windows\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe',service_args=options)
        self.driver.implicitly_wait(30)
        self.base_url = "https://m.facebook.com/profile.php?v=info&id=100001150323526&nocollections=1"

    
    def test_likes(self):
        driver = self.driver
        driver.get("https://m.facebook.com")
#        driver.find_element_by_name("email").clear()
#        driver.find_element_by_name("email").send_keys("facebookAccount['user']")
#        driver.find_element_by_name("pass").clear()
#        driver.find_element_by_name("pass").send_keys("password") #insert password
#        driver.find_element_by_name("login").click()
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        for id in ids:
            self._likes(driver,id)
#        self._writeData(likes)            
            
    def _writeData(self,likes):        
            with open('d:\\fbData\\allLikes_'+dateTime+'.txt', 'a+') as f:
                f.write(json.dumps(likes))
                f.closed
            
    def _likes(self,driver,id):
        driver.get("https://m.facebook.com/timeline/app_collection/?collection_token="+id+"%3A2409997254%3A96")
        
        if(driver.title=="Content Not Found"):
            return
        
        data=[]
        lengthBreak=[]
        length=0
        numberOfLikes=int(driver.find_element_by_class_name("_52jg").text.replace(",",""))
        while(True):
            #subDriver1=driver.find_elements_by_class_name("lineClampContent")
            subDriver1=driver.find_elements_by_class_name("darkTouch")
            lengthBreak.append(len(subDriver1))
            if (numberOfLikes>66):
                if(lengthBreak.count(max(set(lengthBreak)))>3 and len(data)>66) or len(lengthBreak)>227: 
                    break
            else :
                if(lengthBreak.count(max(set(lengthBreak)))>1):
                    break
            subDriver1=subDriver1[length:len(subDriver1)]
            for like in subDriver1:
                driver.execute_script("window.scrollBy(0,10000);")
                link=like.get_attribute("href")
                link=link[38:len(link)] if "=" in link else link[23:len(link)]
                if  link not in data:
                    data.append(link)                    
                    cursor.execute('''INSERT OR IGNORE INTO LIKES (LIKE_LINK) VALUES(?)''',[link] )
                    cursor.execute('''INSERT OR IGNORE INTO PEOPLE_LIKE VALUES(?,?)''',[id,link] )
                    db.commit()
                    length=len(data)
        link=driver.find_element_by_xpath("//*/a[contains(@class,'darkTouch')]").get_attribute("href")
        link=link[38:len(link)] if "=" in link else link[23:len(link)]
        data.append(link)
        cursor.execute('''INSERT OR IGNORE INTO LIKES (LIKE_LINK) VALUES(?)''',[link] )
        cursor.execute('''INSERT OR IGNORE INTO PEOPLE_LIKE VALUES(?,?)''',[id,link] )
        db.commit()
        likes.append({'id':id,'data':data})
        print("Likes_"+id+":"+str(len(data))+"/"+str(numberOfLikes))
        print(str(ids.index(id)+1)+"/"+str(len(ids)))

   
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    nose.main()
