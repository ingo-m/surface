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

mv ${strPath}func_01 ${strPath}prf_01
mv ${strPath}func_02 ${strPath}prf_02

mv ${strPath}func_03 ${strPath}func_01
mv ${strPath}func_04 ${strPath}func_02
mv ${strPath}func_05 ${strPath}func_03
mv ${strPath}func_06 ${strPath}func_04
mv ${strPath}func_07 ${strPath}func_05
mv ${strPath}func_08 ${strPath}func_06

mv ${strPath}func_09 ${strPath}prf_03
#-------------------------------------------------------------------------------
