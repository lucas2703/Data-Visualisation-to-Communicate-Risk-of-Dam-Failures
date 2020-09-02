from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout, QSlider
from PyQt5.QtCore import pyqtSlot
import re, sys, csv
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
from PyQt5.QtGui import *
#from PyQt5.QtWebEngineWidgets import *     apparently don't need?
from PyQt5.QtCore import * 
from math import cos, asin, sqrt, pi

QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

stylesheet = """ 
    QTabBar::tab:!selected{ background: #f3f2f1; color: #1c70b8; font-size: 20pt; width: 250px; height: 50px }
    QTabBar::tab:selected{ background: #1c70b8; color: #ffffff; font-size: 20pt }
    QTabWidget>QWidget>QWidget{background: #e0e6e6}
    """
    
# Reading the postcode area into a global array to be used throughout the GUI
with open('CSV_FILES/postcodes.csv', newline = '') as csvfile:
    postcodeDataTemp = list(csv.reader(csvfile))
    postcodeData = np.array(postcodeDataTemp)
    
# Reading the dam data into a global array to be used throughout the GUI
with open('CSV_FILES/dams.csv', newline = '') as csvfile:
    damDataTemp = list(csv.reader(csvfile))
    damData = np.array(damDataTemp)

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        
        # Set program title, icon and it's dimensions
        self.setWindowTitle('Data Visualisation of Dam Failures')
        self.setWindowIcon(QtGui.QIcon('GUI_Images/icon.png'))
        self.setFixedSize(1280 + 40, 920 + 40)
        
        self.table_widget = DamGUIwithTabs(self)
        self.setCentralWidget(self.table_widget)

        self.show()
        
    
class DamGUIwithTabs(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.introductionLayout = QVBoxLayout(self)        
        
        # Initialize tabs
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        
        # Set global style sheet for tabs
        self.tabs.setStyleSheet(stylesheet)  
        
        ################
        ### Home Tab ###
        ################
        self.homeButton = QPixmap('GUI_Images/homeButton.png')
        self.tabs.addTab(self.tab1, QtGui.QIcon('GUI_Images/homeButton.png'), '')
        
        # Set layout
        self.tab1.layout = QtWidgets.QGridLayout()
        
        # Create a label for the home image .jpg and add it to the layout
        self.homeImage = QLabel()
        #self.homeImage.setPixmap(self.homeImagePixmap.scaled((self.homeImage.size()), QtCore.Qt.KeepAspectRatioByExpanding))
        self.contentsPage = QPixmap('GUI_Images/contents.jpg').scaled(1280, 960, QtCore.Qt.KeepAspectRatio)
        self.homeImage.setPixmap(self.contentsPage)
        self.tab1.layout.addWidget(self.homeImage)
        
        # Set layout for tab
        self.tab1.setLayout(self.tab1.layout)
        
        
        ########################
        ### Introduction tab ###
        ########################
        self.tabs.addTab(self.tab2,'Introduction')
        
        # Set layout
        self.tab2.layout = QtWidgets.QGridLayout()
        
        # Counter to track where in the 'introductionSlides' array the page is currently on
        self.introCounter = 0
        self.introductionSlides = ['1-1', '1-2', '1-3', '1-4', '1-5']
        
        # Add introduction image
        self.introduction = QLabel()
        self.introPixmap = QPixmap('GUI_Images/Section 1/' + str(self.introductionSlides[self.introCounter] + '.jpg')).scaled(1280, 960, QtCore.Qt.KeepAspectRatio)
        self.introduction.setPixmap(self.introPixmap)
        self.tab2.layout.addWidget(self.introduction, 0, 0, 100, 1000)
        
        # Add 'Next' button to layout
        self.nextButtonIntro = QPushButton('Next')
        self.nextButtonIntro.setMaximumWidth(120)
        self.nextButtonIntro.setStyleSheet('color: white; background-color: #1c70b8; padding: 2px; border-radius: 0px; font-size: 22pt')
        self.tab2.layout.addWidget(self.nextButtonIntro, 95, 905, 5, 70)
        self.nextButtonIntro.clicked.connect(lambda: self.next_page("intro"))
        
        # Set layout for tab
        self.tab2.setLayout(self.tab2.layout) 
    
    
        ###############################################
        ### Dam failures and risk to the public tab ###
        ###############################################
        self.tabs.addTab(self.tab3, 'Dam Failures')
        
        # Set layout
        self.tab3.layout = QtWidgets.QGridLayout()
        
        # Counter to track where in the 'introductionSlides' array the page is currently on
        self.failRiskCounter = 0
        self.failRiskSlides = ['2-1', '2-2', '2-3', '2-4', '2-5']
        
        # Add first slide via pixmap 
        self.failRisk = QLabel()
        self.failRiskPixmap = QPixmap('GUI_Images/Section 2/' + str(self.failRiskSlides[self.failRiskCounter] + '.jpg')).scaled(1280, 960, QtCore.Qt.KeepAspectRatio)
        self.failRisk.setPixmap(self.failRiskPixmap)
        self.tab3.layout.addWidget(self.failRisk, 0, 0, 100, 1000)
        
        # Add 'Next' button to layout
        self.nextButtonFailRisk = QPushButton('Next')
        self.nextButtonFailRisk.setMaximumWidth(120)
        self.nextButtonFailRisk.setStyleSheet('color: white; background-color: #1c70b8; padding: 2px; border-radius: 75px; font-size: 22pt')
        self.tab3.layout.addWidget(self.nextButtonFailRisk, 95, 905, 5, 70)
        self.nextButtonFailRisk.clicked.connect(lambda: self.next_page("failRisk"))
        
        # Set layout for tab
        self.tab3.setLayout(self.tab3.layout) 
        
    
        #####################################
        ### Understand your local dam tab ###
        #####################################
        self.tabs.addTab(self.tab4, 'Local Dam')
        
        # Set layout
        self.tab4.layout= QtWidgets.QGridLayout()
        
        # Counter to determine what slide we are on
        self.localDamCounter = 0
        self.localDamSlides = ['3-1', '3-2', '3-3']
        
        # First image in the tab, setup pixmap to be changed in later pages
        self.localDam = QLabel()
        self.localDamPixmap = QPixmap('GUI_Images/Section 3/' + str(self.localDamSlides[self.localDamCounter] + '.jpg')).scaled(1280, 960, QtCore.Qt.KeepAspectRatio)
        self.localDam.setPixmap(self.localDamPixmap)
        self.tab4.layout.addWidget(self.localDam, 0, 0, 1000, 100)
        
        # 'Enter a postcode' text label
        self.postcodeLabel = QLabel()
        self.postcodeLabel.setText('Enter a postcode')
        self.postcodeLabel.setFont(QFont('Helvetica', 28))
        self.postcodeLabel.setMaximumWidth(350)
        self.tab4.layout.addWidget(self.postcodeLabel, 450, 15, 100, 25)
        
        # Enter postcode widget
        self.postcode_edit = QtWidgets.QLineEdit()
        self.postcode_edit.setFixedWidth(225)
        self.postcode_edit.setMaximumHeight(75)
        # Placeholder text
        self.postcode_edit.setPlaceholderText('BS40 8XS')
        self.postcode_edit.setFont(QFont('Helvetica', 28))
        self.tab4.layout.addWidget(self.postcode_edit, 450, 40, 100, 10)
        
        # 'Continue' button 
        self.continueButton = QPushButton('Continue')
        self.continueButton.setMaximumWidth(170)
        self.continueButton.setStyleSheet('color: white; background-color: #1c70b8; padding: 2px; border-radius: 75px; font-size: 24pt')
        self.tab4.layout.addWidget(self.continueButton, 520, 40, 100, 20) 
        self.foundDam = False
        self.continueButton.clicked.connect(lambda: [self.findNearestDam(), self.next_page("localDam")])
        
        # Set layout for tab
        self.tab4.setLayout(self.tab4.layout)
        
        
        #######################
        ### Future risk tab ###
        #######################
        self.tabs.addTab(self.tab5, 'Future Risk')
        
        # Set layout
        self.tab5.layout= QtWidgets.QGridLayout()
        
        # Counter to determine what slide we are on
        self.futureRiskCounter = 0
        self.futureRiskSlides = ['4-1', '4-2', '4-3', '4-4']
        
        # Add introduction image
        self.futureRisk = QLabel()
        self.futureRiskPixmap = QPixmap('GUI_Images/Section 4/' + str(self.futureRiskSlides[self.futureRiskCounter] + '.jpg')).scaled(1280, 960, QtCore.Qt.KeepAspectRatio)
        self.futureRisk.setPixmap(self.futureRiskPixmap)
        self.tab5.layout.addWidget(self.futureRisk, 0, 0, 1000, 1000)
        
        # Add 'Next' button to layout
        self.nextButtonFutureRisk = QPushButton('Next')
        self.nextButtonFutureRisk.setMaximumWidth(120)
        self.nextButtonFutureRisk.setStyleSheet('color: white; background-color: #1c70b8; padding: 2px; border-radius: 75px; font-size: 22pt')
        self.tab5.layout.addWidget(self.nextButtonFutureRisk, 950, 905, 50, 70)
        self.nextButtonFutureRisk.clicked.connect(lambda: self.next_page("futureRisk"))
        
        # Decade array for the slider to access
        self.decadeYears = [1900,  1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]

        # Set layout for tab
        self.tab5.setLayout(self.tab5.layout)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)  
    
    def findNearestDam(self):
        
            # Compile a regex expression that validates the postcode layout 
            testPostcode = re.compile('^([A-Za-z][A-Ha-hJ-Yj-y]?[0-9][A-Za-z0-9]? ?[0-9][A-Za-z]{2}|[Gg][Ii][Rr] ?0[Aa]{2})$')
            
            # Conditional statement to test if the postcode is valid to the regex
            if not(testPostcode.match(self.postcode_edit.text())):          
                # Message prompt to tell the user the postcode input is invalid
                postcodeInvalid = QMessageBox()
                postcodeInvalid.setText('Postcode format is invalid, please try again')
                # Is called once but is needed otherwise the dialogue won't appear
                ret = postcodeInvalid.exec()
                self.foundDam = False
                return
                
            # Function to find the area name from its postcode and the postcodes coordinates      
            def findAreaName(postcode):
                # Find position in array where postcode lines up with the 0th column
                temp = np.where(postcodeData == postcode)
                # Access np array to find the postcode area name
                postcode = postcodeData[int(temp[0])][1]
                # Access np array to find postcode coordiantes
                postcodeCoords = [postcodeData[int(temp[0])][2], postcodeData[int(temp[0])][3]]
                # Need to return this value from the function
                return postcode, postcodeCoords
            
            def findClosestDam(postC, damC):
                # Calls the distance() func and returns the smallest distance between
                # latitude and longitude values, empty array to store values
                # (distance is in km)
                temp = []
                # Need optimising
                for i in range(0, len(damDataCoords)):
                    # Place distance and dam name into temp if empty
                    if not temp:
                        temp.append(distance(float(postcodeCoords[0]), float(damDataCoords[i][0]), float(postcodeCoords[1]), float(damDataCoords[i][1])))
                        temp.append(damData[i][2])
                    # If distance to a dam is less distance than the one in temp, replace it
                    if distance(float(postcodeCoords[0]), float(damDataCoords[i][0]), float(postcodeCoords[1]), float(damDataCoords[i][1])) < temp[0]:
                        temp = [distance(float(postcodeCoords[0]), float(damDataCoords[i][0]), float(postcodeCoords[1]), float(damDataCoords[i][1])), damData[i][2]]
                        damIndex = i
                closestDamData = [str(damData[damIndex][2]), str(damData[damIndex][3]), str(damData[damIndex][4]), str(damData[damIndex][5]), str(damData[damIndex][6])]
                return closestDamData
            
            # To correctly calculate the distances of dams from the users input, the Haversine
            # formula must be used to account for the curvature of a sphere 
            # Found: https://en.wikipedia.org/wiki/Haversine_formula
            def distance(lat1, lat2, long1, long2):
                # 1 degree in radians
                rad1 = pi / 180
                # Haversine formula
                alpha = 0.5 - cos((lat2 - lat1) * rad1) / 2 + cos(lat1 * rad1) * cos(lat2 * rad1) * (1 - cos((long2 - long1) * rad1)) / 2
                return 12742 * asin(sqrt(alpha))    
    
            
            # Read the text in the textbox and take the first two chars
            postcode = str(self.postcode_edit.text().upper())[:2]
            
            # Find the area name from the first two letters of the postcode
            areaName, postcodeCoords = findAreaName(postcode)
            
            # Extract dam coordinates from the .csv file
            damDataCoords = damData[:, 0:2]
            
            # Use postcodeCoords and damData coords to find closest dam to users input
            self.closestDam = findClosestDam(postcodeCoords, damDataCoords)
            self.foundDam = True
            print(self.closestDam)

    # Changing values on slider
    def changedValue(self, value):
        # Change the Qlabel pixmap depending on the value of the slider, where the years are stored in an array
        self.futureRisk.setPixmap(QtGui.QPixmap('GUI_Images/Section 4/4-2/' + str(self.decadeYears[value]) + '.jpg'))

    # Function to go to the next page on neccessary tabs
    def next_page(self, page):
        if page == "intro":
            self.introCounter += 1
            
            # Hide next button when at the end of the slides
            if self.introCounter == 4:
                self.nextButtonIntro.hide()
                
            # Add 'Previous' button to layout after first slide
            if self.introCounter == 1:
                # Add 'Previous' button to layout
                self.prevButtonIntro = QPushButton('Previous')
                self.prevButtonIntro.setMaximumWidth(120)
                self.prevButtonIntro.setStyleSheet('color: white; background-color: #1c70b8; padding: 2px; border-radius: 75px; font-size: 22pt')
                self.tab2.layout.addWidget(self.prevButtonIntro, 95, 27, 5, 100)
                self.prevButtonIntro.clicked.connect(lambda: self.prev_page("intro"))
                
            self.introduction.setPixmap(QtGui.QPixmap('GUI_Images/Section 1/' + str(self.introductionSlides[self.introCounter]) + '.jpg'))
            
        elif page == "failRisk":
            self.failRiskCounter += 1
            
            # Hide next button when at the end of the slides
            if self.failRiskCounter == 4:
                self.nextButtonFailRisk.hide()
                
            # Add 'Previous' button to layout after first slide
            if self.failRiskCounter == 1:
                self.prevButtonFailRisk = QPushButton('Previous')
                #self.prevButtonFailRisk.setMaximumWidth(120)
                self.prevButtonFailRisk.setStyleSheet('color: white; background-color: #1c70b8; padding: 2px; border-radius: 75px; font-size: 22pt')
                self.tab3.layout.addWidget(self.prevButtonFailRisk, 95, 27, 5, 100)
                self.prevButtonFailRisk.clicked.connect(lambda: self.prev_page("failRisk"))
                
            self.failRisk.setPixmap(QtGui.QPixmap('GUI_Images/Section 2/' + str(self.failRiskSlides[self.failRiskCounter]) + '.jpg'))
            
        elif page == "localDam":
            if (self.foundDam == False):
                return
            else:
                self.localDamCounter += 1
                # 1&2: Embankment Dam, 3: Gravity Dam, 4: Buttress Dam, 5: Arch Dam
                if self.localDamCounter == 1:
                    if self.closestDam[1] == "1" or self.closestDam[0] == "2":
                        self.localDam.setPixmap(QtGui.QPixmap('GUI_Images/Section 3/' + str(self.localDamSlides[self.localDamCounter]) + '_BlankEmbankment.jpg'))
                        self.hidePostcodeInput()
                        self.displayDamData()
                    elif self.closestDam[1] == "3":
                        self.localDam.setPixmap(QtGui.QPixmap('GUI_Images/Section 3/' + str(self.localDamSlides[self.localDamCounter]) + '_BlankGravity.jpg'))
                        self.hidePostcodeInput()
                        self.displayDamData()
                    elif self.closestDam[1] == "4":
                        self.localDam.setPixmap(QtGui.QPixmap('GUI_Images/Section 3/' + str(self.localDamSlides[self.localDamCounter]) + '_BlankButtress.jpg'))
                        self.hidePostcodeInput()
                        self.displayDamData()
                    else:
                        self.localDam.setPixmap(QtGui.QPixmap('GUI_Images/Section 3/' + str(self.localDamSlides[self.localDamCounter]) + '_BlankArch.jpg'))
                        self.hidePostcodeInput()
                        self.displayDamData()
                        
                # 'Learn more...' transparent button to popout
                self.moreInfo = QtWidgets.QPushButton()
                self.moreInfo.setIcon(QtGui.QIcon('GUI_Images/learnMore.png'))
                self.moreInfo.setIconSize(QtCore.QSize(583, 45))
                self.moreInfo.setStyleSheet('color: white; background-color: #f3f2f1; padding: 0px; border-radius: 75px; font-size: 22pt')
                self.moreInfo.clicked.connect(self.moreInfoPushed)
                self.tab4.layout.addWidget(self.moreInfo, 750, 46, 200, 45) 
                
                        
        elif page == "futureRisk":
            self.futureRiskCounter += 1
            
            # Hide next button when at the end of the slides
            if self.futureRiskCounter == 3:
                self.nextButtonFutureRisk.hide()
                
            if str(self.futureRiskSlides[self.futureRiskCounter]) == '4-2':
                
                # First image in the slider series
                self.futureRisk.setPixmap(QtGui.QPixmap('GUI_Images/Section 4/4-2/1900.jpg'))
                
                # Create a slider for years 1900 - 2020 in decade increments
                self.yearSlider = QSlider()
                self.yearSlider.setOrientation(Qt.Horizontal)
                self.yearSlider.setTickPosition(QSlider.TicksBothSides)
                self.yearSlider.setTickInterval(1)
                self.yearSlider.setMinimum(0)
                self.yearSlider.setMaximum(12)
                self.yearSlider.setSingleStep(1)
                # Had to set max and min height to stop column overlapping from effecting the next and previous button
                self.yearSlider.setMinimumWidth(907)
                self.yearSlider.setMaximumWidth(907)
                self.yearSlider.setFixedHeight(40)
                
                # changedValue function called when the slider detects a change
                self.yearSlider.valueChanged.connect(self.changedValue)
                self.tab5.layout.addWidget(self.yearSlider, 671, 143, 100, 856)
            elif self.futureRiskCounter == 2:
                self.yearSlider.hide()
                self.futureRisk.setPixmap(QtGui.QPixmap('GUI_Images/Section 4/' + str(self.futureRiskSlides[self.futureRiskCounter]) + '.jpg'))
                
            else:
                self.futureRisk.setPixmap(QtGui.QPixmap('GUI_Images/Section 4/' + str(self.futureRiskSlides[self.futureRiskCounter]) + '.jpg'))
        
            # Add 'Previous' button to layout after first slide
            if self.futureRiskCounter == 1:
                self.prevButtonFutureRisk = QPushButton('Previous')
                self.prevButtonFutureRisk.setStyleSheet('color: white; background-color: #1c70b8; padding: 2px; border-radius: 75px; font-size: 22pt')
                self.tab5.layout.addWidget(self.prevButtonFutureRisk, 950, 27, 50, 100)
                self.prevButtonFutureRisk.clicked.connect(lambda: self.prev_page("futureRisk"))
       
    def moreInfoPushed(self):
        self.moreInfo = QLabel()
        self.moreInfoPixmap = QPixmap('GUI_Images/Section 3/3-3.jpg').scaled(1280, 960, QtCore.Qt.KeepAspectRatio)
        self.moreInfo.setPixmap(self.moreInfoPixmap)
        self.moreInfo.setGeometry(80, 50, 1280, 960)
        self.moreInfo.show()
        
        
    # called on section 3 when need to hide the postcode text box input
    def hidePostcodeInput(self):    
        self.postcode_edit.hide()
        self.postcodeLabel.hide()
        self.continueButton.hide()
        
    # Age, capacity etc. labels
    def displayDamData(self):
        # Dam Name label
        self.damNameLabel = QLabel()
        self.damNameLabel.setText(str(self.closestDam[0]))
        self.damNameLabel.setFont(QFont('Helvetica', 32, weight=QtGui.QFont.Bold))
        self.tab4.layout.addWidget(self.damNameLabel, 176, 29, 100, 40)
        # Dam Age label
        self.damAgeLabel = QLabel()
        self.damAgeLabel.setText(str(self.closestDam[2]) + ' years')
        self.damAgeLabel.setFont(QFont('Helvetica', 26))
        self.tab4.layout.addWidget(self.damAgeLabel, 640, 18, 100, 40)
        # Dam Capacity label
        self.damCapacityLabel = QLabel()
        self.damCapacityLabel.setText(str(self.closestDam[3]) + ' x10<sup>3</sup> m<sup>3</sup>')
        self.damCapacityLabel.setFont(QFont('Helvetica', 26))
        self.tab4.layout.addWidget(self.damCapacityLabel, 694, 18, 100, 40)
        # Dam Owner label
        self.damOwnerLabel = QLabel()
        self.damOwnerLabel.setText(str(self.closestDam[4]))
        self.damOwnerLabel.setFont(QFont('Helvetica', 26))
        self.damOwnerLabel.setMaximumWidth(400)
        self.damOwnerLabel.setWordWrap(True)
        self.tab4.layout.addWidget(self.damOwnerLabel, 776, 18, 100, 40)
        
    # Function to go to the previous page on neccessary tabs 
    def prev_page(self, page):
        if page == "intro":
            self.introCounter -= 1
            # Hide previous button when at the first slide
            if self.introCounter == 0:
                self.prevButtonIntro.hide()
                
            # Show next button when at the second-to-last slide
            if self.introCounter == 3:
                self.nextButtonIntro.show()
            
            self.introduction.setPixmap(QtGui.QPixmap('GUI_Images/Section 1/' + str(self.introductionSlides[self.introCounter]) + '.jpg'))
            
        if page == "failRisk":
            self.failRiskCounter -= 1
            # Hide previous button when at the first slide
            if self.failRiskCounter == 0:
                self.prevButtonFailRisk.hide()
            
            # Show next button when at the second-to-last slide
            if self.failRiskCounter == 3:
                self.nextButtonFailRisk.show()
                
            self.failRisk.setPixmap(QtGui.QPixmap('GUI_Images/Section 2/' + str(self.failRiskSlides[self.failRiskCounter]) + '.jpg'))
            
        elif page == "futureRisk":
            self.futureRiskCounter -= 1
            
            # Hide previous button when at the first slide
            if self.futureRiskCounter == 0:
                self.prevButtonFutureRisk.hide()
                
            # Show next button when at the second-to-last slide
            if self.futureRiskCounter == 2:
                self.nextButtonFutureRisk.show()
            
            if str(self.futureRiskSlides[self.futureRiskCounter]) == '4-2':
                self.yearSlider.show()
                self.futureRisk.setPixmap(QtGui.QPixmap('GUI_Images/Section 4/4-2/1900.jpg'))
            elif self.futureRiskCounter == 0:
                self.yearSlider.hide()
                self.futureRisk.setPixmap(QtGui.QPixmap('GUI_Images/Section 4/' + str(self.futureRiskSlides[self.futureRiskCounter]) + '.jpg'))
            else:
                self.futureRisk.setPixmap(QtGui.QPixmap('GUI_Images/Section 4/' + str(self.futureRiskSlides[self.futureRiskCounter]) + '.jpg'))
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # PyQt5 styles
    app.setStyle('Fusion')
    
    ex = App()
    sys.exit(app.exec_())