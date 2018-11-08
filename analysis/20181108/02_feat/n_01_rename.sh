#!/bin/bash


################################################################################
# Rename nii files of functional runs. Functional runs are motion-corrected in #
# chronological order (run_01, run_02, etc.). However, main experimental runs  #
# and retinotopy runs may be mixed, and need to be separated for the GLM       #
# analysis. Therefore, nii files are renamed to distinguish between main       #
# experiment and pRF runs (e.g. func_01, func_02, etc. and prf_01, prf_02,     #
#  etc..                                                                       #
################################################################################


#-------------------------------------------------------------------------------
# ### Preparations

# Get data path from environmental variable:
strPath="${pacman_data_path}${pacman_sub_id}/nii/func_reg_distcorUnwrp/"
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# ### Rename files

mv ${strPath}func_01.nii.gz ${strPath}prf_01.nii.gz
mv ${strPath}func_02.nii.gz ${strPath}prf_02.nii.gz

mv ${strPath}func_03.nii.gz ${strPath}func_01.nii.gz
mv ${strPath}func_04.nii.gz ${strPath}func_02.nii.gz
mv ${strPath}func_05.nii.gz ${strPath}func_03.nii.gz
mv ${strPath}func_06.nii.gz ${strPath}func_04.nii.gz
mv ${strPath}func_07.nii.gz ${strPath}func_05.nii.gz
mv ${strPath}func_08.nii.gz ${strPath}func_06.nii.gz

mv ${strPath}func_09.nii.gz ${strPath}prf_03.nii.gz
#-------------------------------------------------------------------------------
