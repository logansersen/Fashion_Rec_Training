import os
import shutil

os.makedirs("./clothing", exist_ok=True)

labels = [
    ['top', '01'],
    ['outer', '02'],
    ['skirt', '03'],
    ['dress', '04'],
    ['pants', '05'],
    ['leggings', '06'],
    ['footwear', '11'],
]

filenames = os.listdir("./images_NP")

for label in labels:
    os.makedirs("./clothing/" + label[0], exist_ok=True)

for filename in filenames:
    dir = "./images_SR/" + filename[:-4] + "/BB/"
    clothingItems = os.listdir(dir)
    
    for clothingItem in clothingItems:
        pItem = clothingItem[19:-4]

        for i, row in enumerate(labels):
            if row[1] == str(pItem):
                index = i
                break
            
        folder = labels[index][0]
        sourcePath = dir + clothingItem
        destinationPath = "./clothing/" + folder + "/" + clothingItem
        shutil.copy(sourcePath, destinationPath)
        
        
        
