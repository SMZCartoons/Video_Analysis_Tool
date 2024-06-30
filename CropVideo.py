from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import datetime
import os 
                             
def cropFile(fileName):
    '''Exports cropped version of original video from given start to given end time in seconds'''
    fileName1 = fileName.split(".")[0]
    filePath = "C:\\Users\\SUNDAS9\\OneDrive - Rensselaer Polytechnic Institute\\Documents\\Classes\\Research\\Videos\\"+fileName1+"\\"
   
    os.mkdir(filePath)
     
    fp = open("points.txt")
    
    index = 1
    for w in fp:
        times = w.split('-')
        startTime = times[0]
        endTime = times[1]
        
        startTime = startTime.split(":")
        endTime = endTime.split(":")
        
        startSecond = 0
        if(len(startTime)==3):
            startSecond = (3600*int(startTime[0]))+(60*int(startTime[1]))+(int(startTime[2]))
        elif(len(startTime)==2):
            startSecond = (60*int(startTime[0]))+int(startTime[1])
            
        endSecond = 0
        if(len(startTime)==3):
            endSecond = (3600*int(endTime[0]))+(60*int(endTime[1]))+int(endTime[2])
        elif(len(startTime)==2):
            endSecond = (60*int(endTime[0]))+int(endTime[1])
            
        print(type(startSecond), type(endSecond))
        # have it in hr:min:sec format in points.txt
        
        # put a counter (filename1 filename2, etc.)
        outputFileName = fileName1+"_"+str(index)+".mp4"
        
        ffmpeg_extract_subclip(fileName, startSecond, endSecond, targetname=outputFileName)
        old_path = outputFileName
        new_path = filePath+"\\"+outputFileName
        os.rename(old_path, new_path)
        
        index+=1
        
    fp.close()
    old_path = "points.txt"
    new_path = filePath+"\\points.txt"
    os.rename(old_path, new_path)
    
    old_path = fileName
    new_path = filePath+"\\"+fileName
    os.rename(old_path, new_path)
    
    fp = open("points.txt", "w")
    fp.close()    
    
cropFile("S13_Day1_2.mp4")