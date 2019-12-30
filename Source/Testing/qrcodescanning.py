import pafy
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

myURL = 'https://www.youtube.com/watch?v=NUSKZMAd-Hs'

video = pafy.new(myURL)

play = video.getbest(preftype="webm")
if (play == None):
    play = video.getbest(preftype="mp4")

qrDataSet = set()

cap = cv2.VideoCapture(play.url)
while(True):
    ret,frame = cap.read()
    if frame is None:
            break

    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.imshow('myvideo',frame)
    decodeObj = pyzbar.decode(frame)

    if len(decodeObj) > 0:
        decodedData = decodeObj[0]
        decodedString = str(decodedData)

        if len(decodedString) > 18:
            myWebLink = ''
            #Website URL Scraping
            if decodedString[15:19] == 'http':
                i = 15
                #read until apostrophe
                while (decodedString[i] != "'") :
                    myWebLink += decodedString[i]
                    i += 1
                
                qrDataSet.add(myWebLink)

            #PKMN TCG Code Scraping
            if decodedString[18] == '-' and decodedString[23] == '-' \
                and decodedString[27] == '-':
                    
                print(decodedString[15:31])
                qrDataSet.add(decodedString[15:31])
        
for qrData in qrDataSet:
        print(qrData)

cap.release()
cv2.destroyAllWindows()


