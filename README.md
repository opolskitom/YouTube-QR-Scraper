# YouTube Video QR Code Scraper
 Small program to scrape YouTube videos for QR codes written in Python in under a week. Primarily used for learning Python GUI elements and imports as well as general syntaxing and experience.
 
 # Demonstration
https://www.youtube.com/watch?v=PX6tg_plEXE

[![Demo](https://i.ytimg.com/vi/PX6tg_plEXE/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLBa5HxZtYze8-1Sp-9Y2bGoysn3RA)](https://youtu.be/PX6tg_plEXE)

# Imports
This program uses multiple different imports which can be installed using pip

1. BeatifulSoup and requests
     ```
     pip install requests
     pip install bs4
     ```
   - used for parsing youtube webpage information
   
2. pafy
     ```
     pip install pafy
     ```
     - used for getting and downloading/streaming youtube videos

3. cv2
     ```
     pip install opencv-python
     ```
     - used for video processing along with the video from pafy

4. pyzbar
     ```
     pip install pyzbar
     ```
     - used for barcode/qr scanning images through the frames in cv2
     
5. pyQt5
     ```
     pip install PyQt5
     ```
     - used for UI elements
     
    
# Usage
Wrote this without any intention of big usage as a newer programmer, feel free to use the code in other projects.
