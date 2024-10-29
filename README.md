# Mobie Project Creator

A GUI for easier creation of projects for the FiJi plugin [Mobie](mobie.github.io).

Please note that at this moment this interface only works on linux due to dependencies.

## How to run

1. Open your terminal and type in:
'''
git clone https://github.com/eschalnajmie/load_mobie_project.git
'''
'''
cd load_mobie_project
'''

2. Install anaconda (unless you already have it) from [here](https://www.anaconda.com/products/individual)

3. Create and activate a conda environment by typing in:
'''
conda env create -f environment.yaml
'''
'''
conda activate mobie_project
'''

4. Run the actual application by typing in:
'''
python main.py
'''

## Functionality
- Able to create mobie projects containing multiple images, menus and views.
- Automatically splits multichannel images into their individual channels before uploading them to the project.
- Converts all inputted images to the same measurement.

## Limitations
- As of right now, little to no error handling - assumes all inputs will be correct.
- Can't run on macOS or windows - will lead to an error in luigi.