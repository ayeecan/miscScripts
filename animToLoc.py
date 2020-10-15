from maya import cmds

def getSelected():
    """Get Selection"""
    sel = cmds.ls(sl = True)
    
    if sel == []:
        return None
    else:
        return sel
    
def constrainedLocator(obj):
    """Make and constrain a locator to an object"""
    prefix = 'BakedLoc__'
    locName = prefix + obj
    loc = cmds.spaceLocator(n = locName)[0]
    cons = cmds.parentConstraint(obj, loc, mo = False)[0]
    
    return loc, cons
        
def bakeList(list):
    """Bake a list of controls"""
    frameStart = int(cmds.playbackOptions(q = True, minTime = True))
    frameEnd = int(cmds.playbackOptions(q = True, maxTime = True))
        
    cmds.bakeResults(list, time = (frameStart, frameEnd))
        
def animToLoc():
    """Bake a locator to each selected item"""
    sel = getSelected()
    if sel is None:
        cmds.warning("Nothing Selected!")
        return
    
    locList = []
    consList = []
    for obj in sel:
        loc, cons = constrainedLocator(obj)
        locList.append(loc)
        consList.append(cons)
        
    bakeList(locList)
    cmds.delete(consList)
        
animToLoc()
