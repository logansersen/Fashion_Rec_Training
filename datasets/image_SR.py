from PIL import Image
from PIL import ImageDraw
import os
import shutil
import numpy as np

os.makedirs("./images_SR", exist_ok=True)
segmFiles = os.listdir("./segm_NP")


def segmentationRemover(iSeg, pSeg, pTarget, targetColor):
    matchingPixels = [(x, y) for x in range(iSeg.width) for y in range(iSeg.height) if pSeg[y * iSeg.width + x] == targetColor]
    for x,y in matchingPixels:
        pTarget[x,y] = (255,255,255)

    return pTarget

def exportSegment(iSeg, pSeg, pTarget, currentSegment, keySegments, imageTarget):
    image = imageTarget.copy()
    pixels = image.load()

    if currentSegment == 2:
        for segment in keySegments:
            if segment != currentSegment and segment != 1 and segment != 4:
                pixels = segmentationRemover(iSeg, pSeg, pixels, segment)
    else:
        for segment in keySegments:
            if segment != currentSegment:
                pixels = segmentationRemover(iSeg, pSeg, pixels, segment)

    ''' exports with full model before bounding boxes
    image.save("./images_SR/" + filename[:-4] + "/" + filename[:-4] + "_" + str(currentSegment) + ".jpg")
    '''
    
    #bounding boxes
    matchingPixels = [(x, y) for x in range(iSeg.width) for y in range(iSeg.height) if pSeg[y * iSeg.width + x] == currentSegment]
    if len(matchingPixels) > 5:
        npMatchingPixels = np.array(matchingPixels)
        max_x = np.max(npMatchingPixels[:, 0])
        min_x = np.min(npMatchingPixels[:, 0])
        max_y = np.max(npMatchingPixels[:, 1])
        min_y = np.min(npMatchingPixels[:, 1])

        image = image.crop((min_x, min_y, max_x, max_y))
        os.makedirs("./images_SR/" + filename[:-4] + "/BB/", exist_ok=True)

        if(currentSegment < 10):
            currentSegment = "0" + str(currentSegment)
        else:
            currentSegment = str(currentSegment)
      
        image.save("./images_SR/" + filename[:-4] + "/BB/" + filename[:-4] + "_" + currentSegment + ".jpg")    
    

for filename in segmFiles:
    imageSegm = Image.open("./segm_NP/" + filename)
    imageTarget = Image.open("./images_NP/" + filename[:-3] + "jpg")

    pixelsSegm = list(imageSegm.getdata())
    pixelsTarget = imageTarget.load()

    #body segments
    colorArray = [13, 14, 15]

    for color in colorArray:
        pixelsTarget = segmentationRemover(imageSegm, pixelsSegm, pixelsTarget, color)

    #accessory segments
    colorArray = [7, 8, 9, 10, 12, 16, 17, 18, 19, 20, 21, 22, 23]

    for color in colorArray:
        pixelsTarget = segmentationRemover(imageSegm, pixelsSegm, pixelsTarget, color)
    
    keySegments = [1, 2, 3, 4, 5, 6, 11]

    os.makedirs("./images_SR/" + filename[:-4], exist_ok=True)
    
    for segment in keySegments:
        exportSegment(imageSegm, pixelsSegm, pixelsTarget, segment, keySegments, imageTarget)

    ''' exports with models and accessories removed  
    imageTarget.save("./images_SR/" + filename[:-3] + "jpg")
    '''

"""
0 background
1 shirt
2 outer
3 skirt
4 dress
5 pants
6 leggings
7 headwear
8 eyeglass
9 neckwear
10 belt
11 brown (shoes)
12 orange (bag)
13 red (hair)
14 blue (face)
15 green (body)
16 light blue (ring)
17 middle blue (bracelet)
18 socks
19 gloves
20 necklace
21 rompers
22 earings
23 tie

include: (1, 2, 3, 4 5, 6, 11)

"""



'''  color testing

filename = "./segm_NP2/" + segmFiles[0]

image = Image.open(filename)
pixels = list(image.getdata())
unique_colors = list(set(pixels))
for color in unique_colors:
    print(color)

'''
