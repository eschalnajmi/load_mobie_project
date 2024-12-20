import os
import mobie
import bioio_tifffile
import imageio
import shutil

from bioio.writers import OmeTiffWriter
from bioio import BioImage

class Project:
    def __init__(self, destination_folder, project_name, dataset_name, target="local", unit="nanometer"):
        self.project_folder = os.path.join(destination_folder,project_name,"data")
        self.dataset_name = dataset_name
        self.dataset_folder = os.path.join(self.project_folder, self.dataset_name)
        self.target = target
        self.max_jobs = 4
        self.unit = unit

        self.source_list = []
        self.menu_names = []
        self.settings=[]

    def splitchannels(self,img,path):
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

        return all, allnames
    
    def checkchannels(self, path):
        img = BioImage(path, reader=bioio_tifffile.Reader)
        self.dimensions = 0

        for i in img.shape:
            if i > 1:
                self.dimensions += 1

        if len(img.channel_names) > 1:
            return self.splitchannels(img, path)
       
        print(f"Only one channel found in {path} - no conversion needed :)")
        return [path], [os.path.basename(path)]
        
    def addimg(self, input_path, im_name, menu_name, color=None):
        resolution = (1, 1, 1)

        project_folder = self.project_folder
        dataset_name = self.dataset_name
        target = self.target
        max_jobs = self.max_jobs
        unit = self.unit

        chunks = (64,64,64)
        scale_factors = 4 * [[1, 2, 2]]

        # TO-DO: check nD dimensions
        if self.dimensions == 2:
            print("2D image")
            chunks = (512,512)
            scale_factors = 4 * [[1, 2]]

        view = mobie.metadata.get_default_view("image", im_name)

        if color is not None:
            view = mobie.metadata.get_default_view("image", im_name, color=color)

        try:
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
        except:
            print(f"Could not add {im_name} to project :(")
            return
        

    def addimgtransform(self,input_path, im_name, menu_name, transform, color=None):
        resolution = (1, 1, 1)
        if len(transform) != 12:
            print("Invalid transformation matrix, must be 12 elements long - your matrix has", len(transform))
            return
        
        chunks = (32, 128, 128)
        scale_factors = 4 * [[1, 2, 2]]
        
        # TO-DO: check nD dimensions
        if self.dimensions == 2:
            chunks = (512,512)
            scale_factors = 4 * [[1, 2]]
        

        im = imageio.volread(input_path)
        min_val, max_val = im.min(), im.max()
        view = mobie.metadata.get_default_view(
            "image", im_name,
            source_transform={"parameters": transform},
            contrastLimits=[min_val, max_val],
        )

        if color is not None:
            view = mobie.metadata.get_default_view(
                "image", im_name,
                source_transform={"parameters": transform},
                contrastLimits=[min_val, max_val],
                color=color
            )

        try:
            mobie.add_image(
                input_path=input_path,
                input_key='',
                root=self.project_folder,
                dataset_name=self.dataset_name,
                image_name=im_name,
                menu_name=menu_name,
                resolution=resolution,
                scale_factors=scale_factors,
                transformation=transform,
                chunks=chunks,
                target=self.target,
                max_jobs=self.max_jobs,
                view=view,
                unit=self.unit,
                file_format="bdv.n5"
            )
        
        except:
            print(f"Could not add {im_name} to project :(")

    def add_file(self, path, menu_name, transform=None, color=None):
        input_file = path
        raw_name = os.path.basename(input_file).split(".")[0]
        menu_name = menu_name

        all, names = self.checkchannels(input_file)

        if transform:
            if len(all) == 1:
                self.addimgtransform(all[0],raw_name,menu_name, transform, color=color)
                names = [raw_name]
            else:
                for i, x in enumerate(all):
                    self.addimgtransform(x,f"{i}_{raw_name}",menu_name, transform, color=color)

            self.source_list.append(names)
            return

        if(len(all) == 1):
            self.addimg(all[0],raw_name,menu_name, color=color)
            names = [raw_name]
        else:
            for i, x in enumerate(all):
                self.addimg(x,f"{i}_{raw_name}",menu_name, color=color)
        
        if menu_name not in self.menu_names:
            self.menu_names.append(menu_name)
            self.source_list.append(names)
        else:
            self.source_list[self.menu_names.index(menu_name)] += names

    def deletetmp(self):
        for dir in os.listdir(os.getcwd()):
            if(dir[0:3] == "tmp"):
                shutil.rmtree(dir)

        for file in os.listdir("data"):
            if(file[0:3] == "tmp"):
                os.remove(os.path.join("data",file))
