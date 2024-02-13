from maya import cmds, mel

curVisPanels = cmds.getPanel(vis = True)
graphPanel = cmds.getPanel(withLabel = 'Graph Editor')

cmds.scriptedPanel(graphPanel, e = True, tearOff = True)
newVisPanels = cmds.getPanel(vis = True)

oddPanels = set(curVisPanels).symmetric_difference(newVisPanels)
newPanel = ''
for i in oddPanels:
    if i != graphPanel:
        newPanel = i
        break

cmds.scriptedPanel(graphPanel, e = True, replacePanel = newPanel)
