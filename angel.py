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

def check_exists_by_class_name(class_name):
    try:
        webdriver.find_element_by_class_name(class_name)
    except NoSuchElementException:
        return False
    return True

'''Open webdriver and request url'''
# specify the driver path according to system of use
driver = webdriver = webdriver.Firefox(executable_path = '/home/priyank/gecko/geckodriver')
driver.get('https://angel.co/done-deals/new-press')


'''finding the 'see more' buttons and 'details' buttons and click them'''
count = 0 #specify count to stop searching after a limit.
try:
    while check_exists_by_class_name("fontello-down-dir"):
    # while count<=30:
        more_buttons = driver.find_elements_by_class_name("fontello-down-dir") #finds all drop downs
        for x in more_buttons:
            x.click()
            # count+=1
            time.sleep(1) #sleep to finish opening one drop down before the other
except:
    print("a")
    pass


'''makes a dictionary of lists which stores the amount of fundings at ith index corresponding to ith done deal'''
dict_amount = {} #initializing empty dict
p = 4
while(check_exists_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[1]/div[1]/div/div[1]/div[2]"%(p))):
    for j in range(1,5):
        for i in range(1,5): #iterate over the 4 done deals in each row
            if check_exists_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]"%(p,j,i)):
                # print("1")
                element = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]"%(p,j,i)) #finds the text part of the done deal
                list_temp = [] #stores the amount entries for a done deal
                k = 1 #counter to iterate over the amount entries found
                while check_exists_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[2]/div[1]'%(p,j,i,k)): #check if the amount entry exists(to know when to stop)
                    trial = element.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[2]/div[1]'%(p,j,i,k)) #finds the k'th entry
                    k+=1
                    list_temp.append(trial.text)
                dict_amount[(p-4)*16+(j-1)*4+i] = list_temp #add the list of amount entries at index {4(j-1)+1}(4*row number + i'th element of row)

            else:
                pass
    p+=1
# print(dict_amount) #test dict_amount

# print("\n")

'''makes a dictionary of the dates for certain funding, not acquired'''
dict_dates_amount = {} #initializing empty dict
p = 4
while(check_exists_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[1]/div[1]/div/div[1]/div[2]"%(p))):
    for j in range(1,5):
        for i in range(1,5): #iterate over the 4 done deals in each row
            if check_exists_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]"%(p,j,i)):            
                # print("2")
                element = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]"%(p,j,i))
                list_temp = [] #stores the date entries for a done deal
                k = 1  #counter to iterate over the date entries found
                while (check_exists_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[1]'%(p,j,i,k)) and driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[2]'%(p,j,i,k)).text != "Acquired" and driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[2]'%(p,j,i,k)).text != "Acquired\nREAD PRESS"):
                    date = element.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[1]'%(p,j,i,k))
                    k+=1
                    list_temp.append(date.text)
                dict_dates_amount[(p-4)*16+(j-1)*4+i] = list_temp #add the list of date entries at index {4(j-1)+1}(4*row number + i'th element of row)
            else:
                pass
    p+=1
# print(dict_dates_amount) #test dict_dates_amount
# print("\n")

'''makes a dictionary of strings, where ith string is the name of main investor for ith company'''
dict_name = {}
p = 4
while(check_exists_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[1]/div[1]/div/div[1]/div[2]"%(p))):
    for var in range(1,5):
        for i in range(1,5):
            if check_exists_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]"%(p,var,i)):
                # print("3")
                name = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[1]/div[2]/a"%(p,var,i))
                dict_name[(p-4)*16+(var-1)*4+i] = name.text
            else:
                pass
    p+=1
# print(dict_name)
# print("\n")

'''makes a dictionary of lists which stores the names of companies which provide the fundings at ith index corresponding to ith done deal'''
dict_companies = {}
p = 4
while(check_exists_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[1]/div[1]/div/div[1]/div[2]"%(p))):
    for j in range(1,5):
        for i in range(1,5): #iterate over the 4 done deals in each row
            if check_exists_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]"%(p,j,i)):
                # print("4")
                element = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]"%(p,j,i))
                k = 1 #counter to iterate over the date entries found
                list_ordered_pairs = [] #initializing the list of order pairs (eg: [(1,[GV,Kapor]),(2,[GV,Homebrew])])
                while k<=len(dict_dates_amount[(p-4)*16+(j-1)*4+i]): #iterate till dates are over
                    t = 1 #counter to iterate over investors corresponding to k'th funding amount
                    list_temp = [] #initializing list_temp which stores all the investors for k'th funding amount of i'th companies
                    while t<=10:
                        if check_exists_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[2]/div[%s]/a'%(p,j,i,k,t)): #checks existence of 
                            trial = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[2]/div[%s]/a'%(p,j,i,k,t))
                            
                            if trial.text != "READ PRESS":
                                list_temp.append(trial.text)
                            t+=1
                        else:
                            t+=1

                    list_ordered_pairs.append((k,list_temp))
                    k+=1
            else:
                pass
            dict_companies[(p-4)*16+(j-1)*4 + i] = (list_ordered_pairs)
    p+=1
# print(dict_companies)

# print("\n")

'''makes a dictionary telling when a company was acquired'''
dict_company_acquired_date = {}
p = 4
while(check_exists_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[1]/div[1]/div/div[1]/div[2]"%(p))):
    for j in range(1,5):
        for i in range(1,5): #iterate over the 4 done deals in each row
            if check_exists_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]"%(p,j,i)):
                # print("5")
                element = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]"%(p,j,i))

                if check_exists_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[2]'%(p,j,i,len(dict_dates_amount[(p-4)*16+(j-1)*4+i])+1)) and (driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[2]'%(p,j,i,len(dict_dates_amount[(p-4)*16+(j-1)*4+i])+1)).text == "Acquired" or "Acquired\nREAD PRESS" or driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[2]'%(p,j,i,len(dict_dates_amount[(p-4)*16+(j-1)*4+i])+1)).text.split(" ")[0] == "Acquired"):
                    dict_company_acquired_date[(p-4)*16+(j-1)*4+i] = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[%s]/div[%s]/div[%s]/div/div[1]/div[2]/div/div[%s]/div[1]'%(p,j,i,len(dict_dates_amount[(p-4)*16+(j-1)*4+i])+1)).text
    p+=1
# print(dict_company_acquired_date)

with open('angel.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow(['Name','Acquried Date','Fund1','Date1','investor11','investor12','investor13','fund2','date2','investor21','investor22','investor23','fund3','date3','investor31','investor32','investor33'])
    for i in range(1,len(dict_name)+1):
        row = []
        row.append(dict_name[i])
        try:
            row.append(dict_company_acquired_date[i])
        except:
            row.append('Not Acquired')
        for j in range(3):
            try:
                row.append(dict_amount[i][j])
            except:
                row.append('N/A')
            try:
                row.append(dict_dates_amount[i][j])
            except:
                row.append('N/A')
            for k in range(3):
                try:
                    row.append(dict_companies[i][j][1][k])
                except:
                    row.append('N/A')
        writer.writerow(row)