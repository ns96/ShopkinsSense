# Shopkins Sense -- Detecting Shopkins Characters Using Machine Vision

## Introduction
Shopkins are pint size toy characters modeled after daily household items that are sold at stores. They include designs taken from health and beauty products, items in the freezer, items in a pantry, hats, bags, shoes etc.... In recent years they have become extremely popular among young children, with more than 600 characters now on the market.  Their share numbers and small size make naming them a challenge since there is no room to place names on the shopkins characters. Unfortunately, shot of manually going through a list images there is no quick way to do this. As such, a prototype web application which uses machine vision to help quickly identify shopkins is being developed.

## Techinical Approach
The core of the machine version program was developed using Python and the OpenCV library. A database of over 600 shopkins character images and information was constructed by webscraping the Shopkins world site using Selenium. Two methods were initially tested for feature extraction from images, colored histograms and the SIFT method. Though the use of colored histograms has been shown to be very good at building basic image search engines, this technique proved unfeasible. The same shopkins character is available in various colors, making histogram based comparisons unreliable. The SIFT method proved more reliable, since it is based on detecting objects irrespective of color, orientation, and scale. The flask framework was used to build a simple web application for accessing the machine learning functionality. Additionally, a mobile application is being developed for accessing this functionality in a more mobile friendly manner. The web application is currently being hosted on a Raspberry Pi 3 computer (http://home25p01.quickddns.com:5000/).

## Initial Results
By leveraging the machine version functionality of OpenCV/Python, it is surprising easy to build simple web application which automates the task of identifying Shopkins characters. Though the accuracy is still not as good as can be, it shows there is potential for such a tool. A more sophisticated deep neural network based program could probable achieved better results, but this would require vastly more data (images of shopkins characters) to properly train the model. 

## Next Steps
Plan for the immediate future are to
* Improve the search performance by playing around with the input parameters
* Build a mobile application which makes use of the web application
* Host the application on a more powerful server instead of the raspberry pi

## Running
To run tis application locally
* change to directory where code was downloaded
* execute python shopkins_app.py

On the Raspberry Pi 3 it takes about 12 mins to start web application since feature extraction needs to be done on 600+ character images.
