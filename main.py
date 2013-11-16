import cv2
import time
import sys
import os


command = 'capture'
camNum = 0
outputPath = 'out/'
imagePrefix = 'timelapse_'
clicked = False
fps = 20
size = (640, 480)


def printParams():
    print "Params: " + str(sys.argv)


def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))


def buildVideo():
    global outputPath, fps, size

    if len(sys.argv) > 2:
        outputPath = sys.argv[2]
    
    if len(sys.argv) > 3:
        fps = int(sys.argv[3])
    
    videoWriter = cv2.VideoWriter('MyOutputVid.avi', cv2.cv.CV_FOURCC('M','J','P','G'), fps, size)

    for file in sorted_ls(outputPath):
        if file.endswith(".jpg"):
            image = cv2.imread(outputPath + file)
            videoWriter.write(image)


def capturing():
    global camNum, outputPath, imagePrefix

    if len(sys.argv) > 2:
        camNum = int(sys.argv[2])

    if len(sys.argv) > 3:
        outputPath = sys.argv[3]
    
    if len(sys.argv) > 4:
        imagePrefix = sys.argv[4]
    
    cameraCapture = cv2.VideoCapture(camNum)

    success, frame = cameraCapture.read()
    while not success:
        success, frame = cameraCapture.read()

    cv2.imwrite(outputPath + imagePrefix + str(time.time()) + '.jpg', frame)


def onMouse(event, x, y, flags, param):
    global clicked

    if event == cv2.cv.CV_EVENT_LBUTTONUP:
        clicked = True


def testing():
    global clicked, camNum
    
    if len(sys.argv) > 2:
        camNum = int(sys.argv[2])
    
    cameraCapture = cv2.VideoCapture(camNum)
    cv2.namedWindow('MyWindow')
    cv2.setMouseCallback('MyWindow', onMouse)
    
    success, frame = cameraCapture.read()
    while success and cv2.waitKey(1) == -1 and not clicked:
        cv2.imshow('MyWindow', frame)
        success, frame = cameraCapture.read()
    
    cv2.destroyWindow('MyWindow')


def execCommand(command):
    if command == 'test':
        testing()
    elif command == 'capture':
        capturing()
    elif command == 'build':
        buildVideo()
    else:
        print "wrong command!"


if len(sys.argv) > 1:
    
    command = sys.argv[1]
    
    execCommand(command)
    
    printParams()

    print "done!"

else:
    print 'no command given'