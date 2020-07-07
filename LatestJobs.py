import time
from selenium import webdriver
import csv

from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
chrome_browser = webdriver.Chrome('./chromedriver', options=options)


#chrome_browser = webdriver.Chrome('./chromedriver')
#chrome_browser.maximize_window()
chrome_browser.get('https://nl.linkedin.com/jobs/test-engineer-jobs?sortBy=DD&f_TP=1%2C2&position=1&pageNum=0')
time.sleep(3)

ul_list = chrome_browser.find_element_by_xpath('//ul[@class ="jobs-search__results-list"]')
jobsdesc = ul_list.find_elements_by_tag_name("li")

# function to retrieve the elements like title,company,location and joblink from the jobsearchlist and writing to dictionary
def retrievejobdetails(jobs):
    finalsearch = []
    for i in range(len(jobsdesc)):
         splittext = []
         splittext = (jobsdesc[i].text).split('\n')
         jobtitle = splittext[0]
         company =splittext[1]
         location = splittext[2]
         joblink = jobsdesc[i].find_element_by_tag_name('a').get_attribute('href')
         finalsearch.append({'jobtitle':jobtitle,'company':company,'location':location,'joblink':joblink})
    return(finalsearch)

# create database.csv file and write the latest jobdetails  to the file
def writetocsv(filetowrite):
    with open('database.csv', newline="", mode='a') as csvfile:
        csvfile.seek(0)
        csvfile.truncate()
        writer = csv.DictWriter(csvfile, fieldnames=["JOBTITLE", "COMPANY", "LOCATION","JOBLINK"])
        writer.writeheader()
        for item in filetowrite:
            title = item["jobtitle"]
            company = item["company"]
            loc = item["location"]
            link =item["joblink"]
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([title, company, loc,link])

writetocsv(retrievejobdetails(jobsdesc))
print("job done")

chrome_browser.close()





