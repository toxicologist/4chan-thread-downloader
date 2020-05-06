import requests, urllib.request, os, threading
from progressbar import Bar, ProgressBar, Percentage

def getImagesFromThread(thread):
    images = []
    filenames = []
    d = requests.get(thread).text

    plebs = "4plebs" in thread

    image_filter = '" target="_blank" rel="noreferrer" class="thread_image_link">' if plebs else '<a class="fileThumb" href="//'
    link = '' if plebs else 'https://'

    if "4plebs" in thread:
        images = ['%s%s'%(link, post.split('"')[-1]) for post in d.split(image_filter)[:-1]]
        f_prev = ''
        for file in d.split('download="')[1:]:
            f = file.split('"')[0]
            if f != f_prev:
                filenames.append(f)
                f_prev = f
        
    else:
        images = ['%s%s'%(link, post.split('"')[0]) for post in d.split(image_filter)[1:]]
        for file in d.split('File: ')[1:]:
            if '(...)' in file:
                filenames.append(file.split('<a title="')[1].split('"')[0])
            else:
                filenames.append(file.split('</a>')[0].split('>')[-1])
    return images, filenames

def getImage(image, filename, saveDir):
    global saved
    if not os.path.exists(saveDir):
        os.mkdir(saveDir)
    path = "%s\\%s" % (saveDir, filename)
    if not os.path.exists(path):
        urllib.request.urlretrieve(image, path)
    saved.append(1)
    

def saveImages(images, filenames, saveDir):
    pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(images)).start()
    for i in range(len(images)):
        image = images[i]
        filename = filenames[i]
        #print("Downloading %s/%s: %s" %(images.index(image),len(images), image))
        threading.Thread(target=lambda: getImage(image, filename, saveDir)).start()
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
images, filenames = getImagesFromThread(url)
#print(images)
print(filenames)
print('Downloading %s images' % len(images))
try:
    saveImages(images, filenames, saveDir)
except KeyboardInterrupt:
    print("Exiting")
print('Done!')
