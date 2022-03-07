from maya import cmds

curPanel = cmds.getPanel(withFocus = True)

if cmds.modelPanel(curPanel, exists = True):
    toggleGP = cmds.modelEditor(curPanel, q = True, greasePencils = True)
    cmds.modelEditor(curPanel, e = True, greasePencils = not toggleGP)
