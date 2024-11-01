from gui import *

app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()

allsources = []

projectvals, images, views = window.getvals()

project = Project(projectvals[0], projectvals[1], projectvals[2], projectvals[3], projectvals[4])

imfailed = []
for image in images:
    try:
        source = []
        names = project.add_file(image[0], image[1], image[2], image[3])
        source.append(image[1])
        source.append(names)
        allsources.append(source)
    except Exception:
        imfailed.append(image[0])

imagewindow = imagedoneWindow(imfailed)
imagewindow.show()
app.exec_()

vfailed = []
for view in views:
    source_list = []
    try:
        for menu in view[2]:
            if menu in project.menu_names:
                source_list.append(project.source_list[project.menu_names.index(menu)])
        
        mobie.create_view(view[0], view[1], sources=source_list, display_settings=view[3], overwrite=True)

    except Exception:
        vfailed.append(view[1])

viewwindow = viewdoneWindow(vfailed)
viewwindow.show()
app.exec_()

project.deletetmp()
