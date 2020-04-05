import requests, urllib.request, os, threading
from progressbar import Bar, ProgressBar, Percentage

def getImagesFromThread(thread):
    images = []
    d = requests.get(thread).text
    if "4plebs" in thread:
        for i in d.split('<a href="https://i.4pcdn.org')[1:]:
            images.append('https://i.4pcdn.org%s' % i.split('"')[0])
        
        
    else:
        posts = d.split('<a class="fileThumb" href="//')[1:]
        for post in posts:
            images.append(str('https://%s')%post.split('"')[0])
            
    return images

def getImage(image, saveDir):
    global saved
    if not os.path.exists(saveDir):
        os.mkdir(saveDir)
    path = "%s\\%s" % (saveDir, image.split('/')[-1])
    if not os.path.exists(path):
        urllib.request.urlretrieve(image, path)
    saved.append(1)
    

def saveImages(images,saveDir):
    pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(images)).start()
    for image in images:
        #print("Downloading %s/%s: %s" %(images.index(image),len(images), image))
        threading.Thread(target=lambda: getImage(image, saveDir)).start()
    while True:
        pbar.update(len(saved))
        if len(images) == len(saved):
            print("All images saved")
            break
        
saved = []
url = str(input("Enter the url: \n"))
images = []
saveDir = str(input("Enter savedir: "))
print('Fetching image links...')
images = getImagesFromThread(url)
print('Downloading images')
try:
    saveImages(images, saveDir)
except KeyboardInterrupt:
    print("Exiting")
print('Done!')
