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


'''trying to capture elements of anchor tag(investors){not required}'''
count = 0
while count<=20:
    details = driver.find_elements_by_xpath('//a[@class="u-uncoloredLink"]')
    list_details = [x.text for x in details]
    count+=1


'''makes a dictionary of lists which stores the amount of fundings at ith index corresponding to ith done deal'''
dict_amount = {} #initializing empty dict
j = 1 #keeps count of the row of done deals(1 row has 4 entries on the webpage)
while(check_exists_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[1]/div/div[1]/div[2]"%(j))):
    for i in range(1,5): #iterate over the 4 done deals in each row
        element = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[%s]/div/div[1]/div[2]"%(j,i)) #finds the text part of the done deal
        list_temp = [] #stores the amount entries for a done deal
        k = 1 #counter to iterate over the amount entries found
        while check_exists_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[2]/div[1]'%(j,i,k)): #check if the amount entry exists(to know when to stop)
            trial = element.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[2]/div[1]'%(j,i,k)) #finds the k'th entry
            k+=1
            list_temp.append(trial.text)
        dict_amount[(j-1)*4+i] = list_temp #add the list of amount entries at index {4(j-1)+1}(4*row number + i'th element of row)
    j+=1
print(dict_amount) #test dict_amount

print("\n")

'''makes a dictionary of the dates for certain funding, not acquired'''
dict_dates_amount = {} #initializing empty dict
j = 1 #keeps count of the row of done deals(1 row has 4 entries on the webpage)
flag = 0
while(check_exists_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[1]/div/div[1]/div[2]"%(j))):
    for i in range(1,5): #iterate over the 4 done deals in each row
        element = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[%s]/div/div[1]/div[2]"%(j,i))
        list_temp = [] #stores the date entries for a done deal
        k = 1  #counter to iterate over the date entries found
        while (check_exists_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[1]'%(j,i,k)) and driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[2]'%(j,i,k)).text != "Acquired" and driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[2]'%(j,i,k)).text != "Acquired\nREAD PRESS"):
            date = element.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[1]'%(j,i,k))
            k+=1
            list_temp.append(date.text)
        dict_dates_amount[(j-1)*4+i] = list_temp #add the list of date entries at index {4(j-1)+1}(4*row number + i'th element of row)
    j+=1
print(dict_dates_amount) #test dict_dates_amount

print("\n")

'''makes a dictionary of strings, where ith string is the name of main investor for ith company'''
dict_name = {}
var = 1
while(check_exists_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[1]/div/div[1]/div[1]/div[2]/a"%(var))):
    for i in range(1,5):
        name = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[%s]/div/div[1]/div[1]/div[2]/a"%(var,i))
        dict_name[(var-1)*4+i] = name.text
    var+=1
print(dict_name)

print("\n")

'''makes a dictionary of lists which stores the names of companies which provide the fundings at ith index corresponding to ith done deal'''
dict_companies = {}
j = 1 #keeps count of the row of done deals(1 row has 4 entries on the webpage)
while(check_exists_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[1]/div/div[1]/div[2]"%(j))):
    for i in range(1,5): #iterate over the 4 done deals in each row
        element = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[%s]/div/div[1]/div[2]"%(j,i))
        k = 1 #counter to iterate over the date entries found
        list_ordered_pairs = [] #initializing the list of order pairs (eg: [(1,[GV,Kapor]),(2,[GV,Homebrew])])
        while k<=len(dict_dates_amount[(j-1)*4+i]): #iterate till dates are over
            t = 1 #counter to iterate over investors corresponding to k'th funding amount
            list_temp = [] #initializing list_temp which stores all the investors for k'th funding amount of i'th companies
            while t<=10:
                if check_exists_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[2]/div[%s]/a'%(j,i,k,t)): #checks existence of 
                    trial = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[2]/div[%s]/a'%(j,i,k,t))
                    
                    if trial.text != "READ PRESS":
                        list_temp.append(trial.text)
                    t+=1
                # elif check_exists_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[%s]/div/div[1]/div[2]/div/div/div[2]/div[%s]/a'%(j,i,t)):
                #     if(k==1):
                #         print("yes2,i=",(j-1)*4+i)
                #     trial = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[%s]/div[%s]/div/div[1]/div[2]/div/div/div[2]/div[%s]/a'%(j,i,t))
                #     if trial.text != "READ PRESS":
                #         list_temp.append(trial.text)
                #     t+=1
                else:
                    t+=1

            list_ordered_pairs.append((k,list_temp))
            k+=1
        dict_companies[(j-1)*4 + i] = (list_ordered_pairs)
    j+=1
print(dict_companies)
