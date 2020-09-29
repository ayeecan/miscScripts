from maya import cmds, mel

def getValues():
    """Get highlighted values from Time Slider"""
    slider = mel.eval("$tmpVar=$gPlayBackSlider")
    timeRange = cmds.timeControl(slider, q = True, rangeArray = True)
    firstFrame = timeRange[0]
    lastFrame = timeRange[1] - 1
    
    return firstFrame, lastFrame

def findMid():
    """Find the middle between selected frame range"""
    firstFrame,lastFrame = getValues()
    middle = (firstFrame + lastFrame) / 2
    print "Middle frame is {0}".format(middle),

findMid()
