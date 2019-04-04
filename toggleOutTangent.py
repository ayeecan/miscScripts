from maya import cmds, mel

def queryTan():
    '''Query out tangent'''
    qTan = cmds.keyTangent(q = True, g = True, ott = True)
    tanStr = singleListToString(qTan)
    
    return tanStr
    
def changeTan(tanType):
    '''Change out tangent'''
    cTan = cmds.keyTangent(g = True, ott = tanType)
    tanStr = singleListToString(cTan)
    
    return tanStr

def singleListToString(list):
    '''Return first item in list as a string'''
    if list is None:
        new_string = []
    else:
        new_string = list[0]
    
    return new_string

def runScript():
    '''Runs the script'''
    curTan = queryTan()
    stepTan = 'step'
    autoTan = 'auto'
    
    if curTan == stepTan:
        changeTan(autoTan)
    else:
        changeTan(stepTan)
        
    newCurTan = queryTan()
    mel.eval('print "Global out tangent has been changed to {0}";'.format(newCurTan))
    
runScript()
