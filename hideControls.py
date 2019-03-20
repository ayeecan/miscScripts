from maya import cmds, mel

def createLayer(lyr_name = 'HideCtrlsLyr'):
    '''Create a display layer'''
    if not cmds.objExists(lyr_name):
        cmds.createDisplayLayer(name = lyr_name, empty = True)
    
    return lyr_name
        
def queryLayer(lyr_name):
    '''Return all objects within the display layer'''
    items_in_lyr = cmds.editDisplayLayerMembers(lyr_name, q = True)
    if items_in_lyr is None:
        items_in_lyr = []
        
    return items_in_lyr
        
def addToLayer(lyr_name, obj):
    '''Add object to layer'''
    cmds.editDisplayLayerMembers(lyr_name, obj, noRecurse = True)
    
    return obj
    
def removeFromLayer(obj):
    '''Remove objects from layer'''
    defaultLayer = 'defaultLayer'
    cmds.editDisplayLayerMembers(defaultLayer, obj, noRecurse = True)
        
    return obj
        
def getSelection():
    '''Return a list for selected objects'''    
    selection = cmds.ls(sl = True)

    return selection

def shapeListToObjectString(list):
    '''Return a list as a nice string'''
    new_string = ''
    for item_shape in list:
        item_parent = getParent(item_shape)
        new_string += ' {0}'.format(item_parent)
        
    return new_string

def singleListToString(list):
    '''Return first item in list as a string'''
    if list is None:
        new_string = []
    else:
        new_string = list[0]
    
    return new_string

def getShape(parent_obj):
    '''Return shape node'''
    node = cmds.listRelatives(parent_obj, shapes = True)
    node_string = singleListToString(node)
    
    return node_string
    
def getParent(shape_obj):
    '''Return parent node from shape node'''
    node = cmds.listRelatives(shape_obj, parent = True)
    node_string = singleListToString(node)
    
    return node_string

def runScript():
    '''Run script'''
    lyr_name = createLayer()
    sel = getSelection()
    
    for obj in sel:
        obj_shape = getShape(obj)
        
        objs_in_lyr = queryLayer(lyr_name)
        
        if obj_shape in objs_in_lyr:
            removeFromLayer(obj_shape)
        else:
            addToLayer(lyr_name, obj_shape)
        
    final_lyr_list = queryLayer(lyr_name)
    final_string = shapeListToObjectString(final_lyr_list)
    mel.eval('print "All Objects in {0}:{1}";'.format(lyr_name, final_string))

runScript()
