from maya import cmds

def getObjs():
    """Get Objects from keys"""
    animCurves = cmds.keyframe(q = True, sl = True, n = True)
    if animCurves is None:
        return animCurves
    
    objs = cmds.listConnections(animCurves)
    
    return objs

def selFromKeys():
    """Select object(s) from selected keyframe(s) in graph editor"""
    objs = getObjs()
    
    if objs is None:
        cmds.warning("Please select at least one keyframe")
    else:
        cmds.select(objs, r = True)
    
selFromKeys()
