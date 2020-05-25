
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import os
from os.path import isfile, join
from PIL import Image
import os.path, sys
import glob


filein = '/Users/rubyjiang/Desktop/39/'
#Find all images in a directory training_1
#imgList=glob.glob('/Users/rubyjiang/Desktop/41/*.tif')  
imgList=glob.glob(filein+'*.tif')  
# make a dict to store the crop images:
expNum = filein[-3:-1]
directory_crop = expNum+"_crop"
parent_dir = "/Users/rubyjiang/Desktop"
crop_path = os.path.join(parent_dir, directory_crop) 
os.mkdir(crop_path) 
#make a dict to store the bg subtracted crop images
directory_bg = expNum+"_bg"
bg_path = os.path.join(parent_dir, directory_bg) 
os.mkdir(bg_path)
     
#Loop through all found images, and crop and save in crop file
for img in imgList:
    im = Image.open(img)
    #rotated = im.rotate(180)
    #imCrop = im.crop((0, 215, 888, 384)) 
    #imCrop = im.crop((0, 110, 888, 384)) #a 4-tuple defining the left(x), upper(y), right(x), and lower(y) pixel coordinate.
    imCrop = im.crop((0, 75, 888, 384))
    #imCrop = im.crop((0, 540, 1024, 920)) 
    #fileName = 'Exp'+str(41)+'_'+str(i+1): File name has to be changed every time
    fileName, fileExtension=os.path.splitext(img)
    fileName = fileName[28:] # you may need to change this value
    #imCrop.save(fileName+'_crop.tif')
    imCrop.save(crop_path + '/' + fileName +'_crop.tif')
#Get the crop image size, remember to change this     
# img_for_size = cv.imread('/Users/rubyjiang/Desktop/41_crop/41_IN718_plate_P48.00S0.2L1.5R-1.5_G12_S01001_crop.tif')
# height, width, channels = img_for_size.shape
# size = (width,height) 
# Convert images to video
def convert_frames_to_video(pathIn,pathOut,fps):   
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))] 
    #for sorting the file names properly # this step is important
    files.sort(key = lambda x: int(x[41:-9]))

    for i in range(len(files)):
        filename=pathIn + files[i]
        img = cv.imread(filename)
        height, width, layers = img.shape
        size = (width,height) 
        #inserting the frames into an image array
        frame_array.append(img)
    fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv.VideoWriter(pathOut,fourcc, fps, size)
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()


def main():
    pathIn='/Users/rubyjiang/Desktop/39_crop/'
    pathOut = pathIn +'video.mp4'
    fps = 15
    convert_frames_to_video(pathIn, pathOut, fps)

if __name__=="__main__":
    main()


pathIn='/Users/rubyjiang/Desktop/39_crop/'
#pathIn='/Users/rubyjiang/Desktop/'+ expNum +'_crop/'
pathOut = pathIn +'video.mp4'

#MOG2 background subtraction
# Create a VideoCapture object
cap = cv.VideoCapture(pathOut)
# Check if camera opened successfully
if (cap.isOpened() == False): 
    print("Unable to read camera feed")
fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v') # note the lower case
fgbg = cv.createBackgroundSubtractorMOG2(   history=150,
                                            varThreshold=8, #default 16, lower connect the broken keyhole#3 is good
                                            detectShadows=False # not important in our case 
                                        ) #https://arxiv.org/pdf/1810.02835.pdf
index = 1 
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        fgmask = fgbg.apply(frame)
        name = 'frame' + str(index) + '.jpg'
        cv.imwrite(bg_path+'/'+name, fgmask)
        index+=1

    # Break the loop
    else:
            break
# When everything done, release the video capture and video write objects
cap.release()
# Closes all the frames
cv.destroyAllWindows()



#Note: all places need to be specified every time running a new experiemnt
#13 filein
#35 specify the size for crop
#40 path for size
#61 main function:In, fps
#70 pathIn, copy the pathIn from main()
#92 name
