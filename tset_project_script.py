import os
import mobie
from bioio import BioImage
import bioio_tifffile
from bioio.writers import OmeTiffWriter
import imageio
import shutil

def splitchannels(img,path,dimensions):
    num_channels = len(img.channel_names)
    all = []
    allnames = []
    fname = os.path.basename(path).split(".")[0]

    print(f"Converting {path} to {num_channels} single channel image(s): ")
    for i in range(num_channels):
        if os.path.isfile(f"data/tmp_{fname}_C{i+1}.tif"):
            print(f"\tConverted channel {img.channel_names[i]} :D")
            all.append(f"data/tmp_{fname}_C{i+1}.tif")
            allnames.append(f"{i}_{fname}")
            continue

        try:
            tempimg = img.get_image_data("TCZYX",C=i)
            print(f"\tConverted channel {img.channel_names[i]} :D")
            OmeTiffWriter.save(tempimg, f"data/tmp_{fname}_C{i+1}.tif")
            all.append(f"data/tmp_{fname}_C{i+1}.tif")
            allnames.append(f"{i}_{fname}")
        except:
            print(f"Could not convert channel {img.channel_names[i]} :(")

    return all, allnames, dimensions

def checkchannels(path):
    img = BioImage(path, reader=bioio_tifffile.Reader)
    dimensions = 0

    for i in img.shape:
        if i > 1:
            dimensions += 1

    if len(img.channel_names) > 1:
        return splitchannels(img,path,dimensions)
    else:
        print(f"Only one channel found in {path} - no conversion needed :)")
        return [path], [os.path.basename(path)], dimensions
    
def addimg(input_path, im_name, menu_name, project_folder, dataset_name, target, max_jobs, dimension, color=None, unit="nanometer"):
    resolution = (10., 10., 10.)
    
    # TO-DO: check nD dimensions
    chunks = (64,64,64)
    scale_factors = 4 * [[1, 2, 2]]
    
    if dimension == 2:
        chunks = (512,512)
        scale_factors = 4 * [[1, 2]]
    
    view = mobie.metadata.get_default_view("image", im_name)
    if color is not None:
        view = mobie.metadata.get_default_view("image", im_name, color=color)
    

    mobie.add_image(
        input_path=input_path,
        input_key='',
        root=project_folder,
        dataset_name=dataset_name,
        image_name=im_name,
        menu_name=menu_name,
        resolution=resolution,
        chunks=chunks,
        scale_factors=scale_factors,
        is_default_dataset=False,
        target=target,
        max_jobs=max_jobs,
        unit=unit,
        view=view 
    )

def addimgtransform(input_path, im_name, menu_name, project_folder, dataset_name, target, max_jobs, dimension, transform, color=None, unit="nanometer"):
    resolution = (10, 10, 10)
    
    # TO-DO: check nD dimensions
    chunks = (32, 128, 128)
    scale_factors = 4 * [[1, 2, 2]]

    if dimension == 2:
        chunks = (512,512)
        scale_factors = 4 * [[1, 2]]
    

    im = imageio.volread(input_path)
    min_val, max_val = im.min(), im.max()
    view = mobie.metadata.get_default_view(
        "image", im_name,
        source_transform={"parameters": transform},
        contrastLimits=[min_val, max_val]
    )

    mobie.add_image(
        input_path=input_path,
        input_key='',
        root=project_folder,
        dataset_name=dataset_name,
        image_name=im_name,
        menu_name=menu_name,
        resolution=resolution,
        scale_factors=scale_factors,
        transformation=transform,
        chunks=chunks,
        target=target,
        max_jobs=max_jobs,
        view=view,
        unit=unit,
        file_format="bdv.n5"
    )

project_folder = "test_project/data"
dataset_name = "example"
dataset_folder = os.path.join(project_folder, dataset_name)
target = "local"
max_jobs = 4
unit = "nanometers"

source_list = []

def add_file(path, menu_name, unit, transform=None, color=None):
    input_file = path
    raw_name = os.path.basename(input_file).split(".")[0]
    menu_name = menu_name

    all, names, dimensions = checkchannels(input_file)

    if transform:
        if len(all) == 1:
            addimgtransform(all[0],raw_name,menu_name, project_folder, dataset_name, target, max_jobs, dimensions, transform, color=color, unit=unit)
            names = [raw_name]
        else:
            for i, x in enumerate(all):
                addimgtransform(x,f"{i}_{raw_name}",menu_name, project_folder, dataset_name, target, max_jobs, dimensions, transform, color=color, unit=unit)

        source_list.append(names)
        return

    if(len(all) == 1):
        addimg(all[0],raw_name,menu_name, project_folder, dataset_name, target, max_jobs, dimensions, color=color, unit=unit)
        names = [raw_name]
    else:
        for i, x in enumerate(all):
            addimg(x,f"{i}_{raw_name}",menu_name, project_folder, dataset_name, target, max_jobs, dimensions, color=color, unit=unit)

    source_list.append(names)

add_file("data/em_20nm_z_40_145.tif", "em", unit)
'''transformation = [1.8369913620359506,
              -0.5565781005969193,
              -24.28254860249842,
              68.37265958995685,
              -0.08026654420496038,
              1.8421093883743114,
              2.937347223020879,
              -137.17914808990668,
              -6.591949208711867E-17,
              2.5724757460004824E-33,
              0.999999999999993,
              7.638334409421077E-14]
add_file("data/EM04468_2_63x_pos8T_LM_raw.tif", "lm", unit, transform=transformation, color="green")

settings = [{"color": "white", "contrastLimits": [0., 255.]}, {"opacity": 0.75}]

mobie.create_view(dataset_folder, "default",
                  sources=source_list, display_settings=settings,
                  overwrite=True)'''

for dir in os.listdir(os.getcwd()):
    if(dir[0:3] == "tmp"):
        shutil.rmtree(dir)

for file in os.listdir("data"):
    if(file[0:3] == "tmp"):
        os.remove(os.path.join("data",file))