import picamera
from datetime import date, datetime, time, timedelta
import os
import shutil

########################
######## SETUP #########
########################
print('########################')
print('######## SETUP #########')
print('########################')

camera = picamera.PiCamera()
#camera.rotation = 180
camera.resolution = (1280, 720)

spliceDuration = 30 # SS

##############################
#### DATETIME DECLARTIONS ####
##############################

datetimeNow = datetime.now() # YYYY-MM-DD HH:MM:SS.ms
datetimeToday = datetime.today() # YYYY-MM-DD HH:MM:SS.ms
dateToday = date.today() # YYYY-MM-DD

beginTime = time(6) # 06:00:00
beginDate = date.today() # YYYY-MM-DD
beginDatetime = datetime.combine(beginDate, beginTime) # YYYY-MM-DD 06:00:00

#endTime = time(19) # 19:00:00
endTime = time(17, 1, 00) # HH:MM:SS
endDate = date.today() # YYYY-MM-DD
endDatetime = datetime.combine(endDate, endTime) # YYYY-MM-DD 19:00:00

print('\n##### DATETIME PARAMETER DECLARATIONS #####')
print('datetimeNow:\t\t' + str(datetimeNow) + ' \t' + str(type(datetimeNow)))
print('datetimeToday: \t\t' + str(datetimeToday) + ' \t' + str(type(datetimeToday)))
print('dateToday:\t\t' + str(dateToday) + ' \t\t\t' + str(type(dateToday)))
print('\nbeginTime: \t\t' + str(beginTime) + ' \t\t\t' + str(type(beginTime)))
print('endTime: \t\t' + str(endTime) + ' \t\t\t' + str(type(beginTime)))
print('beginDate: \t\t' + str(beginDate) + ' \t\t\t' + str(type(beginDate)))
print('endDate: \t\t' + str(endDate) + ' \t\t\t' + str(type(endDate)))

localDir = '/home/pi/Desktop/Recordings'
localDirPath = localDir + '/' + str(dateToday)
# Declare a text filename to write exceptions to
exceptionFile = localDir + '/' + str(dateToday) + '_exceptions.txt'
def writeToExceptionFile(exptn):
    f = open(exceptionFile, 'a')
    f.write(str(datetime.now()) + ':\t' + str(exptn) + '\n')
    f.close()

print('\n##### LOCAL SOURCE DIRECTORY DECLARATION #####')
print('localDir: \t\t' + localDir)
print('localDirPath: \t\t' + localDirPath)

#######################################
#### CREATE LOCAL SOURCE DIRECTORY ####
#######################################
print('\n#### CREATE LOCAL SOURCE DIRECTORY ####')
try:
    print('\tcreating new folder in localDir:\t/' + str(dateToday))
    
    os.mkdir(localDirPath)
except Exception as e:
    print('\t\t' + str(e))
    writeToExceptionFile(e)

##########################################
#### RECORD TO LOCAL SOURCE DIRECTORY #### (START RECORDING TO LOCAL FOLDER)
##########################################
print('\n########################')
print('######## RECORD ########')
print('########################')
# Record Video Clips to Path of the Local Directory
try:
    print('recording clips in <' + str(spliceDuration) + '> second intervals until <' + str(endTime) + '>')
    if datetime.now() < endDatetime: # is this line of code necessary??
        while datetime.now() < endDatetime:
            filename = datetime.now().strftime('%H-%M_[%S]' + '.h264')
            try:
                print('\tRecording \'' + filename + '\' to ' + localDirPath)
                camera.start_recording(localDirPath + '/' + filename)
##                dt = end - datetime.now()
##                print('dt: ' + str(dt))
##                if dt < spliceDuration:
##                    camera.wait_recording(dt)
##                else:
                camera.wait_recording(spliceDuration)
                camera.stop_recording()
                print('\tDone recording \'' + filename + '\'')
            except Exception as e:
                print(e)
                writeToExceptionFile(e)
    else:
        print('\tRecord failed.')
        print('\tCurrent time not within record time range (...too to late record)')
finally:
    camera.close()

# Determine Size of Local Directory
print('\n##### LOCAL DIRECTORY SIZE #####')
print('localDirPath: ' + localDirPath)
localDirContents = os.listdir(localDirPath)
localDirTotalSize = 0
for file in localDirContents:
    file_size = os.path.getsize(localDirPath + '/' + file)
    localDirTotalSize += file_size
    print('\t\t' + file + '\t' + str(file_size) + ' bytes')
print('\n\tlocalDirTotalSize: \t' + str(localDirTotalSize) + ' bytes')

print('\n###########################')
print('##### MOUNTED VOLUMES #####')
print('###########################')

mountedVolumesDir = '/media/pi'
mountedVolumes = os.listdir(mountedVolumesDir)

# List Mounted Volumes
print('\n##### LIST VOLUMES #####')
for volume in mountedVolumes:
    diskTotal = shutil.disk_usage(mountedVolumesDir + '/' + volume).total
    diskUsed = shutil.disk_usage(mountedVolumesDir + '/' + volume).used
    diskFree = shutil.disk_usage(mountedVolumesDir + '/' + volume).free
    print('\t' + volume + ':')
    print('\t\t total: ' + str(diskTotal) + ' \tbytes')
    print('\t\t used: \t' + str(diskUsed) + ' \tbytes')
    print('\t\t free: \t' + str(diskFree) + ' \tbytes')
    
# Define function for iterating through mounted volumes and returning true/false if space is available
def checkVolume(mntIndex):
    vol = mountedVolumes[mntIndex]
    diskFree = shutil.disk_usage(mountedVolumesDir + '/' + vol).free
    print(vol + ' free: ' + str(diskFree))
    if diskFree > localDirTotalSize:
        return True
    else:
        mountIndex += 1
        return False

# Check Mounted Volumes for Free Space
print('\n##### DETERMINE TARGET VOLUME #####')
try:
    mountIndex = 0
    while checkVolume(mountIndex) == False:
        checkVolume(mountIndex)
    targetVolDir = mountedVolumesDir + '/' + mountedVolumes[mountIndex]
    print('targetVolDir: \t' + targetVolDir)
except Exception as e:
    print('\t' + str(e))
    writeToExceptionFile(e)

### Create Directory Path of Target Volume
print('\n##### CREATE TARGET DIRECTORY ON MOUNT VOLUME #####')
print('\tcreating new folder in targetVol:\t/' + str(dateToday))
try:
    targetVolPath = targetVolDir + '/' + str(dateToday)
    os.mkdir(targetVolPath)
except Exception as e:
    print('\t\t' + str(e))
    writeToExceptionFile(e)

#############################################################################
### MOVE CONTENT FROM LOCAL SOURCE DIR TO EXTERNAL VOLUME DESTINATION DIR ###
#############################################################################
print('\n###########################')
print('##### COPY CONTENT #####')
print('###########################')
try:
    # Copy files from Source Directory to Destination Directory
    print('copying files from ' + localDirPath + '\tto ' + targetVolPath)# + '\n')
    for file in localDirContents:
        print('\tcopying file\t' + file)
        try:
            #shutil.copy(localDirPath + '/' + file, targetVolPath)
            shutil.move(localDirPath + '/' + file, targetVolPath)
        except Exception as e:
            print('\t' + str(e))
            writeToExceptionFile(e)
    print('Copy complete!')
except Exception as e:
    print('\t' + str(e))
    writeToExceptionFile(e)

f = open(exceptionFile, 'a')
f.write('\n')
f.close()
