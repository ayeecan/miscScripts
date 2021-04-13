from maya import cmds

gpSeq     = 'greasePencilSequence1'
frameTime = gpSeq + '.frame[{0}].frameTime'
frames    = cmds.getAttr(frameTime.format('*'))

for i in range(len(frames)):
    offset = 1000
    timeString = frameTime.format(i)
    
    oldTime = cmds.getAttr(timeString)
    cmds.setAttr(timeString, (oldTime + offset))
