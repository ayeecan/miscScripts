from maya import cmds

graphEditor = "graphEditor1FromOutliner"

def checkSelected():
    """Returns nothing if nothing's selected"""
    sel = cmds.ls(sl = True)
    if sel == []:
        sel = None
        
    return sel

def checkKeys(object):
    """Returns nothing if there's no keys"""
    keys = cmds.keyframe(object, q = True)
    
    return keys

def queryInfinity():
    """Query current infinity type"""
    preInfi = cmds.setInfinity(graphEditor, q = True, pri = True)[0]
    proInfi = cmds.setInfinity(graphEditor, q = True, poi = True)[0]
    
    return preInfi, proInfi
    
def switchSetting(curSetting):
    """Choose new infinity setting"""
    settingsDict = {
             "constant":"cycle",
                "cycle":"cycleRelative",
        "cycleRelative":"constant"
    }

    newSetting = settingsDict[curSetting]
    
    return newSetting
    
def makeInfinity():
    """Set the infinity type"""
    if checkSelected() is None:
        cmds.warning("Nothing Selected!")
        return
    if checkKeys(checkSelected()) is None:
        cmds.warning("Object has no keys!")
        return
        
    preInfi, proInfi = queryInfinity()
    newPre = switchSetting(preInfi)
    newPro = switchSetting(proInfi)
    
    cmds.setInfinity(graphEditor, pri = newPre)
    cmds.setInfinity(graphEditor, poi = newPro)
    
    print "Pre Infinity is now {0}. Post Infinity is now {1}.".format(newPre, newPro),
    
    #Display infinity
    graphEditorAC = "graphEditor1GraphEd"
    cmds.animCurveEditor(graphEditorAC, e = True, displayInfinities = "on")
    
makeInfinity()
