# Reference Tutorial: https://www.youtube.com/watch?v=g9Vql5h6uHM
import os
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
        self.runPart01_InstallingExtention()
        self.runPart02_LoadingData()
        self.runPart03_BasicSegmentationFibulaMandible()

        # Done
        self.Tutorial.endTutorial()
        self.delayDisplay("Test passed!")
    
    def runPart01_InstallingExtention(self):
        # 1 shot: 
        self.mainWindow.moduleSelector().selectModule('Welcome')
        self.layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalView)
        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #1: In the Welcome screen.')

        # TODO: Screenshot is not properly taken in the extension manager environment

        # 2 shot:
        #extension_button = self.util.getNamedWidget("DialogToolBar/QToolButton:0").inner()
        #extension_button.click()
        #self.Tutorial.nextScreenshot()


        # TODO: Search and install "BoneReconstructionPlanner" and "SegmentEditorExtraEffects" extensions
    
    def runPart02_LoadingData(self):
        # 1 shot: 
        self.mainWindow.moduleSelector().selectModule('Welcome')
        self.layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalView)
        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #1: In the Welcome screen.')

        # 2 shot:
        self._load_url_content("https://github.com/SlicerIGT/SlicerBoneReconstructionPlanner/releases/download/TestingData/CTFibula.nrrd", "CTFibula.nrrd")
        self._load_url_content("https://github.com/SlicerIGT/SlicerBoneReconstructionPlanner/releases/download/TestingData/CTMandible.nrrd", "CTMandible.nrrd")


        self.Tutorial.nextScreenshot()
        self.delayDisplay("Screenshot #2: Loaded the sample dataset.")
    
    def runPart03_BasicSegmentationFibulaMandible(self):
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

        lower_threshold = 890
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

        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #5: Showing 3d model.')

        # 6 shot:
        segment_editor_widget = slicer.modules.segmenteditor.widgetRepresentation().self()
        segment_editor_widget.editor.setActiveEffectByName("Islands")

        self.Tutorial.nextScreenshot()
        self.delayDisplay('Screenshot #6: In the Islands options.')


    
    def runPart04_VirtualSurgicalPlanning(self):
        pass
    
    def runPart05_FibulaCuttingGuideGeneration(self):
        pass

    def runPart06_MandibularResectionGuideGeneration(self):
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

    
