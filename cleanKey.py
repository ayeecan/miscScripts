from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide2 import QtWidgets
from maya import cmds, mel

class cleanKeyWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(cleanKeyWindow, self).__init__(parent = parent)

        self.cbName = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')
        
        version_number = '1.0.0'
        windowTitle    = 'Cleanup Keys'
        info_name      = '{0} {1}'.format(windowTitle, version_number)
        
        mainWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(mainWidget)
        self.setWindowTitle(info_name)
        self.setMinimumWidth(275)
        
        cleanBtn = QtWidgets.QPushButton(windowTitle, self)
        cleanBtn.released.connect(self.cleanupKeys)
        bufferLbl = QtWidgets.QLabel('Tolerance:', self)
        self.bufferSpin = QtWidgets.QDoubleSpinBox(self)
        self.bufferSpin.setValue(0.01)
        
        bufferLayout = QtWidgets.QHBoxLayout()
        bufferLayout.addStretch()
        bufferLayout.addWidget(bufferLbl)
        bufferLayout.addWidget(self.bufferSpin)
        bufferLayout.addStretch()
        
        mainLayout = QtWidgets.QVBoxLayout(mainWidget)
        mainLayout.addLayout(bufferLayout)
        mainLayout.addWidget(cleanBtn)
        mainLayout.addStretch()
        
    def getObj(self):
        '''Get Selected Object(s)'''
        selObjs = cmds.ls(sl = True)
        
        return selObjs
        
    def getCbAttr(self):
        '''Get Selected Channel Box Attribute(s)'''
        selAttrs = cmds.channelBox(self.cbName, q = True, selectedMainAttributes = True)
        
        return selAttrs
        
    def fullAttrName(self, obj, attr):
        '''Reformat "obj" and "attr" to "obj.attr"'''
        fullName = '{0}.{1}'.format(obj, attr)
        
        return fullName
        
    def attrFromCurveName(self, curveName):
        '''Gat Attribute Name from Animation Curve Name'''
        obj, rpart, attr = curveName.rpartition('_')
        
        return attr
        
    def getAttrFromKey(self, obj, keyTime):
        '''Get Attribute from Keyframe'''
        fullName = cmds.keyframe(obj, q = True, name = True, time = (keyTime,keyTime))[0]
        attr = self.attrFromCurveName(fullName)
        
        return attr
        
    def getAttrValue(self, obj, attr, time):
        '''Get Attribute's Value'''
        attrName = self.fullAttrName(obj, attr)
        value = cmds.getAttr(attrName, time = time)
        
        return value
        
    def getKey(self):
        '''Get Selected Keyframe(s)'''
        keyDict = {}
        keyTimes = cmds.keyframe(q = True, sl = True)
        keyNames = cmds.keyframe(q = True, sl = True, n = True)
        attrs = []
        
        if keyNames:
            for name in keyNames:
                attr = self.attrFromCurveName(name)
                attrs.append(attr)
        
        if keyTimes:
            for i, time in enumerate(keyTimes):
                keyDict[attrs[i]] = time
        
        return keyDict
        
    def getKeysFromAttr(self, obj, attr):
        '''Get All Keyframes from Attribute'''
        keyTimes = cmds.keyframe(obj, q = True, at = attr)
        
        return keyTimes
        
    def getKeyValue(self, obj, attr, keyTime):
        '''Get Keyframe's value'''
        value = cmds.keyframe(obj, q = True, valueChange = True, at = attr, time = (keyTime,keyTime))
        value_float = float(value[0])
        
        return value_float
        
    def setKey(self, obj, attr, value, keyTime):
        '''Set Keyframe'''
        keysAdded = cmds.setKeyframe(obj, attribute = attr, value = value, time = keyTime)
        
        return keysAdded
        
    def removeKey(self, obj, attr, keyTime):
        '''Remove Keyframe'''
        keysRemoved = cmds.cutKey(obj, attribute = attr, time = (keyTime,keyTime))
        
        return keysRemoved
        
    def compareKey(self, obj, attr, keyTime, buffer):
        '''
        Decides if a key is necessary at the specified time
        Returns used value along with old and new values
        '''
        valueOld = self.getKeyValue(obj, attr, keyTime)
        maxValue = valueOld + buffer
        minValue = valueOld - buffer
        valueUsed = 0
        
        self.removeKey(obj, attr, keyTime)
        valueNew = self.getAttrValue(obj, attr, keyTime)
        
        if valueNew > maxValue or valueNew < minValue:
            self.setKey(obj, attr, valueOld, keyTime)
            valueUsed = valueOld
        else:
            valueUsed = valueNew
            
        return valueUsed, valueOld, valueNew
        
    def createBufferCurve(self, obj):
        '''Create Buffer Curve'''
        curvesMade = cmds.bufferCurve(obj, an = 'objects', overwrite = True)
        
        return curvesMade
        
    def cleanupKeys(self):
        '''Cleanup Unnecessary Keys'''
        obj_list  = self.getObj()
        key_dict  = self.getKey()
        attr_list = self.getCbAttr()
        buffer    = self.bufferSpin.value()
        
        if len(obj_list) == 0:
            cmds.warning('Nothing selected')
            return
            
        for obj in obj_list:
            self.createBufferCurve(obj)
        
            if key_dict:
                for keyAttr in key_dict:
                    keyTime = key_dict[keyAttr]
                    self.compareKey(obj, keyAttr, keyTime, buffer)
            elif attr_list:
                self.cleanFromAttr(obj, attr_list, buffer)
            else:
                objAttrs = cmds.listAttr(obj, keyable = True, unlocked = True)
                self.cleanFromAttr(obj, objAttrs, buffer)
                
        mel.eval('print "Old Curves Have Been Saved in Buffer Curves.";')
    
    def cleanFromAttr(self, obj, attr_list, buffer):
        '''Cleanup from Attributes'''
        for attr in attr_list:
            keys = self.getKeysFromAttr(obj, attr)
            if keys is None:
                continue
            startKey = keys[0]
            endKey = keys[-1]
            for key in keys:
                if key == startKey or key == endKey:
                    continue
                self.compareKey(obj, attr, key, buffer)
def launchUI():
    window = None
    uiName = 'cleanKeyUI'
    
    if uiName in globals() and globals()[uiName].isVisible():
        window = globals()[uiName]
        if window.isVisible():
            window.show()
            window.raise_()
            return None
            
    nuWindow = cleanKeyWindow()
    globals()[uiName] = nuWindow
    nuWindow.show(dockable = True, floating = True)