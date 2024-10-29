import os

from project import *
from PIL import Image

from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QLineEdit,
    QHBoxLayout,
    QWidget,
    QFileDialog,
    QPushButton,
    QLabel,
    qApp,
)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QFormLayout()

        self.menus = []

        self.project = []

        self.images = []

        self.views = []

        self.setWindowTitle("MOBIE Project Creator")

        self.setLayout(self.layout)

        self.projectwindow()

    def clearlayout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            childWidget = child.widget()
            if childWidget:
                childWidget.setParent(None)
                childWidget.deleteLater()


    def projectwindow(self):
        self.setFixedWidth(500)
        self.setFixedHeight(210)

        self.folder = os.getcwd()
        def selectfolder():
            self.folder = QFileDialog.getExistingDirectory(self, 'Select Folder: ')

        def createproject():
            project_name = get_project_name.text()
            dataset_name = get_dataset_name.text()
            unit = get_unit.text()
            target = str(get_target.currentText())

            self.project = [self.folder, project_name, dataset_name, target, unit]
            self.dataset_folder = os.path.join(project_name, "data", dataset_name)
            folderdisplay.deleteLater()
            self.clearlayout()
            self.filewindow()

        get_project_name = QLineEdit()
        get_dataset_name = QLineEdit()
        get_unit = QLineEdit()
        get_target = QComboBox()
        get_target.addItems(["local", "remote"])


        sflayout = QHBoxLayout()
        selectfolderbtn = QPushButton()
        selectfolderbtn.setText("Select folder")
        selectfolderbtn.clicked.connect(selectfolder)
        folderdisplay = QLineEdit(f"{self.folder}")
        folderdisplay.setReadOnly(True)
        sflayout.addWidget(folderdisplay)
        sflayout.addWidget(selectfolderbtn)
        
        createprojectbtn = QPushButton()
        createprojectbtn.setText("Create project")
        createprojectbtn.clicked.connect(createproject)

        self.layout.addRow("Project folder: ", sflayout)
        self.layout.addRow("Project name: ", get_project_name)
        self.layout.addRow("Dataset name: ", get_dataset_name)
        self.layout.addRow("Unit: ", get_unit)
        self.layout.addRow("Target: ", get_target)
        self.layout.addRow(createprojectbtn)
    
    def filewindow(self):

        def get_file():
            self.file = QFileDialog.getOpenFileName(self, "Select image file")[0]
        
        def add_image():
            menu = get_menu_name.text()
            if not(menu in self.menus):
                self.menus.append(menu)

            transformation = [get_transformation.text()]
            colour = str(get_colour.currentText())

            if colour == " ":
                colour = None
            
            if transformation[0] == "":
                transformation = None

            img = [self.file, menu, transformation, colour]
            self.images.append(img)

            self.clearlayout()
            self.filewindow()

        def nextwindow():
            filedisplay.deleteLater()
            selectfilebtn.deleteLater()
            self.clearlayout()
            self.viewwindow()
        
        self.file = ""
        gflayout = QHBoxLayout()
        selectfilebtn = QPushButton()
        selectfilebtn.setText("Select image")
        selectfilebtn.clicked.connect(get_file)
        filedisplay = QLineEdit(f"{self.file}")
        filedisplay.setReadOnly(True)
        gflayout.addWidget(filedisplay)
        gflayout.addWidget(selectfilebtn)

        get_menu_name = QLineEdit()
        get_transformation = QLineEdit()
        get_colour = QComboBox()
        get_colour.addItems([" ", "green", "red", "blue"])

        addimgbtn = QPushButton()
        addimgbtn.setText("Add image")
        addimgbtn.clicked.connect(add_image)

        nextwindowbtn = QPushButton()
        nextwindowbtn.setText("Finished adding images")
        nextwindowbtn.clicked.connect(nextwindow)

        self.layout.addRow("Image file: ", selectfilebtn)
        self.layout.addRow("Menu name: ", get_menu_name)
        self.layout.addRow("Transformation: ", get_transformation)
        self.layout.addRow("Colour: ", get_colour)
        self.layout.addRow(addimgbtn)
        self.layout.addRow(nextwindowbtn)

    def viewwindow(self):
        sources = []
        settings = []

        def add_menu():
            menu = str(get_menus.currentText())
            colour = str(get_colour.currentText())
            strhighercl = str(get_highercl.text())
            strlowercl = str(get_lowercl.text())
            stropacity = str(get_opacity.text())

            sources.append(menu)

            setting = {}
            if colour != " ":
                setting.update({"color": f"{colour}"})
            
            if strhighercl != '' and strlowercl!='':
                lowercl = float(strlowercl)
                highercl = float(strhighercl)
                setting.update({"contrastLimits": [lowercl,highercl]})
            
            if stropacity != '':
                opacity = float(stropacity)
                setting.update({"opacity": opacity})

            print(setting)

            settings.append(setting)

            get_highercl.clear()
            get_lowercl.clear()
            get_opacity.clear()

        def create_view():
            view_name = get_view_name.text()

            get_view_name.clear()

            view = [self.dataset_folder, view_name, sources, settings]

            self.views.append(view)

        def end():
            qApp.quit()

        get_view_name = QLineEdit()

        get_menus = QComboBox()
        get_menus.addItems([i for i in self.menus if i not in sources])
        get_colour = QComboBox()
        get_colour.addItems([" ", "green", "red", "blue", "white"])
        get_opacity = QLineEdit()

        get_lowercl = QLineEdit()
        get_highercl = QLineEdit()
        contrastlimits = QHBoxLayout()
        lowercltext = QLabel()
        lowercltext.setText("Lower contrast limit: ")
        contrastlimits.addWidget(lowercltext)
        contrastlimits.addWidget(get_lowercl)
        highercltext = QLabel()
        highercltext.setText("Higher contrast limit: ")
        contrastlimits.addWidget(highercltext)
        contrastlimits.addWidget(get_highercl)

        addmenubtn = QPushButton()
        addmenubtn.setText("Add menu")
        addmenubtn.clicked.connect(add_menu)

        opacitynbtn = QHBoxLayout()
        opacitytext = QLabel()
        opacitytext.setText("Opacity: ")
        opacitynbtn.addWidget(opacitytext)
        opacitynbtn.addWidget(get_opacity)
        opacitynbtn.addWidget(addmenubtn)

        createviewbtn = QPushButton()
        createviewbtn.setText("Create view")
        createviewbtn.clicked.connect(create_view)

        completebtn = QPushButton()
        completebtn.setText("Done")
        completebtn.clicked.connect(end)

        self.layout.addRow("View name:", get_view_name)
        self.layout.addRow("Menu:",get_menus)
        self.layout.addRow("Colour:",get_colour)
        self.layout.addRow(contrastlimits)
        self.layout.addRow(opacitynbtn)
        self.layout.addRow(createviewbtn)
        self.layout.addRow(completebtn)

    def getvals(self):
        return self.project, self.images, self.views
