import cv2
import numpy as np
from matplotlib import pyplot as plt
import csv
import math
from threading import Thread
import os
import pandas as pd
import time
from multiprocessing import Process, Value, Array, Manager


def splitData(fileName):
    arr = np.loadtxt("gaze.csv", delimiter=",", dtype=str)
    header = arr[0,:]
    arr = arr[1:, :]
    arr1 = arr[:, 2].astype(float)
    arr1 = (arr1-arr1[0])*1e-9

    result = list()
    fp = open("C:\\Users\\SUNDAS9\\OneDrive - Rensselaer Polytechnic Institute\\Documents\\Classes\\Research\\Videos\\"+fileName+"\\points.txt")
    i = 0
    for line in fp:
        line = line.strip().split("-")
        minSec1 = line[0].split(":")
        timeSecStart = (int(minSec1[0])*60)+int(minSec1[1])
        
        minSec2 = line[1].split(":")
        timeSecEnd = (int(minSec2[0])*60)+int(minSec2[1])
        
        currMap = np.zeros(arr1.shape).astype(bool)
        currMap[arr1>=timeSecStart] = True
        
        currMap1 = np.zeros(arr1.shape).astype(bool)
        currMap1[arr1<=timeSecEnd] = True
        
        curr = currMap & currMap1
        
        selectedRows = arr[curr] 
        gazeDataTime = selectedRows[:, 2].astype(float)
        gazeDataTime = ((gazeDataTime-gazeDataTime[0])*1e-9)* 24      
        print(gazeDataTime)
        
        i+=1
        
        filename = "{}{}.csv".format("foo", str(i))
        
        np.savetxt(filename, gazeDataTime, delimiter=',', fmt="%s")
        
        result.append(selectedRows)
        
    return result
    


# def circleFilter(image, frames, index, video_dim, gazeData):
    
#     center_x = int(gazeData[3].astype(float))
#     center_y = int(gazeData[4].astype(float))
#     r, c, _ = image.shape
#     # radius = min(r,c)//2
#     # mask = np.zeros(image.shape, dtype="uint8")
#     # cv2.circle(mask, (center_x//2, center_y//2), radius, (255, 255, 255), thickness=-1)
#     # print((center_x//2, center_y//2), image.shape, r//2)
#     # frame = cv2.bitwise_and(image, mask)
    
    
#     frames[index] = frame
    
def vignette(image, frames, index, video_dim, gazeData):
    r, c = video_dim
    kernel_x = cv2.getGaussianKernel(2*c,200)
    kernel_y = cv2.getGaussianKernel(2*r,200)
    
    kernel = kernel_y * kernel_x.T
    mask = 255 * (kernel / np.linalg.norm(kernel))
    mask = cv2.resize(mask, video_dim)
    
    output = np.copy(image)
    for i in range(3):
        output[:,:,i] = output[:,:,i] * mask
    frames[index] = output
    
    # cv2.imshow('now', output)
    # cv2.waitKey(0)
    
    
def ptOfInterest(gazeData, foldername, filename, index):
    path1 = f"C:\\Users\\SUNDAS9\\OneDrive - Rensselaer Polytechnic Institute\\Documents\\Classes\\Research\\OutputVideos\\{foldername}\\"
    
    startx = time.time()
    processes = list()
        
    frames = list()
    path = "C:\\Users\\SUNDAS9\\OneDrive - Rensselaer Polytechnic Institute\\Documents\\Classes\\Research\\Videos\\"+foldername+"\\"+filename
    cap= cv2.VideoCapture(path)
    success, frame = cap.read()
    outputfileName = filename.split(".")[0]+".avi"
    fps = 24.00
    video_dim = (480,480)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    vidwriter = cv2.VideoWriter(f"{path1}\\output_{index}.avi", cv2.VideoWriter_fourcc(*"MJPG"), 24.0, video_dim, isColor=True)
    
    gazeDataTime = gazeData[:, 2].astype(float)
    gazeDataTime = ((gazeDataTime-gazeDataTime[0])*1e-9)*24
    

    i = 0
    frameNo = 1
    while 1:
        
        currRows = gazeData[(gazeDataTime<=frameNo) & (gazeDataTime>=(frameNo-1))]
        if(currRows.shape[0]==0): break
        print(gazeDataTime[(gazeDataTime<=frameNo) & (gazeDataTime>=(frameNo-1))])
        print(frameNo)
        frame = cv2.resize(frame, ((480, 480)), interpolation = cv2.INTER_AREA)
        print(frame.shape)
        for c in currRows:
            frames.append(None)
            vignette(frame, frames, i, video_dim, c)
            i+=1
        success, frame = cap.read()
        
        frameNo+=1
        
    print(frameNo, i, gazeData.shape)
    end_x = time.time()
    
    i = 0
    for f in frames: 
        print(i)
        vidwriter.write(f)
        i+=1
        
    
    cap.release()
    vidwriter.release()
        
    
'''
    PseudoCode
    processes = empty list
    results = empty list
    
    loop through every frame
        create a thread to proces frame
        add NONE to the results list
        start thread
        append to the active process list
        
    loop through active processes
        join current process
    
    print results
'''
if __name__=='__main__':
    startt = time.time()
    name = "S13_Day1_2" # video name
    os.mkdir("C:\\Users\\SUNDAS9\\OneDrive - Rensselaer Polytechnic Institute\\Documents\\Classes\\Research\\OutputVideos")
    path = f"C:\\Users\\SUNDAS9\\OneDrive - Rensselaer Polytechnic Institute\\Documents\\Classes\\Research\\OutputVideos\\{name}\\" #path to video
    os.mkdir(path)
    result = splitData(name)
    
    print(result[0].shape)
    for i in range(len(result)):
        ptOfInterest(result[i], name, f"{name}_{i+1}.mp4", i)
        endt = time.time()
        print(endt-startt)