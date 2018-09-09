# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 11:16:27 2017

@author: vprayagala2

Purpose:
    This script is to read a json file and return pandas data frame
    Input: Absolute Directory Path
    Output : List of File Names in Directory

Version History
1.0     -   First Version

"""

#%%
import os
#%%
def get_files(folder):
    """Return All the files found in specified directory"""
    file_name_list=[f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
    return file_name_list
#%%
