# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 09:29:53 2017

@author: nathan
"""
import numpy as np
import cv2
import csv
import os.path
from draw_match import drawMatches

# set the max number of onjects to load
MAX_DATA = 1000

# stores a list of features for searching
shopkins = []
shopkins_page = ''

# Initiate SIFT detector
sift = cv2.SIFT()

# BFMatcher with default params
bf = cv2.BFMatcher()

def loadHomepageData():
    '''
    Load the data is the csv file into a dictionary keyed by team
    '''
    shopkins_dict = {}

    print '\nLoading shopkins page data ...'
    
    with open('static/shopkins.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader, None)  # skip the headers        
        
        for row in reader:
            shopkin = {}
            team = row[4]

            shopkin['name'] = row[0]
            shopkin['pid'] = row[1]
            shopkin['img_files'] = row[2]
            shopkin['series'] = row[3]
            shopkin['team'] = team
            shopkin['range'] = row[5]
            
            if team not in shopkins_dict:
                team_list = []
                team_list.append(shopkin)
                shopkins_dict[team] = team_list
            else:
                team_list = shopkins_dict[team]
                team_list.append(shopkin)
    
    # return the list
    print 'done loading page data'
    return shopkins_dict
    
def loadData():
    '''
    load csv file containing data
    '''
    global shopkins
    dcount = 0 # used for
    
    print '\nLoading image data ...'
    
    with open('static/shopkins.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader, None)  # skip the headers        
        
        for row in reader:         
            dcount += 1
            if(dcount > MAX_DATA):
                break
                
            #filename = 'static/real_images/' + row[0].replace(' ', '_').lower() + '.jpg'
            #if not os.path.isfile(filename):
            #    continue
            
            filename = 'static/query_images/' + row[2].split(';')[0]          
            
            # extract features from thr shopkin image
            img = cv2.imread(filename, 0)
            kps, des = sift.detectAndCompute(img, None)
            
            shopkin = {}
            
            shopkin['name'] = row[0]
            shopkin['pid'] = row[1]
            shopkin['img_files'] = row[2]
            shopkin['series'] = row[3]
            shopkin['team'] = row[4]
            shopkin['range'] = row[5]
            shopkin['img'] = img
            shopkin['kps'] = kps
            shopkin['des'] = des
            
            shopkins.append(shopkin)
            
            if dcount%100 == 0:
                print dcount, 'Image files loaded ... '
            #print 'data loaded ', row[0], filename
    
    print 'Done loading data ... size %d' % (len(shopkins))

def findMatches(queryDes, trainDes):
    ''' 
    return the best matches based on the features along
    with the match indexes needed to compute the score
    desA is the train image features and desB in the query image features
    '''
    matches = bf.knnMatch(queryDes, trainDes, k=2)

    # Apply ratio test then get the bext matches and indexes
    good_matches = []
    match_indexes = []
    
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good_matches.append(m)
            match_indexes.append((m.queryIdx, m.trainIdx))
        
    #print 'Number of good matches',len(good_matches)
    return (good_matches, match_indexes)
    
def getScore(queryKps, trainKps, match_indexes): 
    '''
    get the scores of the matches found
    kpsA is the train image points and kpsB in the query image points
    '''
    ptsA = np.float32([queryKps[i].pt for (i, _) in match_indexes])
    ptsB = np.float32([trainKps[j].pt for (_, j) in match_indexes])
    
    (_, status) = cv2.findHomography(ptsA, ptsB, cv2.LMEDS, 0.0)
    #(_, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, 0.0)

    return float(status.sum()) / status.size


def search(t_kps, t_des, team = 'ALL'):
    '''
    search through the query images and return a list top 10 matches
    '''
    # stores the results
    results = []
    
     # try to find the query image in this train image and report score
    for shopkin in shopkins:
        # filter by team
        shopkin_team = shopkin['team'].replace(' ', '_').lower()
        if team != 'ALL' and team != shopkin_team:
            continue
        
        shopkin['score'] = 0
        shopkin['matches'] = None
        
        #print 'Searching for: ', shopkin['name']
        q_kps = shopkin['kps'] 
        q_des = shopkin['des']
        
        matches, match_indexes = findMatches(q_des, t_des)
        
        if len(matches) > 8:
            score = getScore(q_kps, t_kps, match_indexes)
            #print 'Number of matches', len(matches) 
            #print 'Match Score', score, '%\n'
            shopkin['matches'] = matches
            shopkin['score'] = score
            results.append(shopkin)
    
    # sort by score then matches
    results.sort(key = lambda x: x['score'], reverse=True)    
    results.sort(key = lambda x: len(x['matches']), reverse=True)
    
    # take top six and once again sort by score
    #results = results[:8]
    #results.sort(key = lambda x: x['score'], reverse=True)     
    return results[:10]

def searchFor(train_img, team):
    '''
    function to search a particular train image
    '''
    print '\n\nProcessing Train Image: ', train_img
    
    t_img = cv2.imread(train_img, 0)
    t_kps, t_des = sift.detectAndCompute(t_img, None)
    
    return search(t_kps, t_des, team)

def scaleImage(filename):
    '''
    Scales and image to about 400 x 400 to save space and
    make searching a bit more accurate
    '''
    img = cv2.imread(filename)
    r = 400.0 / img.shape[1]
    dim = (400, int(img.shape[0] * r))
    scaled_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    #dn, fn = os.path.split(filename)    
    cv2.imwrite(filename, scaled_img)

# test code

'''   
# main function for testing
if __name__ == '__main__':
    train_imgs = ['test.jpg']
    
    # start code execution here
    loadData()

    # for each of the train images try to find matches
    for train_img in train_imgs:
        train_img = 'static/uploads/' + train_img
        t_img = cv2.imread(train_img, 0)
        t_kps, t_des = sift.detectAndCompute(t_img, None)
    
        print '\n\nProcessing Train Image: ', train_img
        
        results = search(t_kps, t_des, 'ALL')
        
        print '\n\nResults Found ', len(results)
        for shopkin in results:
            print shopkin['name'], '/ Team:', shopkin['team'], '>> score', shopkin['score'], '# matches', len(shopkin['matches'])
    
        if len(results) > 0:
            shopkin = results[2]
            drawMatches(shopkin['img'],shopkin['kps'], t_img, t_kps, shopkin['matches'])
    
    #raw_input("Press Enter to continue...")

# Draw first 10 matches.
#drawMatches(img1,kp1,img2,kp2, matches)
'''