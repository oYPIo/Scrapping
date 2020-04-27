from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import re
import numpy as np
import os

dataAmount = 5000

dirName = 'ScrapedData'
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ")
else:    
    print("Directory " , dirName ,  " already exists") 

driver = Chrome()
driver.get('https://kinogo.by/')

sortByCommentsButton = driver.find_element_by_xpath('//div[@class="content"]//div[@class="mini"]//a[4]')
sortByCommentsButton.click()

lastFilmListPageLink = driver.find_element_by_xpath('//div[@class="bot-navigation"]//a[position()=last()-1]')
lastFilmListPageNumber = int(lastFilmListPageLink.get_attribute('innerHTML')) 

driver2 = Chrome() # for films on a films page
commentsAmount = 0

for filmListPage in  range(lastFilmListPageNumber): 
     
    elements = driver.find_elements_by_xpath('//div[contains(@class,"shortstory shid")]//h2[@class="zagolovki"]//a')
    filmList = [
        { 'Link': _.get_attribute('href'), 
          'Name': (_.get_attribute('innerHTML')).split('<', 1)[0]  #cut off the bug html part 
        } for _ in elements
    ]

    for film in filmList:
        driver2.get(film['Link']) #A film page
    
        lastCommentPageLink = driver2.find_element_by_xpath('//div[@class="bot-navigation"]//a[position()=last()-1]')
        lastCommentPageNumber = int(lastCommentPageLink.get_attribute('innerHTML')) 
    
        filmComments = []
        for commentPage in range(lastCommentPageNumber):   
            texts=driver2.find_elements_by_xpath(('//div[@class="comentarii"]/div/div'))
            texts=[_.text for _ in texts]
            
            if( not texts): break
            filmComments += texts
        
            try:
                goNextPageButton = driver2.find_element_by_xpath('//div[@class="bot-navigation"]//a[contains(text(), "Позже")]')          
                goNextPageButton.click()
            except:break  #you on the last page
    
        comm = np.array(filmComments)
        for i in range(comm.size):
            file=open( dirName+'/'+ film['Name'] + '_' + str(i) +'.txt',"w+")
            file.write(str(comm[i]))
            file.close()
    
        commentsAmount += len(filmComments) 
        if(commentsAmount >= dataAmount): break;
    
    try:
        goNextPageButton = driver.find_element_by_xpath('//div[@class="bot-navigation"]//a[contains(text(), "Позже")]')          
        goNextPageButton.click()
    except:
        print('End of the list filmListPage')
        break 
    
    if(commentsAmount >= dataAmount): break;    

input("Press any key")
driver2.close()
driver.close()

