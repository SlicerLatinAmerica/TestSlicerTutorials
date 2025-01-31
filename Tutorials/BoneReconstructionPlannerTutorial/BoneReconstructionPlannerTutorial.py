# Reference Tutorial: https://www.youtube.com/watch?v=g9Vql5h6uHM
import os
import vtk
import time
import slicer
import zipfile
import SampleData
import urllib.request

import Lib.utils as utils

from slicer.ScriptedLoadableModule import *

# BoneReconstructionPlannerTutorial


class BoneReconstructionPlannerTutorialTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """Do whatever is needed to reset the state - typically a scene clear will be enough."""
        slicer.mrmlScene.Clear(0)

    def runTest(self):
        """Run as few or as many tests as needed here."""
        self.setUp()
        self.test_BoneReconstructionPlannerTutorial1()

    def test_BoneReconstructionPlannerTutorial1(self):
        """Tests parts of the BoneReconstructionPlannerTutorial."""
        self.Tutorial = utils.Tutorial(
            "Slicer	Visualization Tutorial",
            "Author",
            "27/01/2025",
            "description",
        )

        self.util = utils.util()
        self.layoutManager = slicer.app.layoutManager()
        self.mainWindow = slicer.util.mainWindow()

        # Clear Output folder
        self.Tutorial.clearTutorial()
        self.Tutorial.beginTutorial()
        self.delayDisplay("Starting the test")

        # Running Tutorial
        self.runPart01_LoadingData()
        self.runPart02_BasicSegmentationFibulaMandible()
        self.runPart03_VirtualSurgicalPlanning()

        # Done
        self.Tutorial.endTutorial()
        self.delayDisplay("Test passed!")
    
    
    def runPart01_LoadingData(self):
        # 1 shot: 
        self.mainWindow.moduleSelector().selectModule('Welcome')
        self.layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalView)
        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #1: In the Welcome screen.')

        # 2 shot:
        self._load_url_content("https://github.com/SlicerIGT/SlicerBoneReconstructionPlanner/releases/download/TestingData/CTMandible.nrrd", "CTMandible.nrrd")
        self._load_url_content("https://github.com/SlicerIGT/SlicerBoneReconstructionPlanner/releases/download/TestingData/CTFibula.nrrd", "CTFibula.nrrd")

        self.Tutorial.nextScreenshot()
        self.delayDisplay("Screenshot #2: Loaded the sample dataset.")
    
    def runPart02_BasicSegmentationFibulaMandible(self):
        # 1 shot: 
        self.mainWindow.moduleSelector().selectModule('SegmentEditor')
        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #1: In the Segment Editor screen.')

        # 2 shot:
        add_segment_button = self.util.getNamedWidget("PanelDockWidget/dockWidgetContents/ModulePanel/ScrollArea/qt_scrollarea_viewport/scrollAreaWidgetContents/SegmentEditorModuleWidget/qMRMLSegmentEditorWidget/AddSegmentButton").inner()
        add_segment_button.click()
        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #2: Add segment.')

        # 3 shot:
        threshold_button = self.util.getNamedWidget("PanelDockWidget/dockWidgetContents/ModulePanel/ScrollArea/qt_scrollarea_viewport/scrollAreaWidgetContents/SegmentEditorModuleWidget/qMRMLSegmentEditorWidget/EffectsGroupBox/Threshold").inner()
        threshold_button.click()
        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #3: In the Threshold menu.')

        # 4 shot
        segment_editor_widget = slicer.modules.segmenteditor.widgetRepresentation().self()

        segment_editor_widget.editor.setActiveEffectByName("Threshold")

        threshold_effect = segment_editor_widget.editor.activeEffect()

        lower_threshold = 200
        threshold_effect.setParameter("MinimumThreshold", str(lower_threshold))

        apply_button = self.util.getNamedWidget("PanelDockWidget/dockWidgetContents/ModulePanel/ScrollArea/qt_scrollarea_viewport/scrollAreaWidgetContents/SegmentEditorModuleWidget/qMRMLSegmentEditorWidget/OptionsGroupBox/EffectsOptionsFrame/QFrame:13/SegmentEditorThresholdEffectApply")
        apply_button.click()

        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #4: Changing threshold range.')

        # 5 shot:
        segmentation_node = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLSegmentationNode")

        segmentation_node.CreateClosedSurfaceRepresentation()

        segmentation_display_node = segmentation_node.GetDisplayNode()

        segmentation_display_node.SetVisibility(True)
        segmentation_display_node.SetVisibility2DFill(True)

        time.sleep(0.5) #Necessary to wait 3d model to be loaded

        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #5: Showing 3d model.')

        # 6 shot:
        cam = slicer.util.getNode(pattern="vtkMRMLCameraNode1")
        cam.GetCamera().Roll(90)
        cam.GetCamera().Elevation(30)

        self.Tutorial.nextScreenshot()
        self.delayDisplay("Screenshot #6: Rotated view.")

        # 7 shot:
        segment_editor_widget = slicer.modules.segmenteditor.widgetRepresentation().self()
        segment_editor_widget.editor.setActiveEffectByName("Islands")

        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #7: In the Islands options.')

        # 8 shot:
        keep_islands_button = self.util.getNamedWidget("PanelDockWidget/dockWidgetContents/ModulePanel/ScrollArea/qt_scrollarea_viewport/scrollAreaWidgetContents/SegmentEditorModuleWidget/qMRMLSegmentEditorWidget/OptionsGroupBox/EffectsOptionsFrame/QFrame:7/QRadioButton:3")
        keep_islands_button.click()

        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #8: Mark \"Keep Selected Islands\" option.')

        # 9 shot:
        #self._simulate_axial_click(97, 12, 7)
        #self.Tutorial.nextScreenshot()
        #self.delayDisplay('Screenshot #8: Select island to be kept.')
    
    def runPart03_VirtualSurgicalPlanning(self):
        # 1 shot:
        self.mainWindow.moduleSelector().selectModule('BoneReconstructionPlanner')
        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #1: In the Bone Reconstruction Planne screen.')

    def runPart04_FibulaCuttingGuideGeneration(self):
        pass

    def runPart05_MandibularResectionGuideGeneration(self):
        pass
    
    def _load_url_content(self, file_url, file_name):
        download_dir = slicer.app.temporaryPath
        file_path = os.path.join(download_dir, file_name)

        print(f"Downloading {file_url} to {file_path}...")
        urllib.request.urlretrieve(file_url, file_path)
        print("Download complete.")

        print(f"Loading {file_path} into 3D Slicer...")
        slicer.util.loadVolume(file_path)
        print("File loaded successfully.")

    def _simulate_axial_click(self, x, y, z):
        red_slice_node = slicer.util.getNode('vtkMRMLSliceNodeRed')

        if not red_slice_node:
            print("Error: Could not find Red (Axial) slice node.")
            return


        slice_logic = slicer.app.applicationLogic().GetSliceLogic(red_slice_node)

        if not slice_logic:
            print("Error: Could not get slice logic for the Red slice.")
            return


        ras_to_ijk_matrix = vtk.vtkMatrix4x4()
        slice_logic.GetSliceNode().GetRASToIJKMatrix(ras_to_ijk_matrix)

        ijk = [0, 0, 0, 1]
        ijk[0] = x
        ijk[1] = y
        ijk[2] = z

        ijk_coords = [0, 0, 0]
        ras_to_ijk_matrix.MultiplyPoint(ijk, ijk_coords)

        layout_manager = slicer.app.layoutManager()
        red_view_id = layout_manager.sliceViewNames().index('Red') 
        red_view = layout_manager.sliceWidget(red_view_id).sliceView()

        display_coords = red_view.convertIJKToDisplay(ijk_coords)

        event = vtk.vtkGenericMouseEvent()
        event.SetEventType(vtk.vtkCommand.LeftButtonPressEvent)
        event.SetButton(1)
        event.SetX(display_coords[0])
        event.SetY(display_coords[1])

        interactor = red_view.interactor()
        interactor.ProcessEvent(event)

        release_event = vtk.vtkGenericMouseEvent()
        release_event.SetEventType(vtk.vtkCommand.LeftButtonReleaseEvent)
        release_event.SetButton(1)
        release_event.SetX(display_coords[0])
        release_event.SetY(display_coords[1])
        interactor.ProcessEvent(release_event)