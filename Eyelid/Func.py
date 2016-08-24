#!/bin/env python
# -*- coding: iso-8859-1 -*-
###############################################################################
#
# Copyright(c) 2015 Sukwon Shin, Jonghwan Hwang
# $Author: jhwang $
#
###############################################################################

import maya.cmds as cmds
import Base
reload(Base)

class Func(Base.Base):
    def __init__(self, **kw):
        """
        initializing variables
        """
        #local variables
        Base.Base.__init__(self, **kw)
        self.lrUplow = []
        for lr in self.prefix:
            self.lrUplow.append(lr + self.uploPrefix[0])
            self.lrUplow.append(lr + self.uploPrefix[1])
    
    #- new
    def jumperPanel(self):
        """
        """
        jumperPanel = 'jumperPanel'
        if not cmds.objExists(jumperPanel):
            #set the start with plusMinusAverage  
            cmds.group( n = "jumperPanel", em = 1, p = self.faceMainNode)   
    
        if not cmds.objExists('lids_EXP'):
            #set the start with plusMinusAverage
            
            cmds.group( n = "lids_EXP", em = 1, p = "jumperPanel")    
        upJnts = cmds.ls( self.prefix[0] + "upLidBlink*" + self.jntSuffix, fl =1, type= "joint")
        loJnts = cmds.ls( self.prefix[0] + "loLidBlink*" + self.jntSuffix, fl =1, type= "joint")
        upLen = len(upJnts)    
        loLen = len(loJnts)
        cmds.select ('lids_EXP') #lids_EXP: lid start/ end /open 
        #nodes for ValAB
        
        pushY_mult = cmds.shadingNode( 'multiplyDivide', asUtility =1, n ='lidPushY_mult')

        for LR in self.prefix:
    
            if LR == self.prefix[0]:
                XYZ = 'X'
    
            if LR == self.prefix[1]:
                XYZ = 'Y' 
             
            for i in range(0, max(upLen, loLen)): 
                #create each push_lid point in jumperPanel
                cmds.addAttr(jumperPanel, longName= LR + "upPush_Lid%s"%str(i), attributeType='float', dv = 0)
                cmds.addAttr(jumperPanel, longName= LR + "loPush_Lid%s"%str(i), attributeType='float', dv = 0)
                
                #Start = - .cv(LUpCrv.cv) -   +  push_Lid5 + ctrl.ty* *  .squint
                cmds.addAttr('lids_EXP', longName= LR + "upEyeStart%s"%str(i), attributeType='float', dv = 0)
                ##eyeOpenCrv shape(start + blinkCtrl) : upEyeStart0 -lids_EXP.l_upGap*l_eyeBlink.ty*(1-blinkLevel)
                cmds.addAttr('lids_EXP', longName= LR +"upEyeOpen%s"%str(i), attributeType='float', dv = 0)
                #blink target POC.positionY on the loEyeCrv
                cmds.addAttr('lids_EXP', longName= LR +"EyeEnd%s"%str(i), attributeType='float', dv = 0)
            
                cmds.addAttr('lids_EXP', longName= LR +"loEyeStart%s"%str(i), attributeType='float', dv = 0)
                cmds.addAttr('lids_EXP', longName= LR +"loEyeOpen%s"%str(i), attributeType='float', dv = 0)
                 
            #Y = lookUp/Down  X = lookLeft/Right           
            cmds.addAttr(jumperPanel, longName= LR + "lidPushY", attributeType='float', dv = 0)                      
            cmds.addAttr(jumperPanel, longName= LR + "lidPushX", attributeType='float', dv = 0) 
            
            cmds.addAttr(jumperPanel, longName= LR + "valA", attributeType='float', dv = 0)
            cmds.addAttr(jumperPanel, longName= LR + "valB", attributeType='float', dv = 0)
            
            
            #make -JumperPanel.l_lidPushY into +
            cmds.connectAttr('jumperPanel.' + LR + 'lidPushY', pushY_mult + '.input1'+XYZ)
            cmds.setAttr(pushY_mult + '.input2'+XYZ, -1)
            
            #ValA and ValB define by LidPushY clamp
            pushY_clamp = cmds.shadingNode( 'clamp', asUtility =1, n = LR + 'lidPushY_clamp')
            cmds.setAttr(pushY_clamp + '.maxR', 1)
            cmds.setAttr(pushY_clamp + '.maxG', 1)
            #ValAB / LidPushY defined by l_eyeballRotX 
            cmds.connectAttr('jumperPanel.' + LR + 'lidPushY', pushY_clamp + '.inputR')
            cmds.connectAttr(pushY_mult + '.output'+XYZ, pushY_clamp + '.inputG')
            cmds.connectAttr( pushY_clamp + '.outputR', 'jumperPanel.' + LR + 'valA') # l_valA = + lidPushY
            cmds.connectAttr( pushY_clamp + '.outputG', 'jumperPanel.' + LR + 'valB')# l_valB = -(-lidPushY)        
            
            #l_eyeballRotX --> 'jumperPanel.l_lidPushY'
            
            eyeRotX_mult = cmds.shadingNode( 'multiplyDivide', asUtility =1, n = LR + 'eyeRotX_mult')
            rotX_invert = cmds.shadingNode( 'multiplyDivide', asUtility =1, n = LR + 'rotX_invert')
            cmds.connectAttr(self.faceFactors['eyelid'] + '.eyeBallRotX_scale', rotX_invert + '.input1X')
            cmds.setAttr(rotX_invert + '.input2X', -1)
    
            cmds.setAttr(eyeRotX_mult + '.operation', 2)
            cmds.connectAttr(LR + 'eyeballRot.rotateX', eyeRotX_mult + '.input1X')
            cmds.connectAttr(rotX_invert + '.outputX', eyeRotX_mult + '.input2X')
            
            eyeUD_mult = cmds.shadingNode( 'multiplyDivide', asUtility =1, n = LR + 'eyeUD_mult')
            cmds.connectAttr(eyeRotX_mult + '.outputX', eyeUD_mult + '.input1X')
            cmds.connectAttr(eyeRotX_mult + '.outputX', eyeUD_mult + '.input1Y')
            cmds.connectAttr('faceFactors.range_'+LR+'eyeU', eyeUD_mult + '.input2X')
            cmds.connectAttr('faceFactors.range_'+LR+'eyeD', eyeUD_mult + '.input2Y')
            
            pushY_con = cmds.shadingNode( 'condition', asUtility =1, n = LR + 'lidPushY_con')
            cmds.connectAttr(LR + 'eyeballRot.rotateX', pushY_con+'.firstTerm')
            cmds.setAttr(pushY_con+".secondTerm", 0)
            cmds.setAttr(pushY_con+".operation", 4)
            cmds.connectAttr(eyeUD_mult + '.outputX', pushY_con+ '.colorIfTrueR')
            cmds.connectAttr(eyeUD_mult + '.outputY', pushY_con+ '.colorIfFalseR')
            cmds.connectAttr(pushY_con+ '.outColorR', 'jumperPanel.' +LR+ 'lidPushY')
            
            #l_eyeballRotY --> 'jumperPanel.l_lidPushX'
            eyeRotY_mult = cmds.shadingNode( 'multiplyDivide', asUtility =1, n = LR + 'eyeRotY_mult')
            cmds.setAttr(eyeRotY_mult + '.operation', 2)
            cmds.connectAttr(self.faceFactors['eyelid'] + '.eyeBallRotY_scale', eyeRotY_mult + '.input2X')
            cmds.connectAttr(self.faceFactors['eyelid'] + '.eyeBallRotY_scale', eyeRotY_mult + '.input2Y')
            cmds.connectAttr(LR + 'eyeballRot.rotateY', eyeRotY_mult + '.input1X')
            cmds.connectAttr(LR + 'eyeballRot.rotateY', eyeRotY_mult + '.input1Y')
            
            eyeLR_mult = cmds.shadingNode( 'multiplyDivide', asUtility =1, n = LR + 'eyeLR_mult')
            cmds.connectAttr(eyeRotY_mult + '.outputX', eyeLR_mult + '.input1X')
            cmds.connectAttr(eyeRotY_mult + '.outputX', eyeLR_mult + '.input1Y')
            cmds.connectAttr('faceFactors.range_'+LR+'eyeR', eyeLR_mult + '.input2X')
            cmds.connectAttr('faceFactors.range_'+LR+'eyeL', eyeLR_mult + '.input2Y')
            
            pushX_con = cmds.shadingNode( 'condition', asUtility =1, n = LR + 'lidPushX_con')
            cmds.connectAttr(LR + 'eyeballRot.rotateY', pushX_con +'.firstTerm')
            cmds.setAttr(pushY_con+".secondTerm", 0)
            cmds.setAttr(pushY_con+".operation", 4)
            cmds.connectAttr(eyeLR_mult + '.outputX', pushX_con+ '.colorIfTrueG')
            cmds.connectAttr(eyeLR_mult + '.outputY', pushX_con+ '.colorIfFalseG')
            cmds.connectAttr(pushX_con+ '.outColorG', 'jumperPanel.' +LR+ 'lidPushX') 
            
        
    def crvCtrlToJnt(self, uploPrefix, lidCtl, jnt, wideJnt, pocNode, wideJntPocNode, ctlPocNode, initialX, RotateScale ,miValue, index):
        #connect browCtrlCurve and controller to the brow joints
        shadingNodePrefix = uploPrefix + 'Eyelid'
        ctlMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = shadingNodePrefix + 'CtlMult' + str(index))
        wideJntMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = shadingNodePrefix + 'wideJntMult' + str(index))
        plusXAvg = cmds.shadingNode('plusMinusAverage', asUtility=True, n = shadingNodePrefix + 'PlusX' + str(index))
        wideJntAddX = cmds.shadingNode('addDoubleLinear', asUtility=True, n = shadingNodePrefix + 'wideJntAddX' + str(index))
        plusYAvg = cmds.shadingNode('plusMinusAverage', asUtility=True, n = shadingNodePrefix + 'PlusY' + str(index))
        totalY = cmds.shadingNode('addDoubleLinear', asUtility=True, n = shadingNodePrefix+ 'YAdd' + str(index))
        blinkRemap = cmds.shadingNode('remapValue', asUtility=True, n = shadingNodePrefix + 'Remap' + str(index))
        blinkGap = cmds.shadingNode('addDoubleLinear', asUtility=True, n = shadingNodePrefix + 'BlinkGap_yAdd' + str(index))
                
        #- Jonghwan fix(not sure if it is correct) for right side controller
        if uploPrefix.startswith(self.prefix[1]):
            miValue = miValue * -1
        
        #TranslateX add up
        #1. curve translateX add up 
        cmds.setAttr(plusXAvg + '.operation', 1) 
        cmds.connectAttr(pocNode + '.positionX', plusXAvg + '.input1D[0]') 
        cmds.setAttr(plusXAvg + '.input1D[1]', -initialX)
        cmds.connectAttr(ctlPocNode + '.positionX', plusXAvg + '.input1D[2]') 
        cmds.setAttr(plusXAvg + '.input1D[3]', -initialX) 
        cmds.connectAttr(wideJntPocNode + '.positionX', wideJntAddX + '.input1') 
        cmds.setAttr(wideJntAddX + '.input2', -initialX) 
        cmds.connectAttr(wideJntAddX + '.output', plusXAvg + '.input1D[4]')
        #2. add miro control translateX 
        cmds.connectAttr(lidCtl + '.tx', plusXAvg + '.input1D[5]')
        #3. multiply XRotateScale
        cmds.connectAttr(plusXAvg + '.output1D', ctlMult + '.input1X')
        cmds.setAttr(ctlMult + '.input2X', miValue * RotateScale)
        cmds.connectAttr(wideJntAddX + '.output', wideJntMult + '.input1X')
        cmds.setAttr(wideJntMult + '.input2X', miValue * RotateScale)
        
        #4. connect jnt rotateY
        cmds.connectAttr(ctlMult + '.outputX', jnt + '.ry') 
        cmds.connectAttr(wideJntMult + '.outputX', wideJnt + '.ry')   
            
        # translateY add up
        #1. curve translateY add up 
        cmds.setAttr(plusXAvg + '.operation', 1)
        cmds.connectAttr(pocNode + '.positionY', plusYAvg + '.input1D[0]')
        cmds.connectAttr(ctlPocNode + '.positionY', plusYAvg + '.input1D[1]')
        cmds.connectAttr(wideJntPocNode + '.positionY', plusYAvg + '.input1D[2]') 
        #2. add miro control translateY 
        cmds.connectAttr(lidCtl + '.ty', plusYAvg + '.input1D[3]')
        
        #3. multiply YRotateScale
        cmds.connectAttr(plusYAvg + '.output1D', ctlMult + '.input1Y')
        cmds.setAttr(ctlMult + '.input2Y', -RotateScale)
        cmds.connectAttr(wideJntPocNode + '.positionY', wideJntMult + '.input1Y')
        cmds.setAttr(wideJntMult + '.input2Y', -RotateScale)   
        
        #4. connect jnt rotateX
        if self.uplo[0] in jnt: 
            blinkRemap = cmds.shadingNode('remapValue', asUtility=True, n = jnt.split('Blink', 1)[0] + str(index+1).zfill(2)+'_remap')
            cmds.connectAttr(ctlMult + ".outputY", blinkRemap + '.outputMin') 
            cmds.connectAttr(blinkRemap + '.outValue',  jnt + '.rx')
            cmds.connectAttr(wideJntMult + '.outputY', wideJnt + '.rx') 
        
        elif self.uplo[1] in jnt: 
            #get the remap from upJoint
            upJnt = jnt.replace("_lo","_up")
            cmds.connectAttr(ctlMult + ".outputY", blinkGap + ".input1") 
            cmds.connectAttr(blinkGap + ".output",(upJnt.split('Blink',1)[0] + str(index+1).zfill(2)+'_remap'+'.outputMax'))  
            cmds.connectAttr(ctlMult + ".outputY",  jnt + '.rx') 
            cmds.connectAttr(wideJntMult + '.outputY', wideJnt + '.rx')

    def createLidCtl(self, miNum):
        """
        create sub controller for the control panel
        """
           
        for updn in self.lrUplow:
            ctlP = updn + "Ctrl0"
            kids = cmds.listRelatives(ctlP, ad=True, type ='transform')   
            if kids:
                cmds.delete(kids)
                    
            cntCtlP = cmds.duplicate(ctlP, po =True, n = updn + 'CntCtlP')
            cmds.parent(cntCtlP[0],ctlP)
            cntCtl = cmds.circle(n = updn + "Center", ch=False, o =True, nr =(0, 0, 1), r = 0.1 )
            cntCtl[0]
            cmds.parent(cntCtl[0], cntCtlP[0])
            cmds.setAttr(cntCtl[0] + ".overrideEnabled", 1)
            cmds.setAttr(cntCtl[0] + "Shape.overrideEnabled", 1)
            cmds.setAttr(cntCtl[0] + "Shape.overrideColor", 9)
            cmds.setAttr(cntCtl[0] + '.translate', 0,0,0)
            cmds.transformLimits(cntCtl, tx =(-1, 1), etx=(True, True))
            cmds.transformLimits(cntCtl, ty =(-1, 1), ety=(True, True))
        
            inCornerP = cmds.duplicate(cntCtlP , n = updn + 'InCornerP', rc =True)
            cmds.setAttr(inCornerP[0] +'.tx', -1)
            inTemp = cmds.listRelatives(inCornerP[0], c=True, type ='transform') 
            inCorner = cmds.rename(inTemp[0], updn + 'InCorner')
            cmds.setAttr(inCorner +'.scale', .8, .8, .8)
            cmds.transformLimits(inCorner, tx =(-.25, .25), etx=(True, True))
            cmds.transformLimits(inCorner, ty =(-1,  1), ety=(True, True))
                    
            outCornerP = cmds.duplicate(cntCtlP , n = updn + 'OutCornerP', rc=True)
            cmds.setAttr(outCornerP[0] +'.tx', 1)
            outTemp = cmds.listRelatives(outCornerP[0], c=True, type ='transform') 
            outCorner = cmds.rename(outTemp[0], updn + 'OutCorner') 
            cmds.setAttr(outCorner +'.scale', .8, .8, .8) 
            cmds.transformLimits(outCorner, tx =(-.25, .25), etx=(True, True))
            cmds.transformLimits(outCorner, ty =(-1, 1), ety=(True, True))
            
            attTemp = ['scaleX','scaleY','scaleZ', 'rotateX','rotateY','rotateZ', 'tz', 'visibility' ]  
            for x in attTemp:
                cmds.setAttr(cntCtl[0] +"."+ x, lock = True, keyable = False, channelBox =False)
                cmds.setAttr(inCorner +"."+ x, lock = True, keyable = False, channelBox =False) 
                cmds.setAttr(outCorner+"."+ x, lock = True, keyable = False, channelBox =False) 
        
            for i in range(0, miNum):
                detailCtl = cmds.spaceLocator(n = updn  + 'Detail' + str(i+1).zfill(2))
                detailCtlP = cmds.group(em =True, n = updn  + 'Detail'+ str(i+1).zfill(2) + 'P')
                cmds.parent(detailCtl[0], detailCtlP)
                cmds.parent(detailCtlP, ctlP)
                cmds.setAttr(detailCtl[0] +".overrideEnabled", 1)
                cmds.setAttr(detailCtl[0] +"Shape.overrideEnabled", 1)
                cmds.setAttr(detailCtl[0]+"Shape.overrideColor", 20)
                increment = 2.0 /(miNum-1)
                cmds.setAttr(detailCtlP + ".tx", increment*i - 1.0)
                cmds.setAttr(detailCtlP + ".ty", 0)
                cmds.setAttr(detailCtlP + ".tz", 0)
                cmds.xform(detailCtl, r =True, s =(0.1, 0.1, 0.1))
                cmds.transformLimits(detailCtl , tx =(-.25, .25), etx=(True, True))
                cmds.transformLimits(detailCtl , ty =(-.5, .5), ety=(True, True))
                for y in attTemp:
                    cmds.setAttr(detailCtl[0] +"."+ y, lock = True, keyable = False, channelBox =False)

    def lidControlConnect(self): 
        """
        connect with control panel
        """
        for pos in self.lrUplow:
            ctlCrvCv = cmds.ls(pos + 'Ctl' + self.crvSuffix + '.cv[*]', fl =True)
            print ctlCrvCv
            cvNum = len(ctlCrvCv)
        
            # lidCtl drive the center controlPoints on ctlCrv
            if not (pos + "Center") and (pos +"InCorner") and (pos + "OutCorner"):
                print "create lid main controllers"
            else :
                
                cntAddD = cmds.shadingNode('addDoubleLinear', asUtility=True, n= pos + "Cnt_AddD")            
                cmds.connectAttr(pos + "InCorner.ty" , ctlCrvCv[0] + ".yValue")
                cmds.connectAttr(pos + "InCorner.ty" , ctlCrvCv[1] + ".yValue")
                cmds.setAttr(ctlCrvCv[0] + ".xValue" , lock = True)     
                cmds.setAttr(ctlCrvCv[1] + ".xValue" , lock = True) 
                cmds.connectAttr(pos + "Center.ty" , ctlCrvCv[2] + ".yValue")  
                # center control X match to center point (lidCtl_crv)
                
                if self.prefix[0] in pos :
                    cmds.connectAttr(pos + "Center.tx", cntAddD + ".input1")
                    cmds.setAttr (cntAddD + ".input2", 0.5) 
                    cmds.connectAttr(cntAddD + ".output" , ctlCrvCv[2] + ".xValue")
                    
                if self.prefix[1] in pos :
                    cntMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = pos +'Cnt_mult')
                    cmds.connectAttr(pos + "Center.tx" , cntMult + ".input1X") 
                    cmds.setAttr(cntMult + ".input2X", -1)
                    cmds.connectAttr(cntMult + ".outputX", cntAddD + ".input1")
                    cmds.setAttr (cntAddD + ".input2", 0.5) 
                    cmds.connectAttr(cntAddD + ".output" , ctlCrvCv[2] + ".xValue")            
                 
                cmds.connectAttr(pos + "OutCorner.ty" , ctlCrvCv[3] + ".yValue")
                cmds.connectAttr(pos + "OutCorner.ty" , ctlCrvCv[4] + ".yValue")
                cmds.setAttr(ctlCrvCv[3] + ".xValue", lock = True )  
                cmds.setAttr(ctlCrvCv[4] + ".xValue", lock = True )   
        
            detailPCtls = cmds.ls(pos + "Detail*P", type = 'transform')

            details = []
            for mom in detailPCtls :
                kid= cmds.listRelatives(mom, c = True, type = 'transform')
                details.append(kid[0])
                        
            ctlNum = len (details) 
                
            for i in range (0, ctlNum):
                # POC on ctlCrv drive detail control parent  
                cntRemoveX = cmds.shadingNode('addDoubleLinear', asUtility=True, n= pos +"Cnt"+ str(i+1)+"RemoveX")
                momMult = cmds.shadingNode('multiplyDivide', asUtility=True, n = pos +'Mom'+ str(i+1)+'_mult')
                cmds.connectAttr(pos + "CtlPoc0" +str(i+1) +".positionY", detailPCtls[i] + ".ty")
                #Xvalue match between POC and CtrlP
                cmds.connectAttr(pos + "CtlPoc0" +str(i+1) +".positionX", momMult + ".input1X")        
                cmds.connectAttr(momMult + ".outputX", cntRemoveX + ".input1")
                if "l_" in pos :
                    cmds.setAttr(momMult + ".input2X", 2)
                    cmds.setAttr( cntRemoveX  + ".input2", -1) 
                    cmds.connectAttr(cntRemoveX +".output", detailPCtls[i] + ".tx")
                if "r_" in pos :
                    cmds.setAttr(momMult + ".input2X", -2)
                    cmds.setAttr( cntRemoveX  + ".input2", 1)              
                    cmds.connectAttr(cntRemoveX +".output", detailPCtls[ctlNum-i-1] + ".tx")
                    
                # detail control drive the joint(add to the +-Average node)
                cmds.connectAttr(details[i] + ".tx", pos +"EyelidPlusX" + str(i+1) + ".input1D[6]") 
                cmds.connectAttr(details[i] + ".ty", pos +"EyelidPlusY" + str(i+1) + ".input1D[4]")
    
    def __allCrvs(self):
        crvs = []
        
        if not cmds.objExists(self.eyelidCrvGrpName):
            print "curve is not setup yet"
        else:
            topLidCrvGrp = cmds.listRelatives(self.eyelidCrvGrpName)
            for topGrp in topLidCrvGrp:
                for crv in cmds.listRelatives(topGrp):        
                    crvs.append(crv)
        return crvs
    
    def hideAlLCrv(self):
        """
        hide all curves
        """
        crvs = self.__allCrvs()
        for crv in crvs:
            cmds.setAttr(crv + '.v', 0)
                
        return crvs
        
    def showCrv(self, crv):
        """
        unhide crv
        """
        if not cmds.objExists(crv):
            print "curve does not exists"
        else:
            self.hideAlLCrv()
            cmds.setAttr(crv + '.v', 1)
    
    def saveEyelidCrvInfo(self):
        """
        save eyelid curve's info as json file
        """
        crvs = self.__allCrvs()
        allCrvInfo = {}
        for crv in crvs:
            allCrvCvs = cmds.ls(crv + '.cv[*]', fl = True)
            allCrvCvs = [x for x in allCrvCvs if 'Ctl' + self.crvSuffix not in x]
            for crvCv in allCrvCvs:
                #cmds.xform(crvCv, t = True, q = True, ws = True)
                allCrvInfo[crvCv] = cmds.xform(crvCv, t = True, q = True, ws =True)
        
        self.writeJsonFile(self.eyelidCrvJsonLoc, allCrvInfo)
        cmds.confirmDialog(title='Eyelid Curve info Saved',
                           message='Location : %s' %self.eyelidCrvJsonLoc,
                           button=['ok'],
                           defaultButton='ok')
        
        return self.eyelidCrvJsonLoc
    
    def loadEyelidCrvInfo(self):
        """
        retrieve curves with data saved
        """
        crvData = self.readJsonFile(self.eyelidCrvJsonLoc)
        for eachCrv in crvData.keys():
            print eachCrv
            cmds.xform(eachCrv, t = crvData[eachCrv], ws =True)
        
        return crvData
        