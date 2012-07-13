from operator import itemgetter

import cv2

def display(image):
    cv2.imshow('',image)
    while cv2.waitKey(-1) not in [-1, 113]: # close or press q
        pass

def hLine(image, row, color=(0,0,255,0)):
    cv2.line(image, (0,row), (image.shape[1], row), color)

def emptyRows2D(image):
    return [not cv2.minMaxLoc(image[i])[0] < 50 for i in xrange(0, image.shape[0])]

def largeBlankSections(image):
    emptyrows = emptyRows2D(image)
    sections = []
    currentRowVal = None
    for i in xrange(len(emptyrows)):
        if emptyrows[i] != currentRowVal:
            sections.append({'val':emptyrows[i], 'count':1, 'startpos':i})
            currentRowVal = emptyrows[i]
        else:
            sections[-1]['count'] += 1
    trueSections = filter(itemgetter('val'), sections)
    minSecCount = max(trueSections, key=itemgetter('count'))['count']/10
    blankSections = filter(lambda sec: sec['count'] > minSecCount, trueSections)
    return blankSections

image = cv2.imread("""C:\Users\Drew Gross\Documents\Projects\EZMM\Test data\CHE101MS08N.jpg\page.jpg""")
gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)

for obj in largeBlankSections(gray):
    for i in xrange(obj['startpos'], obj['startpos'] + obj['count']):
        hLine(image, i)

cv2.imwrite('test.jpg', image)
