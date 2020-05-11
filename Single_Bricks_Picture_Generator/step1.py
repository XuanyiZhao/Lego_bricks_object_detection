'''
Run this code in the AutoDesk Maya Python Script Editor!
Start with a new empty scene. The script will setup the cameras and softbox lighting for you.
Copyright Joost Hazelzet, script is provided under MIT License.
'''

import maya.cmds as cmds
from mtoa.cmds.arnoldRender import arnoldRender
import mtoa.ui.arnoldmenu as arnoldmenu;
import mtoa.utils as mutils
from os import listdir
from os.path import isfile, join
import random

#Setup the cameras
cmds.camera(centerOfInterest=5, focalLength=170, lensSqueezeRatio=1, cameraScale=1, horizontalFilmAperture=1.41732,
        horizontalFilmOffset=0, verticalFilmAperture=0.94488, verticalFilmOffset=0, filmFit='fill', overscan=1,
        motionBlur=0, shutterAngle=144, nearClipPlane=0.1, farClipPlane=10000, orthographic=0, orthographicWidth=30,
        panZoomEnabled=0, horizontalPan=0, verticalPan=0, zoom=1)
nameCameraRight = cmds.ls(selection=True)[0]
cmds.move( 19., 0., 19., r=False )
cmds.rotate( 0., 45., 0., r=False )

cmds.camera(centerOfInterest=5, focalLength=170, lensSqueezeRatio=1, cameraScale=1, horizontalFilmAperture=1.41732,
        horizontalFilmOffset=0, verticalFilmAperture=0.94488, verticalFilmOffset=0, filmFit='fill', overscan=1,
        motionBlur=0, shutterAngle=144, nearClipPlane=0.1, farClipPlane=10000, orthographic=0, orthographicWidth=30,
        panZoomEnabled=0, horizontalPan=0, verticalPan=0, zoom=1)
nameCameraLeft = cmds.ls(selection=True)[0]
cmds.move( -19., 0., 19., r=False )
cmds.rotate( 0., -45., 0., r=False )

print(nameCameraRight, nameCameraLeft)


#Setup the lighting
cmds.polyPlane(width=1, height=1, subdivisionsX=10, subdivisionsY=10, axis=[0,1,0], createUVs=2,constructionHistory=True)
mutils.createMeshLight()
nameLight = cmds.ls(selection=True)[0]
cmds.setAttr(nameLight+"Shape.intensity", 10)
cmds.setAttr(nameLight+"Shape.aiExposure", 5)
cmds.setAttr(nameLight+".scaleX", 20)
cmds.setAttr(nameLight+".scaleZ", 20)
cmds.setAttr(nameLight+".rotateX", -90)
cmds.setAttr(nameLight+".translateZ", 3)

print(nameLight)
