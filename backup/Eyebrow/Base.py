#!/bin/env python
# -*- coding: iso-8859-1 -*-
###############################################################################
#
# Copyright (c) 2015 Sukwon Shin, Jonghwan Hwang
# $Author: jhwang $
#
###############################################################################

# brow joints create
'''select left brow vertex points and pivot point. run the script
  name = centerBrowBase0l, EyeBrowBase01... '''

import maya.cmds as cmds

from arFace.Misc import Core 
reload(Core)
from arFace.Misc import Util
reload(Util)
from arFace.Misc import Controller
reload(Controller)

class Base(Core.Core, Util.Util, Controller.Controller):
    def __init__(self, **kw):
        """
        initializing variables
        """
        
        #initializing Global variables
        #super(Core.Core, self, **kw).__init__()
        Core.Core.__init__(self, **kw)
        Util.Util.__init__(self)
        Controller.Controller.__init__(self)
        
        #initializing local variables
        self.jntName          = 'Brow0'
        self.browBase         = 'BrowBase'
        self.baseCntJntName   = self.cPrefix + self.browBase
        self.parentCntJntName = self.cPrefix + 'BrowP'
        self.ljntName         = self.prefix[0] + self.jntName
        self.baseJntName      = self.prefix[0] + 'BrowBase'
        self.parentJntName    = self.prefix[0] + 'BrowP'
        
        self.eyeBrowVtxs      = self.locData['eyebrowVtxs']
        self.eyeBrowLoc       = self.locData['eyebrowLoc']