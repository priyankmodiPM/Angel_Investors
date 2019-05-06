from selenium import webdriver
import time
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException        


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
while count<=2:
    more_buttons = driver.find_elements_by_class_name("fontello-down-dir") #finds all drop downs
    for x in more_buttons:
        x.click()
        count+=1
        time.sleep(1) #sleep to finish opening one drop down before the other


'''trying to capture elements of anchor tag(investors){not required}'''
count = 0
while count<=20:
    details = driver.find_elements_by_xpath('//a[@class="u-uncoloredLink"]')
    list_details = [x.text for x in details]
    count+=1

'''makes a dictionary of lists which stores the amount of fundings at ith index corresponding to ith done deal'''
list_amount = {}
j = 1
while(check_exists_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[1]/div/div[1]/div[2]"%(j))):
    for i in range(1,5):
        element = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[%s]/div/div[1]/div[2]"%(j,i))
        list_temp = []
        k = 1 
        while check_exists_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[2]/div[1]'%(j,i,k)):
            trial = element.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[2]/div[1]'%(j,i,k))
            k+=1
            list_temp.append(trial.text)
        list_amount[(j-1)*4+i] = list_temp
    j+=1
print(list_amount)

print("\n")

'''makes a dictionary of strings, where ith string is the name of main investor for ith company'''
list_name = {}
var = 1
while(check_exists_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[1]/div/div[1]/div[1]/div[2]/a"%(var))):
    for i in range(1,5):
        name = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[%s]/div/div[1]/div[1]/div[2]/a"%(var,i))
        list_name[(var-1)*4+i] = name.text
    var+=1
print(list_name)
