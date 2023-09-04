import os
import shutil

os.makedirs("./segm_NP", exist_ok=True)

segmFiles = os.listdir("./segm")

for file in segmFiles:
    index0 = file.find("0")
    indexSeg = file.find("segm")

    if (file.find("full") == -1):
        continue
    
    sourcePath = os.path.join("./segm", file)
    destinationPath = os.path.join("./segm_NP", file[index0:(indexSeg - 1)] + ".png")
    shutil.copy(sourcePath, destinationPath)
