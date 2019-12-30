# Created by: Thomas Opolski
# Date Created: 12/27/19
# Date Modified: 12/27/19

# Program Description: The idea starts with a basic youtube link parser that gets all
# videos within a certain search criteria, puts them in a list, and downlaods 
# them to be processed and analyzed.

import requests
from bs4 import BeautifulSoup
import webbrowser
import pafy
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from tkinter import *

#global definitions
tcgCodeQREnabled = True
websiteQREnabled = True

def getQrDataSet(play):
    qrDataSet = set()

    cap = cv2.VideoCapture(play.url)
    while(True):
        ret,frame = cap.read()
        if frame is None:
                break

        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.imshow('videoFramesAnalyzed',frame)
        #check qr code
        decodeObj = pyzbar.decode(frame)

        if len(decodeObj) > 0:
            decodedData = decodeObj[0]
            decodedString = str(decodedData)

            if len(decodedString) > 20:

                #Website URL Scraping
                if (websiteQREnabled):
                    myWebLink = ''
                    
                    if decodedString[15:19] == 'http':
                        i = 15
                        #read until apostrophe
                        while (decodedString[i] != "'") :
                            myWebLink += decodedString[i]
                            i += 1
                        
                        qrDataSet.add(myWebLink)

                #PKMN TCG Code Scraping
                if (tcgCodeQREnabled):
                    if decodedString[18] == '-' and decodedString[23] == '-' \
                        and decodedString[27] == '-':
                            
                        print(decodedString[15:31])
                        qrDataSet.add(decodedString[15:31])
        
    cap.release()
    cv2.destroyAllWindows()

    return qrDataSet

def getFromURL(myURL):
    myURL = 'https://www.youtube.com/watch?v=NUSKZMAd-Hs'

    video = pafy.new(myURL)

    play = video.getbest(preftype="webm")
    if (play == None):
        play = video.getbest(preftype="mp4")

    qrDataSet = getQrDataSet(play)

    return qrDataSet

def getFromSearch(myURL):

    #setting up beautiful soup
    result = requests.get(myURL)
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')

    #list of urls
    urls = []

    #finding h3 tag for listed video content
    for h3_tag in soup.find_all("h3"):
        a_tag = h3_tag.find('a')
        if(a_tag):
            urls.append('https://youtube.com' + a_tag.attrs['href'])

    print(urls)

    #set shortest to first element
    shortest = pafy.new(urls[0])
    print(shortest.length)
    for url in urls[1:]:
        video = pafy.new(url)
        print(video.length)
        if (video.length < shortest.length and video.length != 0.0):
            shortest = video

    #for downloading all videos
    # for url in urls:
    #     video = pafy.new(url)
        
    print("Video to scrape: " + shortest.title)
    print(shortest.duration)

    play = shortest.getbest(preftype="webm")
    if (play == None):
        play = shortest.getbest(preftype="mp4")

    qrDataSet = getQrDataSet(play)

    return qrDataSet


def main():

    #saved url: https://www.youtube.com/results?search_query=pokemon+card+opening&sp=CAISBAgBEAE%253D
    #saved myURL: https://www.youtube.com/results?search_query=oogaboogaroogatooga12345&sp=QgIIAQ%253D%253D
    qrDataSet = getFromSearch("https://www.youtube.com/results?search_query=oogaboogaroogatooga12345&sp=QgIIAQ%253D%253D")

    for qrData in qrDataSet:
            print(qrData)


    



if __name__ == "__main__" :
    main()