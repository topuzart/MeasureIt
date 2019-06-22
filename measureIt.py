import maya.cmds as mc

def mit(self):
    import maya.cmds as mc
    global LocCount

    # Empty list to append the object going to be measured.
    hero = []

    # Getting the name of the selected object in the following 2 lines.
    selection = mc.ls(sl=True)
    myObjectName = selection[0]

    # Adding selected object to the "hero" list.
    hero.append(myObjectName)

    # Creating a bounding box that selected object fits perfectly
    bbox = mc.exactWorldBoundingBox(myObjectName)

    temp = mc.ls('locator_*')
    if len(temp) == 0:
        LocCount = 0

    # Items exist in the scene before this script has been runned.
    scene_before = cmds.ls(l=True, transforms=True)

    bBoxCube = mc.polyCube(n='bBoxCube_{index}'.format(index=LocCount), w=bbox[3] - bbox[0], h=bbox[4] - bbox[1],
                           d=bbox[5] - bbox[2])
    mc.xform(bBoxCube, t=((bbox[3] + bbox[0]) / 2, (bbox[4] + bbox[1]) / 2, (bbox[5] + bbox[2]) / 2))

    heroPivotX = mc.getAttr(hero[0] + '.scalePivotX')
    heroPivotY = mc.getAttr(hero[0] + '.scalePivotY')
    heroPivotZ = mc.getAttr(hero[0] + '.scalePivotZ')

    mc.move(heroPivotX, heroPivotY, heroPivotZ, "bBoxCube_{index}.scalePivot".format(index=LocCount),
            "bBoxCube_{index}.rotatePivot".format(index=LocCount), absolute=True)

    xList = []
    xListSt = []
    xListSt2 = []

    yList = []
    yListSt = []
    yListSt2 = []

    zList = []
    zListSt = []
    zListSt2 = []

    vertPos = []
    vertPosList = []

    selection = mc.ls(sl=True)
    myObjectName = selection[0]

    for i in range(0, mc.polyEvaluate(v=True)):
        vertPos = mc.pointPosition(myObjectName + '.vtx[{index}]'.format(index=i))

        vertPosList.append(vertPos)
        xListSt.append(vertPos)
        yListSt.append(vertPos)
        zListSt.append(vertPos)

        xListSt2.append(vertPos)
        yListSt2.append(vertPos)
        zListSt2.append(vertPos)

    # Genişlik: +z,-y
    xListSt.sort(key=lambda x: (x[0], -x[2], x[1]))
    xListSt2.sort(key=lambda x: (-x[2], x[1], -x[0]))

    # Yükseklik: -z,+x
    yListSt.sort(key=lambda x: (x[2], -x[0], x[1]))
    yListSt2.sort(key=lambda x: (x[2], -x[0], -x[1]))

    # Derinlik: -x,-y
    zListSt.sort(key=lambda x: (x[0], x[1], x[2]))
    zListSt2.sort(key=lambda x: (x[0], x[1], -x[2]))

    posList = [xListSt, xListSt2, yListSt, yListSt2, zListSt, zListSt2]

    mc.hide('bBoxCube_{index}'.format(index=LocCount))

    mc.scaleConstraint(hero[0], 'bBoxCube_{index}'.format(index=LocCount), mo=True, w=1)
    mc.parentConstraint(hero[0], 'bBoxCube_{index}'.format(index=LocCount), mo=True, w=1)

    for i in posList:
        LocCount += 1
        mc.spaceLocator(n='locator_#')
        mc.move(i[0][0], i[0][1], i[0][2])
        mc.select(myObjectName + '.vtx[{index}]'.format(index=vertPosList.index(i[0])))
        mc.pointOnPolyConstraint(myObjectName + '.vtx[{index}]'.format(index=vertPosList.index(i[0])),
                                 'locator_{index}'.format(index=LocCount))
        if (LocCount % 2) == 0:
            mc.distanceDimension('locator_{index}'.format(index=LocCount - 1), 'locator_{index}'.format(index=LocCount))

    # Items exist in the scene after this script has been runned.
    scene_after = cmds.ls(l=True, transforms=True)

    # Last created items/Difference between scene_before - scene_after
    new_objs = list(set(scene_after).difference(scene_before))

    mc.group(new_objs, n=hero[0] + '_Dim_01')

def showSelObject(*args):
    sel = mc.ls(sl=True)
    add = mc.textField('tFld', edit=True, text=sel[0])

if mc.window("dumWin", exists=True):
    mc.deleteUI("dumWin")

# Specs of the window
myWindow = mc.window("dumWin", t="Measure it!", w=300, h=300)
# Creates an adjustable column
mc.columnLayout(adj=True)
# Define logo path
logoPath = mc.internalVar(upd=True) + "icons/MitLogo_02.png"
# logo display space specs
mc.image(w=300, h=100, image=logoPath)
mc.separator(w=300)
mc.separator(w=300)
mc.text("Select an item to measure.", align='center')
mc.separator(w=300)
# set parents ends the current layout
mc.setParent('..')
mc.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 75), (2, 150), (3, 75)])
mc.text("Selected Item:", align='center')
mc.textField('tFld')
mc.button(l="Update", c=showSelObject)
mc.setParent('..')
mc.columnLayout()
mc.separator(w=300)
mc.button(l="Measure", c=mit, w=300)
mc.separator(w=300)
mc.separator(w=300)
mc.setParent('..')
mc.columnLayout()
mc.text('Log:')
mc.separator(w=300)
mc.separator(w=300)

mc.textField(tx='You will see updates here.', w=300, h=150)
mc.showWindow(myWindow)


