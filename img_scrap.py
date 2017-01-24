# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 12:55:35 2017

simple class to webscrap shopkins images and names

@author: nathan
"""
import sys
import urllib
import time
import unicodecsv as csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# the file to save records to
img_dir = 'data/query_images/'
data_file = 'data/shopkins.csv'

# load the first page with images
url = "http://myshopkinslist.shopkinsworld.com/"

browser = webdriver.Chrome()

# dictionary that store all the shopkins
shopkins = {}

# save shopkins records to CSV files
def saveRecordsToCSV(records):
    try:    
        fieldnames = ['name', 'pid', 'img_files', 'series', 
                      'team', 'range']
    
        with open(data_file, 'wb') as out_file:
            csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
            csvwriter.writeheader()   
    
            for row in records:
                csvwriter.writerow(row)
        
            out_file.close()
    except:
        e = sys.exc_info()[0]
        print 'file %s, %s' % (filename, e)

'''
# function to extract features from the images
def extractFeatures(filename):
    img = cv2.imread(filename, 0)
    kps, des = sift.detectAndCompute(img, None)
    return (kps, des)
'''

# iterate through all the pages loading all shopkins data
for i in range(1,85):
    browser.get(url + str(i))

    timeout = 20
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'character-list'))
        WebDriverWait(browser, timeout).until(element_present)
    except TimeoutException:
        print "Timed out waiting for page to load"
        quit()

    # now process the page shopkins
    elms = browser.find_elements_by_css_selector('.character-image.inline')
    print '#Shopkins found ', len(elms)

    for elm in elms:
        print elm.tag_name
        pid = elm.get_attribute('data-product-id')
        name = elm.get_attribute('data-name')
        img_url = elm.get_attribute('data-image')
        series = elm.get_attribute('data-series')
        team = elm.get_attribute('data-team')
        item_range = elm.get_attribute('data-range')
        
        print name, img_url
    
        # save the image locally
        basename = name.replace(' ', '_').lower() + '_' + pid + '.png'
        filename = img_dir + basename
        urllib.urlretrieve(img_url, filename)
        
        # save this to the data diictionary now
        if name not in shopkins:
            shopkin = {}
            
            shopkin['name'] = name
            shopkin['pid'] = pid
            shopkin['img_files'] = basename
            shopkin['series'] = series
            shopkin['team'] = team
            shopkin['range'] = item_range
            
            shopkins[name] = shopkin
        else:
            shopkin = shopkins[name]
            img_files = shopkin['img_files'] + ';' + basename
            shopkin['img_files'] = img_files
        
        # pause for few seconds
        time.sleep(2)
        
    # save dictionary as csv file now incase we crash
    saveRecordsToCSV(shopkins.values())

# debug code
#import pprint
#pp = pprint.PrettyPrinter(depth=6)
#pp.pprint(shopkins) 

# do a final save of the dictionary now 
saveRecordsToCSV(shopkins.values())

#with open(data_file, 'wb') as handle:
#    pickle.dump(shopkins, handle, protocol=pickle.HIGHEST_PROTOCOL)

#with open('filename.pickle', 'rb') as handle:
#    b = pickle.load(handle)
            
            
