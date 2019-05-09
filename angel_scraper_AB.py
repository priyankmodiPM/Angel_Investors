# from selenium import webdriver
# import time
# from selenium.common.exceptions import WebDriverException

# # Open webdriver and request url
# driver = webdriver = webdriver.Firefox(executable_path = '/home/priyank/gecko/geckodriver')
# # driver.Chrome('C:/Users/31162/Downloads/chromedriver_win32/chromedriver')
# driver.get('https://angel.co/done-deals/new-press')

# next_index = 0

# while True:
#     try:
#         more = driver.find_element_by_xpath(r'//*[@id="root"]/div[4]/div[2]'\
#             '/div/div/div/div/a[2]')
#     except WebDriverException:
#         time.sleep(2)
#         continue

#     more.click()
#     time.sleep(2)


#     # finding the "DETAILS" elements and clicking them
#     elements = driver.find_elements_by_xpath(r'//*[contains(concat( " ", @class, " " ), concat( " ", "u-textAlignCenter", " " )) and contains(concat( " ", @class, " " ), concat( " ", "u-uppercase", " " ))]')[next_index:]
#     #elements = list(filter(lambda x: x.text=='DETAILS', elements))[next_index:]

#     for element in elements:
#         element.click()
#         time.sleep(0.5)

#     # Main details to be scraped after dropdowns are clicked
#     new_elements = driver.find_elements_by_xpath(r'//*[contains(concat( '\
#             '" ", @class, " " ), concat( " ", "s-grid-colMd12", " " ))]')\
#             [next_index:]

#     text = open('details.txt', 'a')
#     text.write('\n\n'.join(str(i) for i in map(lambda x: x.text,\
#             new_elements)))

#     next_index += len(list(elements))

from selenium import webdriver
import time
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException        
import csv
import io
import codecs

'''checks for validity of a given xpath'''
def check_exists_by_xpath(xpath):
    try:
        webdriver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


'''Open webdriver and request url'''
# specify the driver path according to system of use
driver = webdriver = webdriver.Firefox(executable_path = '/home/priyank/gecko/geckodriver')
driver.get('https://angel.co/done-deals/new-press')


'''finding the 'see more' buttons and 'details' buttons and click them'''
count = 0 #specify count to stop searching after a limit.
while count<=1:
    more_buttons = driver.find_elements_by_class_name("fontello-down-dir") #finds all drop downs
    for x in more_buttons:
        x.click()
        count+=1
        time.sleep(1) #sleep to finish opening one drop down before the other

x = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[2]/div[1]/div/div[1]/div[2]/div/div/div[2]/div[2]/a')
print(x.text)