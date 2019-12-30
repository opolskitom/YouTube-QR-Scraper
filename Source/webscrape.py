# Created by: Thomas Opolski
# Date Created: 12/27/19
# Date Modified: 12/27/19

# Program Description: The idea is a basic youtube link parser that gets all
# videos within a certain search criteria or link, puts them in a list, and downlaods 
# them to be processed and analyzed. Output websites and codes in the appropriate section.

import requests
from bs4 import BeautifulSoup
import webbrowser
import pafy
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from PyQt5 import QtGui, QtWidgets, uic

class QRCodeScraper:

    #bools for checkboxes
    displayVideosEnabled = True
    websiteQREnabled = True
    tcgCodeQREnabled = False
    searchLinkEnabled = False

    def __init__(self):
        #initializing window
        super(QRCodeScraper,self).__init__()
        self.app = QtWidgets.QApplication([])
        self.call = uic.loadUi('myWindow.ui')
        self.call.setWindowTitle("YouTube QR Scraper")
        self.call.setWindowIcon(QtGui.QIcon("qrcodeicon.png"))

        #setting functionalities for widgets

        #buttons (3)
        self.call.addVideoButton.clicked.connect(self.addVideo)
        self.call.clearVideosButton.clicked.connect(self.clearVideo)
        self.call.scanVideosButton.clicked.connect(self.scanVideo)

        #check boxes (4)
        self.call.getWebsitesCheckBox.stateChanged.connect(self.stateChangeWebsite)
        self.call.getTcgCodesCheckBox.stateChanged.connect(self.stateChangeTCGCode)
        self.call.displayVideosCheckBox.stateChanged.connect(self.stateChangeVideoDisplay)
        self.call.searchLinkCheckBox.stateChanged.connect(self.stateChangeSearchLink)

        #display and close window
        self.call.show()
        self.app.exec()

    def addVideo(self):
        userUrl = self.call.userLinkEdit.text()
        if (self.searchLinkEnabled):
            urlListFromSearch = self.getURLSFromSearch(userUrl)
            for url in urlListFromSearch:
                self.call.videoQueueList.addItem(url)
        else:
            self.call.videoQueueList.addItem(userUrl)

    def clearVideo(self):
        self.call.videoQueueList.clear()

    def scanVideo(self):
        outputList = []

        urlLinkList =  [str(self.call.videoQueueList.item(i).text()) \
            for i in range(self.call.videoQueueList.count())]
        
        for urlLink in urlLinkList:
            outputList += list(self.getFromURL(urlLink))

        for output in outputList:
            self.call.outputDataList.addItem(output)

    def stateChangeWebsite(self):
        if self.websiteQREnabled:
            self.websiteQREnabled = False
        else:
            self.websiteQREnabled = True

    def stateChangeTCGCode(self):
        if self.tcgCodeQREnabled:
            self.tcgCodeQREnabled = False
        else:
            self.tcgCodeQREnabled = True

    def stateChangeVideoDisplay(self):
        if self.displayVideosEnabled:
            self.displayVideosEnabled = False
        else:
            self.displayVideosEnabled = True

    def stateChangeSearchLink(self):
        if self.searchLinkEnabled:
            self.searchLinkEnabled = False
        else:
            self.searchLinkEnabled = True
 
    def getQrDataSet(self, play):
        qrDataSet = set()

        cap = cv2.VideoCapture(play.url)
        while(True):
            ret,frame = cap.read()
            if frame is None:
                    break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            #display video if enabled
            if (self.displayVideosEnabled):
                cv2.imshow('videoFramesAnalyzed',frame)

            #check qr code
            decodeObj = pyzbar.decode(frame)

            if len(decodeObj) > 0:
                decodedData = decodeObj[0]
                decodedString = str(decodedData)

                if len(decodedString) > 20:

                    #Website URL Scraping
                    if (self.websiteQREnabled):
                        myWebLink = ''
                        
                        if decodedString[15:19] == 'http':
                            i = 15
                            #read until apostrophe
                            while (decodedString[i] != "'") :
                                myWebLink += decodedString[i]
                                i += 1
                            
                            qrDataSet.add(myWebLink)

                    #PKMN TCG Code Scraping
                    if (self.tcgCodeQREnabled):
                        if decodedString[18] == '-' and decodedString[23] == '-' \
                            and decodedString[27] == '-':
                                
                            print(decodedString[15:31])
                            qrDataSet.add(decodedString[15:31])
            
        cap.release()
        cv2.destroyAllWindows()

        return qrDataSet

    def getFromURL(self, myURL):

        try:
            video = pafy.new(myURL)

            play = video.getbest(preftype="webm")
            if (play == None):
                play = video.getbest(preftype="mp4")

            qrDataSet = self.getQrDataSet(play)

            return qrDataSet

        except:
            print("Invalid URL")
            return []

    def getURLSFromSearch(self, myURL):
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

        return(urls)


def main():

    #saved search URL: https://www.youtube.com/results?search_query=oogaboogaroogatooga12345&sp=QgIIAQ%253D%253D

    myScraper = QRCodeScraper()


if __name__ == "__main__" :
    main()