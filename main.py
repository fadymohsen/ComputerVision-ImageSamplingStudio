import sys
from PyQt5.QtWidgets import QApplication, QTabWidget, QFileDialog
from PyQt5 import uic
import cv2
import pyqtgraph as pg
import numpy as np

# Features
from NoiseFilter import noiseAdditionFiltration
from EdgeDetection import EdgeDetector
from Thresholding import Thresholding 
from curves import Curves
from normalizeAndEqualize import ImageProcessor
from frequency_domain_filters import FrequencyDomainFilters





# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------





class MyTabWidget(QTabWidget):
    def __init__(self, ui_file):
        super().__init__()
        uic.loadUi(ui_file, self)
        self.image_edges = pg.GraphicsLayoutWidget()
        self.selected_image_path = None
        self.pushButton_browseImage.clicked.connect(self.browse_image)

        # Import Features Classes
        self.noiseAddFilterAdd = noiseAdditionFiltration(self)
        self.addDetectionAdd = EdgeDetector(self)
        self.addThresholdingAdd = Thresholding(self)
        self.addCurvesAdd = Curves(self)
        self.addEqualizeNormalize = ImageProcessor(self)
        self.frequency_domain_filters = FrequencyDomainFilters(self)  
        


        # START - To be Edited
        """
        import RGBHistogram
        from frequency_domain_filters import ideal_filter, butterworth_filter, gaussian_filter, hyprid_images
        self.vb = None
        self.image_mixed = False
        self.img_data_low_pass = None
        self.img_data_high_pass  = None
        self.counter = 0
        """
        # END - To be Edited
        

# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------

    def browse_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "",
                                                "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.webp)",
                                                options=options)
        if file_name:
            self.selected_image_path = file_name
            self.display_image_on_graphics_layout(file_name)
            # Apply in Noise/Filtering
            self.noiseAddFilterAdd.applyNoise()
            # Apply in EdgeDetection
            self.addDetectionAdd.detectEdges()
            # Apply in curves
            self.addCurvesAdd.drawCurves()
            # Apply in Normalization & Equalization
            self.addEqualizeNormalize.imageProcessing()
            # Apply in frequency domain filters
            self.frequency_domain_filters.apply_frequency_domain_filters()


# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------

    def display_image_on_graphics_layout(self, image_path):
        image_data = cv2.imread(image_path)
        image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
        image_data = np.rot90(image_data, -1)
        # Clear the previous image if any
        self.graphicsLayoutWidget_displayImagesMain.clear()
        # Create a PlotItem or ViewBox
        view_box = self.graphicsLayoutWidget_displayImagesMain.addViewBox()
        # Create an ImageItem and add it to the ViewBox
        image_item = pg.ImageItem(image_data)
        view_box.addItem(image_item)
        # Optional: Adjust the view to fit the image
        view_box.autoRange()

# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------

    def keyPressEvent(self, event):
        if event.key() == 16777216:         # Integer value for Qt.Key_Escape
            if self.isFullScreen():
                self.showNormal()           # Show in normal mode
            else:
                self.showFullScreen()       # Show in full screen
        else:
            super().keyPressEvent(event)
    
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------


""" 
    def handleObjects(self):
        self.btn_chooseImageCurves_2.clicked.connect(self.open_image)
        #self.btn_chooseImageNoise_2.clicked.connect(lambda: self.noiseAdd.Browse())
        self.slider_adjustFrequency.valueChanged.connect(self.updateFrequencyValue)
        self.slider_adjustTValue.valueChanged.connect(self.updateTValue)
        self.radioButton_highPass.clicked.connect(
            lambda: self.freq_domain_filters(self.radioButton_lowPass.isChecked()))
        self.radioButton_lowPass.clicked.connect(
            lambda: self.freq_domain_filters(self.radioButton_lowPass.isChecked()))
        self.comboBox_filterType.currentTextChanged.connect(
            lambda: self.freq_domain_filters(self.radioButton_lowPass.isChecked()
                                             , self.comboBox_filterType.currentText()))
        self.btn_addFirstImage.clicked.connect(self.toggle_data)
        self.btn_addSecondImage.clicked.connect(self.toggle_data)
        self.btn_addFirstImage.clicked.connect(
            lambda: self.freq_domain_filters(True,
                                             self.comboBox_filterType.currentText()))
        self.btn_addSecondImage.clicked.connect(lambda:self.freq_domain_filters(False,
                                                                                self.comboBox_filterType.currentText()))

        self.btn_applyHybrid.clicked.connect(lambda:self.mix_images(self.img_data_low_pass,self.img_data_high_pass))
        self.comboBox_edgeMaskType.currentIndexChanged.connect(self.on_edgeMaskType_change)
        self.comboBox_edgeMaskDirection.currentIndexChanged.connect(self.on_edgeMaskDirection_change)
        self.slider_adjustTValue.setRange(0, 255)  
        self.slider_adjustTValue.setValue(127)  
        self.slider_adjustTValue.valueChanged.connect(self.updateThreshold)
        
        self.radioButton_normalHistogram.toggled.connect(lambda:self.drawHistograms(self.imageEdgeDetection))
        self.radioButton_cumulative.toggled.connect(lambda:self.drawHistograms(self.imageEdgeDetection))
        

    def updateFrequencyValue(self, value):
        self.label_frequencyValue.setText('Cut-off Frequency: {} Hz'.format(value))
        self.freq_domain_filters(self.radioButton_lowPass.isChecked()
                                 , self.comboBox_filterType.currentText())

    def updateTValue(self, value):
        self.label_valueOfT.setText('T-Value: {}'.format(value))

    def toggle_data(self):
        self.image_mixed = True
        self.open_image()


def open_image(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image", "",
                                                  "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.webp)",
                                                  options=options)
        self.imageEdgeDetection = cv2.imread(fileName)
        self.imageEdgeDetection = cv2.rotate(self.imageEdgeDetection, cv2.ROTATE_90_CLOCKWISE)
        self.displayImagesThreshold()
        self.drawHistograms(self.imageEdgeDetection)
        
        self.image_data = cv2.imread(fileName, 0)
        self.read_image(self.image_beforeEdgeDetection, self.image_data)
        self.grayScaleImage = cv2.cvtColor(self.imageEdgeDetection, cv2.COLOR_BGR2GRAY)
        histogramCurve, distributionCurve = curves.drawCurves(self.image_data)

        view = self.image_histogramCurve.addViewBox()
        view.addItem(histogramCurve)
        distributionView = self.image_distributionCurve.addViewBox()
        distributionView.addItem(distributionCurve )
        self.checkMaskType()

        if not self.image_mixed:
            self.read_image(self.image_originalFrequencies, self.image_data)

    def on_edgeMaskType_change(self, index):
        self.currentTypeIndex = index
        self.checkMaskType()

    def checkMaskType(self):
        detector = EdgeDetector(self)  # Create an instance of EdgeDetector

        # Display the original image before edge detection
        self.showFinalImage(self.image_beforeEdgeDetection)

        if self.currentTypeIndex == 0:
            img = detector.sobelEdgeDetection(self.image, self.edgeDetectionDirection)
        elif self.currentTypeIndex == 1:
            img = detector.prewittEdgeDetection(self.image, self.edgeDetectionDirection)
        elif self.currentTypeIndex == 2:
            img = detector.robertEdgeDetection(self.image, self.edgeDetectionDirection)
        else:
            img = detector.cannyEdgeDetection(self.image)
        
        self.showFinalImage(img)







    def on_edgeMaskDirection_change(self, index):
        if index == 0:
            self.edgeDetectionDirection = "Horizontal"
            self.checkMaskType()
        else:
            self.edgeDetectionDirection = "Vertical"
            self.checkMaskType()

    def clear_view_box(self,graph_widget):
        if graph_widget is not None:
            graph_widget.clear()

    def read_image(self,graph_name, img_data):
        if self.vb is not None:
            self.clear_view_box(graph_name)
        img_data = cv2.rotate(img_data, cv2.ROTATE_90_CLOCKWISE)
        self.vb = graph_name.addViewBox()

        img = pg.ImageItem(img_data)
        self.vb.addItem(img)
        # self.vb.setAspectLocked(True)  # Lock aspect ratio to prevent scaling
        # self.vb.autoRangeEnabled = False  # Disable auto-scaling


    def freq_domain_filters(self,low_pass_applied,type_filter="Ideal"):
        cut_off_freq = int(self.slider_adjustFrequency.value())
        img_filtered_data = self.filter_types[type_filter](self.image_data, cut_off_freq, low_pass_applied)

        if self.image_mixed:
            self.counter += 1
            if low_pass_applied:
                self.img_data_low_pass = img_filtered_data
                self.read_image(self.image_lowPass, np.abs(img_filtered_data))
            else:
                self.img_data_high_pass = img_filtered_data
                self.read_image(self.image_highPass, np.abs(img_filtered_data))
        else:
            self.read_image(self.image_filteredFrequencies, np.abs(img_filtered_data))

    def mix_images(self,img_data1,img_data2):
        result = hyprid_images(img_data1,img_data2)
        self.read_image(self.image_result, result)

    def showFinalImage(self, edgeDetectedImage):
        self.image_afterEdgeDetection.clear()
        edgeDetectedImage = pg.ImageItem(edgeDetectedImage)
        view = self.image_afterEdgeDetection.addViewBox()
        view.addItem(edgeDetectedImage)

    def drawHistograms(self,image):

        histogram_r,histogram_g,histogram_b,cdf_r,cdf_g,cdf_b = RGBHistogram.drawRGBHistograms(image)
        
        if self.radioButton_normalHistogram.isChecked():
            
            # Plot histograms in respective PlotWidget objects
            RGBHistogram.plotHistogram(histogram_r, 'red', self.image_redHistogram)
            RGBHistogram.plotHistogram(histogram_g, 'green', self.image_greenHistogram)
            RGBHistogram.plotHistogram(histogram_b, 'blue', self.image_blueHistogram)
            

        elif self.radioButton_cumulative.isChecked(): 
            
            # Plot cumulative functions
            RGBHistogram.plotCumulative(cdf_r, 'r', self.image_redHistogram)
            RGBHistogram.plotCumulative(cdf_g, 'g', self.image_greenHistogram)
            RGBHistogram.plotCumulative(cdf_b, 'b', self.image_blueHistogram)
            
        else:
            
            # Neither radio button is checked
            self.image_redHistogram.clear()
            self.image_greenHistogram.clear()
            self.image_blueHistogram.clear()
            pass    

    
    
    def updateThreshold(self, value):

        # Convert image to grayscale if it's not already
        if len(self.imageEdgeDetection.shape) == 3:
            gray_image = cv2.cvtColor(self.imageEdgeDetection, cv2.COLOR_RGB2GRAY)
        else:
            gray_image = self.imageEdgeDetection


        self.global_threshold = Thresholding.GlobalThresholding(value,gray_image)

        # Local thresholding
        block_size = 39
        self.local_threshold = Thresholding.adaptive_thresholdGaussian(gray_image, block_size, value/255)
        self.displayImagesThreshold()



    def displayImagesThreshold(self):

        self.image_beforeThresholding.clear()
        ImageBeforeThresholding = pg.ImageItem(self.grayScaleImage)
        BeforeThresholding = self.image_beforeThresholding.addViewBox()
        BeforeThresholding.addItem(ImageBeforeThresholding)

        
        if self.radioButton_globalThresholding.isChecked():
            # Perform global thresholding
            self.image_afterThresholding.clear()
            ImageAfterThresholding = pg.ImageItem(self.global_threshold)
            AfterThresholding = self.image_afterThresholding.addViewBox()
            AfterThresholding.addItem(ImageAfterThresholding)
            pass

        elif self.radioButton_localThresholding.isChecked():
            # Perform local thresholding
            self.image_afterThresholding.clear()
            ImageAfterThresholding = pg.ImageItem(self.local_threshold)
            AfterThresholding = self.image_afterThresholding.addViewBox()
            AfterThresholding.addItem(ImageAfterThresholding)    
            pass

        else:
            # Neither radio button is checked
            self.image_afterThresholding.clear()
            pass
"""
    
    





def main():
    app = QApplication(sys.argv)
    window = MyTabWidget("MainWindow.ui")
    window.showFullScreen()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()