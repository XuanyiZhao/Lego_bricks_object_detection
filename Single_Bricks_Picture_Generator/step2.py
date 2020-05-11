#Prepare the renderer
cmds.setAttr("defaultArnoldDriver.ai_translator", "png", type="string")
random.seed(1)

def RenderLegoBrick(pathBricks, frames, cameraRight, cameraLeft, test):
    if test:
        brickFiles = ['3001 brick 2x4.dae']
    else:
        brickFiles = [f for f in listdir(pathBricks) if isfile(join(pathBricks, f))]

    print('{0} brick models found.'.format(len(brickFiles)))
    processed=0
    images=0

    for brickFile in brickFiles:

        print('Process Collada file: '+brickFile)
        brickName = brickFile.split('.')[0]

        #Remove all former brick parts if any
        if cmds.ls('Part_*') != []:
            cmds.select('Part_*')
            cmds.delete()

        #Import the Collada file. This generates a Part_.. node in the scene
        daeFile = pathBricks+brickFile
        cmds.file(daeFile, type="DAE_FBX", i=True, ra=True, ignoreVersion=True, options="v=0;",
                importTimeRange="combine", pr=True, mergeNamespacesOnClash=True )

        #Set the reflectivity, color and center the Part node
        cmds.select('Part_*', r=True)
        part = cmds.ls(sl=True,long=False)
        phong = cmds.defaultNavigation(defaultTraversal=True, destination=part+'*.surfaceShader')
        cmds.setAttr(phong+'.reflectivity', 0.24)
        cmds.setAttr(phong+'.color', 0.5, 0.5, 0.5, type='float3')
        cmds.xform(centerPivots=True)
        cmds.move( 0., 0., 0., rpr=True ) #Move pivot to center of brick

        #Rotate the Part node randomly along the x, y and z axis, render via the 2 cameras and saves the result
        for i in range(frames):
            rotx = random.random()*360
            roty = random.random()*360
            rotz = random.random()*360
            cmds.rotate(rotx, roty, rotz, r=False )
            fileName = "{0} {1:03d}".format(brickName, i)
            cmds.setAttr("defaultArnoldDriver.pre", fileName+"R", type="string")
            arnoldRender(400, 400, False, False, cameraRight, ' -layer defaultRenderLayer')
            cmds.setAttr("defaultArnoldDriver.pre", fileName+"L", type="string")
            arnoldRender(400, 400, False, False, cameraLeft, ' -layer defaultRenderLayer')
        processed += 1
        images += frames*2

    print('{0} brick models processed.'.format(processed))
    print('{0} images generated.'.format(images))

# Use this command to start the rendering process.
# The import statements, nameCameraRight and nameCameraLeft are defined in the previous scene setup script.
RenderLegoBrick('Users/zhaoxuanyi/Desktop/', 20, nameCameraRight, nameCameraLeft, True)
