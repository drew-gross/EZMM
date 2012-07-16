from operator import itemgetter

import cv2

def display(image):
    cv2.imshow('',image)
    while cv2.waitKey(-1) not in [-1, 113]: # close or press q
        pass

def hLine(image, row, color=(0,0,255,0)):
    cv2.line(image, (0,row), (image.shape[1], row), color)

def vLine(image, col, color=(0,0,255,0)):
    cv2.line(image, (col, 0), (col, image.shape[0]), color)

def rowFromSection(image, section):
    return image[section['startpos']:section['count'] + section['startpos']]

def colFromSection(image, section):
    return image[:,section['startpos']:section['count'] + section['startpos']]

def isEmpty(row):
    return cv2.minMaxLoc(row)[0] > 25

def rowsWithProperty(image, property):
    return [property(image[i]) for i in xrange(image.shape[0])]

def colsWithProperty(image, property):
    return [property(image[:,i]) for i in xrange(image.shape[1])]

def findTrueSections(array):
    sections = []
    currentVal = None
    for index, val in enumerate(array):
        if val != currentVal:
            sections.append({'val':val, 'count':1, 'startpos':index})
            currentVal = val
        else:
            sections[-1]['count'] += 1;
    sectionsWithProperty = filter(itemgetter('val'), sections)
    return sectionsWithProperty

def largeRowsWithProperty(image, sectionProperty):
    trueSections = rowsWithProperty(image, sectionProperty)
    minSecCount = max(trueSections, key=itemgetter('count'))['count']/10
    return findTrueSections(rowHasProperty)

def splitToRows(image):
    grayImage = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
    sections = findTrueSections(rowsWithProperty(grayImage, lambda x: not isEmpty(x)))
    return map(lambda section: rowFromSection(image, section), sections)

def splitToCols(image):
    grayImage = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
    sections = findTrueSections(colsWithProperty(grayImage, lambda x: not isEmpty(x)))
    return map(lambda section: colFromSection(image, section), sections)

image = cv2.imread("""C:\Users\Drew Gross\Documents\Projects\EZMM\Test data\CHE101MS08N.jpg\page.jpg""")

letters = []
rows = splitToRows(image)
for row in rows:
    cols = splitToCols(row)
    for col in cols:
        letters.append(col)

[cv2.imwrite(str(index) + '.jpg', row) for index, row in enumerate(letters)]