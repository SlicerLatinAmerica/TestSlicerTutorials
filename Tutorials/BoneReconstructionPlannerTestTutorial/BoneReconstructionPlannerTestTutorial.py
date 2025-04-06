# Reference: https://github.com/SlicerIGT/SlicerBoneReconstructionPlanner

import vtk, slicer
import numpy as np
import Lib.utils as utils

from slicer.ScriptedLoadableModule import *
from BRPLib.helperFunctions import *
from BRPLib.guiWidgets import *

#
# BoneReconstructionPlannerTestTutorial
#

class BoneReconstructionPlannerTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear()

  def runTest(self):
    """Run as few or as many tests as needed here.
    """

    self.delayDisplay("Starting the test")
    # TUTORIALMAKER BEGIN

    # TUTORIALMAKER INFO TITLE Bone Reconstruction Planner Test Tutorial
    # TUTORIALMAKER INFO AUTHOR SlicerBoneReconstructionPlanner Team
    # TUTORIALMAKER INFO DATE 27/01/2025
    # TUTORIALMAKER INFO DESC This tutorial is a comprehensive test and demonstration of the Bone Reconstruction Planner module in 3D Slicer, showcasing its functionalities through a series of scripted steps and screenshots.

    #slicer.util.mainWindow().enabled = False
    # Shot 01:
    self.setUp()
    slicer.util.selectModule("Welcome")
    # TUTORIALMAKER SCREENSHOT
    self.delayDisplay("Screenshot #1: In the Welcome screen.")
    
    # Shot 02:
    self.section_EnterBRP()
    # TUTORIALMAKER SCREENSHOT
    self.delayDisplay("Screenshot #2: Entered Bone Reconstruction Planner module.")

    # Shot 03:
    self.section_GetWidget()
    self.section_GetLogic()

    self.section_LoadSampleData()
    # TUTORIALMAKER SCREENSHOT
    self.delayDisplay("Screenshot #3: Loaded sample data.")

    # Shot 04:
    self.section_MakeModels()
    # TUTORIALMAKER SCREENSHOT
    self.delayDisplay("Screenshot #4: Made models.")

    # Shot 05:
    self.section_AddMandibularCurve()
    # TUTORIALMAKER SCREENSHOT
    self.delayDisplay("Screenshot #5: Added mandibular curve.")

    # Shot 06:
    self.section_AddMandiblePlanes()
    # TUTORIALMAKER SCREENSHOT
    self.delayDisplay("Screenshot #6: Added mandible planes.")

    # Shot 07:
    self.section_AddFibulaLineAndCenterIt()
    # TUTORIALMAKER SCREENSHOT
    self.delayDisplay("Screenshot #7: Added fibula line and centered it.")

    # Shot 08:
    self.section_SimulateAndImproveMandibleReconstruction()
    # TUTORIALMAKER SCREENSHOT
    self.delayDisplay("Screenshot #8: Simulated and improved mandible reconstruction.")

    # Shot 09:
    self.section_createMiterBoxesFromCorrespondingLine()
    # TUTORIALMAKER SCREENSHOT
    self.delayDisplay("Screenshot #9: Created miter boxes.")

    # Shot 10:
    #self.section_prepareGuideBaseForFibulaGuide()
    self.section_createAndUpdateSawBoxesFromMandiblePlanes()
    # TUTORIALMAKER SCREENSHOT
    self.delayDisplay("Screenshot #10: Created and updated saw boxes.")

    #slicer.util.mainWindow().enabled = True

    # Done
    # TUTORIALMAKER END
    self.delayDisplay('Test passed!')

  def section_EnterBRP(self):
    self.assertIsNotNone(slicer.modules.bonereconstructionplanner)
    slicer.util.selectModule('Data')
    slicer.util.selectModule('BoneReconstructionPlanner')
    self.assertEqual(slicer.util.selectedModule(),'BoneReconstructionPlanner')
  
  def section_GetWidget(self):
    self.widgetBRP = slicer.modules.bonereconstructionplanner.widgetRepresentation().self()
      
  def section_GetLogic(self):
    self.logicBRP = self.widgetBRP.logic  
      
  def test_LoadFinishedPlanSampleData(self):
    # this test should be updated with a new TestPlanBRP sample data.
    self.section_EnterBRP()
    self.section_GetWidget()
    self.section_GetLogic()

    self.delayDisplay("Started loading TestPlanBRP scene")
    import SampleData
    SampleData.downloadSample('TestPlanBRP')
    self.delayDisplay('Loaded TestPlanBRP scene')


    self.delayDisplay('Checking correct import')

    if int(slicer.app.revision) >= 31454:
      expecterNumberOfNodesByClass = {
        'vtkMRMLScalarVolumeNode': 2,
        'vtkMRMLSegmentationNode': 2,
        'vtkMRMLModelNode': 45,
        'vtkMRMLMarkupsCurveNode': 4,
        'vtkMRMLMarkupsPlaneNode': 12,
        'vtkMRMLMarkupsLineNode': 5,
        'vtkMRMLDynamicModelerNode': 4,
        'vtkMRMLMarkupsFiducialNode': 3,
        'vtkMRMLLinearTransformNode': 17
      }
    else:
      expecterNumberOfNodesByClass = {
        'vtkMRMLScalarVolumeNode': 2,
        'vtkMRMLSegmentationNode': 2,
        'vtkMRMLModelNode': 42,
        'vtkMRMLMarkupsCurveNode': 4,
        'vtkMRMLMarkupsPlaneNode': 12,
        'vtkMRMLMarkupsLineNode': 5,
        'vtkMRMLDynamicModelerNode': 4,
        'vtkMRMLMarkupsFiducialNode': 3,
        'vtkMRMLLinearTransformNode': 14
      }

    for nodeClass, expectedNumberOfNodesInScene in expecterNumberOfNodesByClass.items():
      self.assertEqual(
        slicer.mrmlScene.GetNumberOfNodesByClass(nodeClass),
        expectedNumberOfNodesInScene
      )


    # weak test to ensure integrity of the folder hierarchy, 
    #   just check if the number of leaf/one-level-below-BRPFolder items is okay
    shNode = slicer.mrmlScene.GetSubjectHierarchyNode()
    sceneItemId = shNode.GetSceneItemID()
    leafIdList = vtk.vtkIdList()
    shNode.GetItemChildren(sceneItemId,leafIdList,True)

    self.assertEqual(
      leafIdList.GetNumberOfIds(),
      110
    )

    BRPFolder = shNode.GetItemByName("BoneReconstructionPlanner")
    oneLevelBelowBRPIdList = vtk.vtkIdList()
    shNode.GetItemChildren(BRPFolder,oneLevelBelowBRPIdList,False)

    self.assertEqual(
      oneLevelBelowBRPIdList.GetNumberOfIds(),
      27
    )

    self.delayDisplay('Test data imported correctly')

  def section_LoadSampleData(self):
    # Get input data
    import SampleData
    self.fibulaVolume = SampleData.downloadSample('CTFibula')
    self.delayDisplay('Loaded CTFibula')
    self.mandibleVolume = SampleData.downloadSample('CTMandible')
    self.delayDisplay('Loaded CTMandible')
    self.fibulaSegmentation = SampleData.downloadSample('FibulaSegmentation')
    self.delayDisplay('Loaded FibulaSegmentation')
    self.mandibleSegmentation = SampleData.downloadSample('MandibleSegmentation')
    self.delayDisplay('Loaded MandibleSegmentation')

    parameterNode = self.logicBRP.getParameterNode()
    wasModified = parameterNode.StartModify()
    parameterNode.SetNodeReferenceID("currentScalarVolume", self.mandibleVolume.GetID())
    parameterNode.SetParameter("scalarVolumeChangedThroughParameterNode", "True")
    parameterNode.SetNodeReferenceID("fibulaSegmentation", self.fibulaSegmentation.GetID())
    parameterNode.SetNodeReferenceID("mandibularSegmentation", self.mandibleSegmentation.GetID())
    parameterNode.EndModify(wasModified)

    self.assertEqual(
      parameterNode.GetNodeReference("currentScalarVolume").GetID(),
      self.mandibleVolume.GetID()
    )
    self.assertEqual(
      parameterNode.GetNodeReference("fibulaSegmentation").GetID(),
      self.fibulaSegmentation.GetID()
    )
    self.assertEqual(
      parameterNode.GetNodeReference("mandibularSegmentation").GetID(),
      self.mandibleSegmentation.GetID()
    )
      
  def section_MakeModels(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """
    self.delayDisplay("Starting the MakeModelsTest")

    parameterNode = self.logicBRP.getParameterNode()

    self.logicBRP.makeModels()

    fibulaModelNode = parameterNode.GetNodeReference("fibulaModelNode")
    mandibleModelNode = parameterNode.GetNodeReference("mandibleModelNode")
    decimatedFibulaModelNode = parameterNode.GetNodeReference("decimatedFibulaModelNode")
    decimatedMandibleModelNode = parameterNode.GetNodeReference("decimatedMandibleModelNode")

    allowedDifferenceFactor = 0.02
    targetFibulaPoints = 197962
    targetMandiblePoints = 109820
    targetDecimatedFibulaPoints = 9872
    targetDecimatedMandiblePoints = 5483
    self.assertLess(
      abs(fibulaModelNode.GetMesh().GetNumberOfPoints() - targetFibulaPoints), 
      allowedDifferenceFactor*targetFibulaPoints
    )
    self.assertLess(
      abs(mandibleModelNode.GetMesh().GetNumberOfPoints()-targetMandiblePoints), 
      allowedDifferenceFactor*targetMandiblePoints
    )
    self.assertLess(
      abs(decimatedFibulaModelNode.GetMesh().GetNumberOfPoints() - targetDecimatedFibulaPoints), 
      allowedDifferenceFactor*targetDecimatedFibulaPoints
    )
    self.assertLess(
      abs(decimatedMandibleModelNode.GetMesh().GetNumberOfPoints()-targetDecimatedMandiblePoints), 
      allowedDifferenceFactor*targetDecimatedMandiblePoints
    )
    
    fibulaCentroidX = float(parameterNode.GetParameter("fibulaCentroidX"))
    fibulaCentroidY = float(parameterNode.GetParameter("fibulaCentroidY"))
    fibulaCentroidZ = float(parameterNode.GetParameter("fibulaCentroidZ"))
    mandibleCentroidX = float(parameterNode.GetParameter("mandibleCentroidX"))
    mandibleCentroidY = float(parameterNode.GetParameter("mandibleCentroidY"))
    mandibleCentroidZ = float(parameterNode.GetParameter("mandibleCentroidZ"))

    #np.testing.assert_almost_equal(actual,desired)
    np.testing.assert_almost_equal(fibulaCentroidX,-95.32889,decimal=1)
    np.testing.assert_almost_equal(fibulaCentroidY,-8.86916,decimal=1)
    np.testing.assert_almost_equal(fibulaCentroidZ,-18.44151,decimal=1)
    np.testing.assert_almost_equal(mandibleCentroidX,0.1073946,decimal=1)
    np.testing.assert_almost_equal(mandibleCentroidY,65.49171,decimal=1)
    np.testing.assert_almost_equal(mandibleCentroidZ,-57.415688,decimal=1)

    shNode = slicer.mrmlScene.GetSubjectHierarchyNode()
    BRPFolder = shNode.GetItemByName("BoneReconstructionPlanner")
    segmentationModelsFolder = shNode.GetItemByName("Segmentation Models")
    fibulaModelItemID = shNode.GetItemByDataNode(fibulaModelNode)
    mandibleModelItemID = shNode.GetItemByDataNode(mandibleModelNode)
    decimatedFibulaModelItemID = shNode.GetItemByDataNode(decimatedFibulaModelNode)
    decimatedMandibleModelItemID = shNode.GetItemByDataNode(decimatedMandibleModelNode)

    self.assertNotEqual(BRPFolder,shNode.GetInvalidItemID())
    self.assertNotEqual(segmentationModelsFolder,shNode.GetInvalidItemID())

    self.assertEqual(
      BRPFolder,
      shNode.GetItemParent(segmentationModelsFolder)
    )
    self.assertEqual(
      segmentationModelsFolder,
      shNode.GetItemParent(fibulaModelItemID)
    )
    self.assertEqual(
      segmentationModelsFolder,
      shNode.GetItemParent(mandibleModelItemID)
    )
    self.assertEqual(
      segmentationModelsFolder,
      shNode.GetItemParent(decimatedFibulaModelItemID)
    )
    self.assertEqual(
      segmentationModelsFolder,
      shNode.GetItemParent(decimatedMandibleModelItemID)
    )

    self.delayDisplay("MakeModelsTest successful")

  def section_AddMandibularCurve(self):
    self.delayDisplay("Starting the AddMandibularCurveTest")

    mandibularCurvePoints = [
      [ 43.02632904,  61.06202698, -60.92616272],
      [ 33.40823746,  83.49567413, -71.52266693],
      [ 20.23157501, 103.01984406, -78.46653748],
      [  3.63758111, 110.96538544, -82.94055939],
      [-15.31359386, 103.96769714, -83.5898056 ],
      [-31.47601509,  77.34331512, -76.59559631],
      [-44.32816696,  47.25786209, -64.23408508],
    ]

    self.logicBRP.addMandibularCurve()
    selectionNode = slicer.app.applicationLogic().GetSelectionNode()
    mandibularCurveNode = slicer.mrmlScene.GetNodeByID(
      selectionNode.GetActivePlaceNodeID()
    )
    for point in mandibularCurvePoints:
      mandibularCurveNode.AddControlPoint(*point)
    interactionNode = slicer.app.applicationLogic().GetInteractionNode()
    interactionNode.SwitchToViewTransformMode()

    self.assertEqual(
      len(mandibularCurvePoints),
      mandibularCurveNode.GetNumberOfControlPoints()
    )

    shNode = slicer.mrmlScene.GetSubjectHierarchyNode()
    BRPFolder = shNode.GetItemByName("BoneReconstructionPlanner")
    mandibularCurveItemID = shNode.GetItemByDataNode(mandibularCurveNode)
    self.assertEqual(
      BRPFolder,
      shNode.GetItemParent(mandibularCurveItemID)
    )

    #the mandibleCurveSelector autopopulates and updates the parameterNode
    parameterNode = self.logicBRP.getParameterNode()
    mandibleCurveFromParameterNode = parameterNode.GetNodeReference("mandibleCurve")
    self.assertEqual(
      mandibularCurveNode.GetID(),
      mandibleCurveFromParameterNode.GetID()
    )

    self.delayDisplay("AddMandibularCurveTest successful")
  
  def section_AddMandiblePlanes(self):
    self.delayDisplay("Starting the AddMandibularPlanesTest")

    planeOrigins = [
      [38.89806365966797, 71.97505950927734, -65.15746307373047],
      [-28.70669174194336, 81.52465057373047, -75.59122467041016],
      [21.20140266418457, 100.38216400146484, -73.75139617919922],
      [-9.514277458190918, 105.30805969238281, -79.4371337890625],
    ]

    for origin in planeOrigins:
      self.logicBRP.addCutPlane()
      selectionNode = slicer.app.applicationLogic().GetSelectionNode()
      mandibularPlaneNode = slicer.mrmlScene.GetNodeByID(
        selectionNode.GetActivePlaceNodeID()
      )
      mandibularPlaneNode.AddControlPoint(*origin)
      interactionNode = slicer.app.applicationLogic().GetInteractionNode()
      interactionNode.SwitchToViewTransformMode()
    

    shNode = slicer.mrmlScene.GetSubjectHierarchyNode()

    BRPFolder = shNode.GetItemByName("BoneReconstructionPlanner")
    mandibularPlanesFolderItemID = shNode.GetItemByName("Mandibular planes")

    self.assertEqual(
      BRPFolder,
      shNode.GetItemParent(mandibularPlanesFolderItemID)
    )

    mandibularPlanesList = createListFromFolderID(mandibularPlanesFolderItemID)
    self.assertEqual(
      len(mandibularPlanesList),
      4
    )

    colorArray = []

    for planeNode in mandibularPlanesList:
      self.assertEqual(
        planeNode.GetNumberOfControlPoints(),
        3
      )
      self.assertTrue(
        planeNode.GetAttribute("isMandibularPlane") == "True"
      )
      self.assertTrue(
        np.allclose(
          np.array(planeNode.GetSize()),
          np.array([self.logicBRP.PLANE_SIDE_SIZE,self.logicBRP.PLANE_SIDE_SIZE])
        )
      )
      self.assertEqual(
        planeNode.GetPlaneType(),
        slicer.vtkMRMLMarkupsPlaneNode.PlaneType3Points
      )
      
      displayNode = planeNode.GetDisplayNode()
      self.assertEqual(
        displayNode.GetGlyphScale(),
        self.logicBRP.PLANE_GLYPH_SCALE
      )
      self.assertTrue(
        displayNode.GetHandlesInteractive(),
      )
      self.assertTrue(
        displayNode.GetTranslationHandleVisibility(),
      )
      self.assertTrue(
        displayNode.GetRotationHandleVisibility(),
      )
      self.assertFalse(
        displayNode.GetScaleHandleVisibility(),
      )

      colorArray.append(displayNode.GetSelectedColor())
    
    colorArray = np.array(colorArray)

    # check that plane colors do not repeat
    for i in range(len(colorArray)):
      for j in range(len(colorArray)):
        if i!=j:
          self.assertFalse(
            np.allclose(
              colorArray[i],
              colorArray[j]
            )
          )
    
    # check planes order
    parameterNode = self.logicBRP.getParameterNode()
    mandibleCurve = parameterNode.GetNodeReference("mandibleCurve")
    closestCurvePoint = [0,0,0]
    smallerCurvePointIndex = 0
    for i in range(len(mandibularPlanesList)):
      origin = [0,0,0]
      mandibularPlanesList[i].GetOrigin(origin)
      curvePointIndex = mandibleCurve.GetClosestPointPositionAlongCurveWorld(
        origin,closestCurvePoint
      )
      self.assertLessEqual(smallerCurvePointIndex, curvePointIndex)
      if smallerCurvePointIndex <= curvePointIndex:
        smallerCurvePointIndex = curvePointIndex

    self.delayDisplay("AddMandibularPlanesTest successful")

  def section_AddFibulaLineAndCenterIt(self):
    self.delayDisplay("Starting the AddFibulaLineAndCenterItTest")

    fibulaLinePoints = [
      [-91.39446258544922, -12.100865364074707, -90.508544921875],
      [-104.19928741455078, -9.48827075958252, 47.4937744140625],
    ]

    self.logicBRP.addFibulaLine()
    selectionNode = slicer.app.applicationLogic().GetSelectionNode()
    fibulaLineNode = slicer.mrmlScene.GetNodeByID(
      selectionNode.GetActivePlaceNodeID()
    )
    for point in fibulaLinePoints:
      fibulaLineNode.AddControlPoint(*point)
    interactionNode = slicer.app.applicationLogic().GetInteractionNode()
    interactionNode.SwitchToViewTransformMode()

    self.assertEqual(
      len(fibulaLinePoints),
      fibulaLineNode.GetNumberOfControlPoints()
    )

    shNode = slicer.mrmlScene.GetSubjectHierarchyNode()
    BRPFolder = shNode.GetItemByName("BoneReconstructionPlanner")
    fibulaLineItemID = shNode.GetItemByDataNode(fibulaLineNode)
    self.assertEqual(
      BRPFolder,
      shNode.GetItemParent(fibulaLineItemID)
    )

    #the fibulaLineSelector autopopulates and updates the parameterNode
    parameterNode = self.logicBRP.getParameterNode()
    fibulaLineFromParameterNode = parameterNode.GetNodeReference("fibulaLine")
    self.assertEqual(
      fibulaLineNode.GetID(),
      fibulaLineFromParameterNode.GetID()
    )

    self.logicBRP.centerFibulaLine()

    centeredLinePoints = np.array(
      [
        [ -88.32122039794922, -10.915949821472168, -90.24563598632812],
        [-100.49141693115234, -9.320514678955078, 47.834014892578125]
      ]
    )

    for i in range(2):
      self.assertTrue(
        np.allclose(
          fibulaLineNode.GetNthControlPointPosition(i),
          centeredLinePoints[i],
          atol=1e-2
        )
      )

    self.delayDisplay("AddFibulaLineAndCenterItTest successful")

  def section_SimulateAndImproveMandibleReconstruction(self):
    self.delayDisplay("Starting the SimulateAndImproveMandibleReconstruction")
    self.delayDisplay("Create the reconstruction for first time")
    self.logicBRP.onGenerateFibulaPlanesTimerTimeout()
    self.delayDisplay("Reconstruction successful")
    #

    # # generate mandibular plane movements with this code:
    # def createListFromFolderID(folderID):
    #   createdList = []
    #   shNode = slicer.mrmlScene.GetSubjectHierarchyNode()
    #   myList = vtk.vtkIdList()
    #   shNode.GetItemChildren(folderID,myList)
    #   for i in range(myList.GetNumberOfIds()):
    #     createdList.append(shNode.GetItemDataNode(myList.GetId(i)))
    #   return createdList
    # def updateMandibularPlaneMovementsList(caller=None,event=None,movementsList=[]):
    #   plane = caller
    #   planeMatrix = vtk.vtkMatrix4x4()
    #   plane.GetObjectToWorldMatrix(planeMatrix)
    #   movementsList.append([plane.GetID(),slicer.util.arrayFromVTKMatrix(planeMatrix).tolist()])
    # shNode = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)
    # mandiblePlanesFolder = shNode.GetItemByName("Mandibular planes")
    # mandiblePlanes = createListFromFolderID(mandiblePlanesFolder)
    # # list to save the movements for the test
    # movementsList = []
    # # set observers
    # planesAndObserversList = []
    # for plane in mandiblePlanes:
    #   planesAndObserversList.append(
    #     [
    #         plane.GetID(),
    #         plane.AddObserver(
    #             slicer.vtkMRMLMarkupsNode.PointEndInteractionEvent,
    #             lambda caller,event,movementsList=movementsList: updateMandibularPlaneMovementsList(caller,event,movementsList)
    #         )
    #     ]
    #  )
    # 
    # 

    if not slicer.app.commandOptions().noMainWindow:
      layoutManager = slicer.app.layoutManager()
      mandibleViewNode = slicer.mrmlScene.GetSingletonNode(slicer.MANDIBLE_VIEW_SINGLETON_TAG, "vtkMRMLViewNode")
      if int(slicer.app.revision) >= 31524:
        layoutManager.addMaximizedViewNode(mandibleViewNode)
      else:
        layoutManager.setMaximizedViewNode(mandibleViewNode)

    # 8 movements below
    # movementsList = [['vtkMRMLMarkupsPlaneNode4', [[0.5161781920883237, -0.04134258142560255, -0.8554828256449669, -9.862711906433127], [-0.8468593163756161, 0.12466280634486007, -0.5169994999823967, 107.90783691406249], [0.12802098374975024, 0.991337468108258, 0.02933687175645767, -83.94944763183594], [0.0, 0.0, 0.0, 1.0]]], ['vtkMRMLMarkupsPlaneNode4', [[0.516178231664674, -0.041342429710410605, -0.8554828090973949, -7.397708892822266], [-0.8468592958433797, 0.12466287181842768, -0.5169995178272775, 103.8636703491211], [0.12802095999946736, 0.9913374662019095, 0.029337039816463184, -83.33809661865234], [0.0, 0.0, 0.0, 1.0]]], ['vtkMRMLMarkupsPlaneNode2', [[0.8922376682835299, 0.18524939419545736, -0.41181865577725557, -28.11571121215824], [-0.4465787117400004, 0.22681900255851603, -0.8655175297467994, 84.53712463378889], [-0.06692830131275733, 0.9561567873673105, 0.2851048937756292, -79.05013275146474], [0.0, 0.0, 0.0, 1.0]]], ['vtkMRMLMarkupsPlaneNode2', [[0.8922376766572847, 0.1852491791773996, -0.41181873435688954, -24.693025588989258], [-0.4465787239770117, 0.22681897690359318, -0.8655175301560744, 82.82402038574219], [-0.06692810802850067, 0.9561568351115349, 0.2851047790290762, -79.30686950683594], [0.0, 0.0, 0.0, 1.0]]], ['vtkMRMLMarkupsPlaneNode3', [[-0.708383352772158, -0.24065112649761564, -0.6635360282838488, 22.992961883544925], [-0.6972025285352179, 0.09205350357255149, 0.7109393692039546, 100.19924163818364], [-0.11000754392029201, 0.9662366106681359, -0.23299174338413398, -77.51470947265622], [0.0, 0.0, 0.0, 1.0]]], ['vtkMRMLMarkupsPlaneNode3', [[-0.7083834009232749, -0.240651176447713, -0.6635359587623766, 20.943126678466797], [-0.6972024658214877, 0.09205345939667467, 0.7109394364258759, 98.18177032470703], [-0.11000763132079507, 0.9662366024361924, -0.23299173625635644, -77.8330307006836], [0.0, 0.0, 0.0, 1.0]]], ['vtkMRMLMarkupsPlaneNode1', [[-0.8984010895060554, -0.2612400933848085, -0.35302846341708666, 39.90895843505858], [-0.42656108809295407, 0.32777755218344756, 0.8429753937153698, 68.75823974609365], [-0.1045041649853625, 0.9079182176236601, -0.4059105684849661, -64.72950744628893], [0.0, 0.0, 0.0, 1.0]]], ['vtkMRMLMarkupsPlaneNode1', [[-0.8984010923061703, -0.2612399980002971, -0.3530285268754991, 36.00282287597656], [-0.4265610935556299, 0.32777742996859105, 0.8429754384724448, 66.90361022949219], [-0.10450411861599232, 0.9079182891912633, -0.4059104203445687, -65.18387603759766], [0.0, 0.0, 0.0, 1.0]]]]
    # 4 movements below
    movementsList = [['vtkMRMLMarkupsPlaneNode4', [[0.516178231664674, -0.041342429710410605, -0.8554828090973949, -7.397708892822266], [-0.8468592958433797, 0.12466287181842768, -0.5169995178272775, 103.8636703491211], [0.12802095999946736, 0.9913374662019095, 0.029337039816463184, -83.33809661865234], [0.0, 0.0, 0.0, 1.0]]], ['vtkMRMLMarkupsPlaneNode2', [[0.8922376766572847, 0.1852491791773996, -0.41181873435688954, -24.693025588989258], [-0.4465787239770117, 0.22681897690359318, -0.8655175301560744, 82.82402038574219], [-0.06692810802850067, 0.9561568351115349, 0.2851047790290762, -79.30686950683594], [0.0, 0.0, 0.0, 1.0]]], ['vtkMRMLMarkupsPlaneNode3', [[-0.7083834009232749, -0.240651176447713, -0.6635359587623766, 20.943126678466797], [-0.6972024658214877, 0.09205345939667467, 0.7109394364258759, 98.18177032470703], [-0.11000763132079507, 0.9662366024361924, -0.23299173625635644, -77.8330307006836], [0.0, 0.0, 0.0, 1.0]]], ['vtkMRMLMarkupsPlaneNode1', [[-0.8984010923061703, -0.2612399980002971, -0.3530285268754991, 36.00282287597656], [-0.4265610935556299, 0.32777742996859105, 0.8429754384724448, 66.90361022949219], [-0.10450411861599232, 0.9079182891912633, -0.4059104203445687, -65.18387603759766], [0.0, 0.0, 0.0, 1.0]]]]
    for item in movementsList:
      self.delayDisplay("Update mandibular plane and reconstruction")
      self.delayDisplay("Move mandibular plane")
      nodeID = item[0]
      newPlaneToWorldMatrix = slicer.util.vtkMatrixFromArray(np.array(item[1]))
      planeNode = slicer.mrmlScene.GetNodeByID(nodeID)
      oldPlaneToWorld = vtk.vtkMatrix4x4()
      planeNode.GetObjectToWorldMatrix(oldPlaneToWorld)
      worldToOldPlane = vtk.vtkMatrix4x4()
      vtk.vtkMatrix4x4.Invert(oldPlaneToWorld, worldToOldPlane)
      transform = vtk.vtkTransform()
      transform.PostMultiply()
      transform.Concatenate(worldToOldPlane)
      transform.Concatenate(newPlaneToWorldMatrix)
      wasModified = planeNode.StartModify()
      for i in range(3):
        oldPos = planeNode.GetNthControlPointPosition(i)
        newPos = [0,0,0]
        transform.TransformPoint(oldPos,newPos)
        planeNode.SetNthControlPointPosition(i,newPos)
      planeNode.EndModify(wasModified)
      self.delayDisplay("Mandibular plane moved")
      #
      self.delayDisplay("Update reconstruction")
      self.logicBRP.onGenerateFibulaPlanesTimerTimeout()
      self.delayDisplay("Update successful")
    
    if not slicer.app.commandOptions().noMainWindow:
      # hide original mandible
      self.widgetBRP.setOriginalMandibleVisility(False)
      # hide mandible plane handles
      self.widgetBRP.setMandiblePlanesInteractionHandlesVisibility(False)
    
    self.delayDisplay("Optimize bones contact in reconstruction")
    parameterNode = self.logicBRP.getParameterNode()
    parameterNode.SetParameter("mandiblePlanesPositioningForMaximumBoneContact","True")
    self.logicBRP.onGenerateFibulaPlanesTimerTimeout()
    self.delayDisplay("Bones contact optimized")

    if not slicer.app.commandOptions().noMainWindow:
      fibulaViewNode = slicer.mrmlScene.GetSingletonNode(slicer.FIBULA_VIEW_SINGLETON_TAG, "vtkMRMLViewNode")
      layoutManager = slicer.app.layoutManager()
      if int(slicer.app.revision) >= 31524:
        layoutManager.removeMaximizedViewNode(mandibleViewNode)
        layoutManager.addMaximizedViewNode(fibulaViewNode)
      else:
        layoutManager.setMaximizedViewNode(None)
        layoutManager.setMaximizedViewNode(fibulaViewNode)

    # solve rotation about the anatomical axis of the grafted bone-pieces
    self.delayDisplay("Make between-bone-pieces relative rotation zero")
    parameterNode = self.logicBRP.getParameterNode()
    parameterNode.SetParameter("makeAllMandiblePlanesRotateTogether","True")
    self.logicBRP.onGenerateFibulaPlanesTimerTimeout()
    self.delayDisplay("Achieved zero relative rotation")

    if not slicer.app.commandOptions().noMainWindow:
      layoutManager = slicer.app.layoutManager()
      if int(slicer.app.revision) >= 31524:
        layoutManager.removeMaximizedViewNode(fibulaViewNode)
      else:
        layoutManager.setMaximizedViewNode(None)

    self.delayDisplay("SimulateAndImproveMandibleReconstruction test successful")
    
  def section_createMiterBoxesFromCorrespondingLine(self):
    self.delayDisplay("Starting the createMiterBoxesFromCorrespondingLine test")

    parameterNode = self.logicBRP.getParameterNode()
    wasModified = parameterNode.StartModify()
    parameterNode.SetNodeReferenceID("currentScalarVolume", self.fibulaVolume.GetID())
    parameterNode.SetParameter("scalarVolumeChangedThroughParameterNode", "True")
    parameterNode.EndModify(wasModified)

    sliceOffset = -38.08869552612305
    if not slicer.app.commandOptions().noMainWindow:
      redSliceNode = slicer.mrmlScene.GetSingletonNode("Red", "vtkMRMLSliceNode")
      redSliceNode.SetSliceOffset(sliceOffset)

    miterBoxLinePoints = [
      [-92.47185918150018, -10.999045106771323, sliceOffset],
      [-104.08360013902106, -12.657865243560021, sliceOffset],
    ]
    
    miterBoxLine = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode", "miterBoxLine")
    miterBoxLine.CreateDefaultDisplayNodes()
    
    for point in miterBoxLinePoints:
      miterBoxLine.AddControlPoint(*point)

    self.assertEqual(
      len(miterBoxLinePoints),
      miterBoxLine.GetNumberOfControlPoints()
    )

    wasModified = parameterNode.StartModify()
    parameterNode.SetParameter("checkSecurityMarginOnMiterBoxCreation","False")
    parameterNode.SetNodeReferenceID("miterBoxDirectionLine",miterBoxLine.GetID())
    parameterNode.EndModify(wasModified)
    self.logicBRP.createMiterBoxesFromFibulaPlanes()

    # asserts below

    self.delayDisplay("CreateMiterBoxesFromCorrespondingLine test successful")

  def loadFibulaGuideBase(self):
    import SampleData
    self.fibulaSurgicalGuideBaseModel = SampleData.downloadSample('FibulaGuideBase')
    self.delayDisplay('Loaded FibulaGuideBase')

    parameterNode = self.logicBRP.getParameterNode()
    parameterNode.SetNodeReferenceID("fibulaSurgicalGuideBaseModel", self.fibulaSurgicalGuideBaseModel.GetID())

    self.assertEqual(
      parameterNode.GetNodeReference("fibulaSurgicalGuideBaseModel").GetID(),
      self.fibulaSurgicalGuideBaseModel.GetID()
    )
  
  def section_prepareGuideBaseForFibulaGuide(self):
    self.loadFibulaGuideBase()

  def section_createAndUpdateSawBoxesFromMandiblePlanes(self):
    self.delayDisplay("Starting the createAndUpdateSawBoxesFromMandiblePlanes test")

    if not slicer.app.commandOptions().noMainWindow:
      layoutManager = slicer.app.layoutManager()
      mandibleViewNode = slicer.mrmlScene.GetSingletonNode(slicer.MANDIBLE_VIEW_SINGLETON_TAG, "vtkMRMLViewNode")
      if int(slicer.app.revision) >= 31524:
        layoutManager.addMaximizedViewNode(mandibleViewNode)
      else:
        layoutManager.setMaximizedViewNode(mandibleViewNode)

    self.logicBRP.createSawBoxesFromFirstAndLastMandiblePlanes()

    # # generate saw boxes movements with this code:
    # def createListFromFolderID(folderID):
    #   createdList = []
    #   shNode = slicer.mrmlScene.GetSubjectHierarchyNode()
    #   myList = vtk.vtkIdList()
    #   shNode.GetItemChildren(folderID,myList)
    #   for i in range(myList.GetNumberOfIds()):
    #     createdList.append(shNode.GetItemDataNode(myList.GetId(i)))
    #   return createdList
    # def updateSawBoxesMovementsList(caller=None,event=None,movementsList=[]):
    #   plane = caller
    #   planeMatrix = vtk.vtkMatrix4x4()
    #   plane.GetObjectToWorldMatrix(planeMatrix)
    #   movementsList.append([plane.GetID(),slicer.util.arrayFromVTKMatrix(planeMatrix).tolist()])
    # shNode = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)
    # sawBoxesPlanesFolder = shNode.GetItemByName("sawBoxes Planes")
    # sawBoxesPlanes = createListFromFolderID(mandiblePlanesFolder)
    # # list to save the movements for the test
    # movementsList = []
    # # set observers
    # planesAndObserversList = []
    # for plane in sawBoxesPlanes:
    #   planesAndObserversList.append(
    #     [
    #         plane.GetID(),
    #         plane.AddObserver(
    #             slicer.vtkMRMLMarkupsNode.PointEndInteractionEvent,
    #             lambda caller,event,movementsList=movementsList: updateSawBoxesMovementsList(caller,event,movementsList)
    #         )
    #     ]
    #  )
    # 
    # 

    movementsList = [['vtkMRMLMarkupsPlaneNode11', [[-0.10858201072394683, 0.9292904853485047, -0.3530285268754998, 42.21461987204822], [0.39399905998699103, 0.3662746931765254, 0.8429754384724443, 76.13834598713792], [0.9126744697188107, -0.04756093963730036, -0.40591042034456926, -52.639932827421404], [0.0, 0.0, 0.0, 1.0]]], ['vtkMRMLMarkupsPlaneNode11', [[-0.10858201072394683, 0.9292904853485047, -0.3530285268754998, 43.024681091308594], [0.39399905998699103, 0.3662746931765254, 0.8429754384724443, 73.1989517211914], [0.9126744697188107, -0.04756093963730036, -0.40591042034456926, -59.4488639831543], [0.0, 0.0, 0.0, 1.0]]], ['vtkMRMLMarkupsPlaneNode11', [[-0.10858201072394683, 0.9292904853485047, -0.3530285268754998, 47.28470993041992], [0.39399905998699103, 0.3662746931765254, 0.8429754384724443, 74.87801361083984], [0.9126744697188107, -0.04756093963730036, -0.40591042034456926, -59.66689682006836], [0.0, 0.0, 0.0, 1.0]]], ['vtkMRMLMarkupsPlaneNode12', [[0.1458282507662034, -0.8995217903481598, -0.4118187343568899, -35.072343539111024], [0.24624056084596485, 0.4361708279869181, -0.8655175301560744, 90.12325764191597], [0.9581751966486786, 0.024810431315229024, 0.28510477902907616, -73.89405603129094], [0.0, 0.0, 0.0, 1.0]]]]

    for item in movementsList:
      self.delayDisplay("Move saw box")
      nodeID = item[0]
      newPlaneToWorldMatrix = slicer.util.vtkMatrixFromArray(np.array(item[1]))
      planeNode = slicer.mrmlScene.GetNodeByID(nodeID)
      oldPlaneToWorld = vtk.vtkMatrix4x4()
      planeNode.GetObjectToNodeMatrix(oldPlaneToWorld)
      worldToOldPlane = vtk.vtkMatrix4x4()
      vtk.vtkMatrix4x4.Invert(oldPlaneToWorld, worldToOldPlane)
      transform = vtk.vtkTransform()
      transform.PostMultiply()
      transform.Concatenate(worldToOldPlane)
      transform.Concatenate(newPlaneToWorldMatrix)
      wasModified = planeNode.StartModify()
      for i in range(3):
        oldPos = planeNode.GetNthControlPointPosition(i)
        newPos = [0,0,0]
        transform.TransformPoint(oldPos,newPos)
        planeNode.SetNthControlPointPosition(i,newPos)
      planeNode.EndModify(wasModified)
      self.delayDisplay("Saw box moved")

    if not slicer.app.commandOptions().noMainWindow:
      layoutManager = slicer.app.layoutManager()
      if int(slicer.app.revision) >= 31524:
        layoutManager.removeMaximizedViewNode(mandibleViewNode)
      else:
        layoutManager.setMaximizedViewNode(None)
      # show mandible plane handles
      self.widgetBRP.setMandiblePlanesInteractionHandlesVisibility(True)
      # hide saw boxes handles
      self.widgetBRP.setBiggerSawBoxesInteractionHandlesVisibility(False)

    # asserts below


    self.delayDisplay("CreateAndUpdateSawBoxesFromMandiblePlanes test successful")

def createListFromFolderID(folderID):
  shNode = slicer.mrmlScene.GetSubjectHierarchyNode()
  createdList = []

  if folderID != shNode.GetInvalidItemID():
    myList = vtk.vtkIdList()
    shNode.GetItemChildren(folderID,myList)
    for i in range(myList.GetNumberOfIds()):
      createdList.append(shNode.GetItemDataNode(myList.GetId(i)))
  
  return createdList

def setFolderItemVisibility(folderItemID, visibility):
  pluginHandler = slicer.qSlicerSubjectHierarchyPluginHandler().instance()
  folderPlugin = pluginHandler.pluginByName("Folder")
  folderPlugin.setDisplayVisibility(folderItemID, visibility)