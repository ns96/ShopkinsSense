# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 10:58:40 2017

@author: nathan
"""
import os
import orb_match
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

# set the file where files are uploaded
UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

shopkins_page = ''
team_list = []

def generateShopkinsPage():
    '''generate page which loads all the shopins'''
    global shopkins_page, team_set
    
    print '\nGenerating shopkins page ...'
    
    data = orb_match.loadHomepageData()
    
    for team in data:
        team_list.append(team)
        shopkins = data[team]    
        
        shopkins_page += '<hr><h3>Team: ' + team + ' / Count: ' + str(len(shopkins)) + '<h3><hr>' 
        
        for shopkin in shopkins:
            shopkins_page += '<h4>Name: ' + shopkin['name'] + ' / Series: ' +\
                shopkin['series'] + ' / Team: ' + team + '</h4>'
                
            for img in shopkin['img_files'].split(';'):
                img = '/static/query_images/' + img
                shopkins_page += '<img src="'+ img + '" width="10%">'
                
            shopkins_page += '<hr>'
    
    # add the teams
    shopkins_page = '<h3>' + ' | '.join(team_list) + '</h3><hr>' + shopkins_page    
    
    print 'Done generating page ...'

# load the csv file with the data
def loadData():
    generateShopkinsPage()
    orb_match.loadData()

def doSearch(img_file, team):
    '''
    Method to actual conduct search through database
    '''
    results = orb_match.searchFor(img_file, team)
    
    text = '[0] <img src="/' + img_file + '" width="15%"> Search Image / Team: ' + team + '<hr><hr>'
    
    i = 0
    for shopkin in results:
        i += 1
        img = '/static/query_images/' + shopkin['img_files'].split(';')[0]        
        text += '[' + str(i) + '] <img src="'+ img + '" width="10%">'
        
        text += shopkin['name'] + ' / Team: ' + shopkin['team'] +\
            ' >> Score: ' + str(shopkin['score']) +\
            ' # Matches: ' + str(len(shopkin['matches'])) +\
            '<br><br><hr>'
    
    return text
    
@app.route("/search/<string:filename>/<string:team>")
def search(filename, team):
    img_file = UPLOAD_FOLDER + filename 
    return doSearch(img_file, team)

@app.route("/test/<string:filename>/<string:team>")
def testSearch(filename, team):
    img_file = 'static/test_images/' + filename 
    return doSearch(img_file, team)

def show_upload_form():
    html = """
    <!doctype html>
    <title>Upload new File</title>
    <h2>Upload Shopkin Image</h2>
    <form method=post enctype=multipart/form-data>
      <p>
      %s
      <input type=file name=file>
      <input type=submit value=Search>
      </p>
    </form>
    """
    
    team_select = 'Select Team <select name="team">'
    team_select += '<option value="ALL">ALL</option>'    
    for team in team_list:
        team_norm = team.replace(' ', '_').lower()
        team_select += '<option value="' + team_norm + '">' + team + '</option>'
    team_select += '</select>'
    
    return html % (team_select)
       
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
            
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file:
            team = request.form.get("team")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # rescale the image
            orb_match.scaleImage(app.config['UPLOAD_FOLDER'] + filename)            
            
            return redirect(url_for('search',
                                    filename = filename,
                                    team = team))
    
    # if no form submital just display the upload form                                
    return show_upload_form()
   
@app.route('/')
def homepage():    
    return shopkins_page

if __name__ == '__main__':
    loadData()
    app.run(use_reloader=True)
