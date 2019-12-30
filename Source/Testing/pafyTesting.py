import pafy

url = 'https://youtube.com/watch?v=OI4cSgsWVfo'

pafyResult = pafy.new(url)

myVideo = pafyResult.getbestvideo('m4v',True)

print(myVideo)

myVideo.download()