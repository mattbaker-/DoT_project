main06.py
Yesterday
Wed 8:05 PM
M
You uploaded an item
Text
main06.py
import picamera
from time import sleep
from datetime import date, datetime, time, timedelta
import os
import glob

camera = picamera.PiCamera()
camera.rotation = 180
camera.resolution = (1280, 720)

startUpTime = datetime.now() # timestamp at which the code is run (or 'bootupTimestamp')

start = datetime(startUpTime.year, startUpTime.month, startUpTime.day, hour = 7) # 07:00:00
end = datetime(startUpTime.year, startUpTime.month, startUpTime.day, hour = 18, minute = 37) # 19:00:00
print('start: ' + str(start))
print('end: ' + str(end))

spliceDuration = 60 # in seconds (or 'segmentDuration')
endRecordingTime = startUpTime + timedelta(seconds = spliceDuration)#minutes = 5)#seconds = spliceDuration)#
print('Begin Recording at:\t\t' + str(startUpTime))
print('End Recording at:\t\t' + str(endRecordingTime) + '\n')

def main():
    os.chdir('/home/pi/Desktop/Recordings')
    #os.chdir('/media/pi/8132-4C61')
    
    dateString = datetime.strftime(date.today(), "%m-%d")
    print('Date String: ' + dateString)
    try:
        os.mkdir(dateString)
    except Exception as e:
        print(e)
    os.chdir(os.getcwd() + '/' + dateString)
    print('cwd: ' + os.getcwd() + '\n')
    
    timeString = datetime.strftime(datetime.now(), "%H:%M")
    print('Time String: ' + timeString)
    try:
        os.mkdir(timeString)
    except Exception as e:
        print(e)
    os.chdir(os.getcwd() + '/' + timeString)
    print('cwd: ' + os.getcwd() + '\n')
    
    while datetime.now() < end:#endRecordingTime:
        filename = datetime.now().strftime('%H:%M:%S' + '.h264')
        #print('filename: ' + filename + '\n')
        try:
            print('\tRecording \'' + filename + '\' to ' + os.getcwd())
            camera.start_recording(filename)
            camera.wait_recording(spliceDuration)
            camera.stop_recording()
            print('\tDone recording \'' + filename + '\'')
        except Exception as e:
            print(e)
    
try:
    main()
finally:
    camera.close()
