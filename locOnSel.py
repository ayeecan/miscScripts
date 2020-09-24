from maya import cmds

def getSelected():
    """Get Selection"""
    sel = cmds.ls(sl = True)
    
    if sel == []:
        return None
    else:
        return sel
        
def locOnSel():
    """
    Create a locator at selection
    If multiple objects are selected, a locator is created for each object
    """
    sel = getSelected()
    if sel is None:
        cmds.warning("Nothing Selected!")
        return
    
    for obj in sel:
        loc = cmds.spaceLocator()
        cmds.matchTransform(loc, obj)
    
locOnSel()
