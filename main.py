from gui import *

app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()

allsources = []

projectvals, images, views = window.getvals()

project = Project(projectvals[0], projectvals[1], projectvals[2], projectvals[3], projectvals[4])

for image in images:
    source = []
    names = project.add_file(image[0], image[1], image[2], image[3])
    source.append(image[1])
    source.append(names)
    allsources.append(source)


for view in views:
    source_list = []

    for menu in view[2]:
        if menu in project.menu_names:
            source_list.append(project.source_list[project.menu_names.index(menu)])
    
    mobie.create_view(view[0], view[1], sources=source_list, display_settings=view[3], overwrite=True)

project.deletetmp()
