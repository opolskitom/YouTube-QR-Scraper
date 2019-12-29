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

def main():

    #setting up beautiful soup
    #saved url: https://www.youtube.com/results?search_query=pokemon+card+opening&sp=CAISBAgBEAE%253D
    result = requests.get("https://www.youtube.com/results?search_query=oogaboogaroogatooga1234")
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
    print(shortest.length)
    print(shortest.duration)

    play = shortest.getbest(preftype="webm")
    if (play == None):
        play = shortest.getbest(preftype="mp4")

    
    codes = set()

    cap = cv2.VideoCapture(play.url)
    while(True):
        ret,frame = cap.read()
        if frame is None:
                break

        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.imshow('video',frame)
        #check qr code
        decodeObj = pyzbar.decode(frame)

        if len(decodeObj) > 0:
            decodedData = decodeObj[0]
            decodedString = str(decodedData)

            if len(decodedString) > 18:

                
                #PKMN TCG Code Scraping
                if decodedString[18] == '-' and decodedString[23] == '-' \
                    and decodedString[27] == '-':
                    
                    print(decodedString[15:31])
                    codes.add(str(decodedString[15:31]))
            
    for code in codes:
            print(code)

    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__" :
    main()