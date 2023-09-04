import os
import shutil

os.makedirs("./images_NP", exist_ok=True)
os.makedirs("./segm_NP", exist_ok=True)


imageFiles = os.listdir("./images")

for file in files:
    if file.endswith("full.jpg"):
        sourcePath = os.path.join("./images", file)
        destinationPath = os.path.join("./images_NP", file[-22:])
        shutil.copy(sourcePath, destinationPath)
