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
from resource import facebookAccount
import nose,sqlite3

reviews=[]
db=sqlite3.connect("d://HelloWorldDb")
cursor=db.cursor()

class Reviews(unittest.TestCase):
    def setUp(self):
        #disble images
        chrome_options = Options()
        chrome_options.add_experimental_option( "prefs", {'profile.default_content_settings.images': 2})
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
#        options=[]
#        options.append('--load-images=false')
#        self.driver=webdriver.PhantomJS(executable_path='C:\\Users\\VUGON\\Desktop\\phantomjs-2.0.0-windows\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe',service_args=options)
        self.driver.implicitly_wait(0)
        self.base_url = "https://m.facebook.com/profile.php?v=info&id=100001150323526&nocollections=1"

    
    def test_reviews(self):
        driver = self.driver
        driver.get("https://m.facebook.com")
#        driver.find_element_by_name("email").clear()
#        driver.find_element_by_name("email").send_keys("facebookAccount['user']")
#        driver.find_element_by_name("pass").clear()
#        driver.find_element_by_name("pass").send_keys("facebookAccount['password']") 
#        driver.find_element_by_name("login").click()
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        for id in ids:
            self._reviews(driver,id)
        self._writeData(reviews)            
            
    def _writeData(self,reviews):        
            with open('d:\\fbData\\reviews_'+dateTime+'.txt', 'a+') as f:
                f.write(json.dumps(reviews))
                f.closed
    
    def _reviews(self,driver,id):
        driver.get("https://m.facebook.com/timeline/app_collection/?collection_token="+id+"%3A254984101287276%3A105")
        
#        if(driver.title=="Content Not Found"):
#            return
            
        data=[]
        lengthBreak=[]
        length=0
        try:
            numberOfReviews=int(driver.find_element_by_class_name("_52jg").text)
            while(True):
                subDriver1=driver.find_elements_by_xpath("//*/a[contains(@class,'_373r')]")
                lengthBreak.append(len(subDriver1))
                if (numberOfReviews>12):
                    if(lengthBreak.count(max(set(lengthBreak)))>2 and len(data)>12) or len(lengthBreak)>77: 
                        break
                else :
                    if(lengthBreak.count(max(set(lengthBreak)))>1):
                        break
                subDriver1=subDriver1[length:len(subDriver1)]
                for reviewItem in subDriver1:
                    driver.execute_script("window.scrollBy(0,10000);")
                    link=reviewItem.get_attribute("href")
                    link=link[link.find("activity/")+9:len(link)]
                    name=reviewItem.find_element_by_class_name("_373u").text
                    rating=reviewItem.find_element_by_class_name("_42ng").text
                    name=name.replace("\n"+rating,"")
                    rating=int(rating[0:rating.index(" ")])
                    review={'link':link,'name':name,'rating':rating}
                    cursor.execute('''INSERT OR IGNORE INTO REVIEWS VALUES(?,?,?)''',[name,link,rating] )
                    cursor.execute('''INSERT OR IGNORE INTO PEOPLE_REVIEW VALUES(?,?)''',[id,name] )
                    db.commit()
                    if(review not in data):
                        data.append(review)
                    length=len(data)
        except:
            return
        reviews.append({'id':id,'data':data})
        print("Reviews_"+id+":"+str(len(data))+"/"+str(numberOfReviews))
        print(str(ids.index(id)+1)+"/"+str(len(ids)))                        
                    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    nose.main()

## need upgrade