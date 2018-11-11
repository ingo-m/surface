#!/bin/bash


# For subject 20181108 there is an additional dataset from a pilot session with
# a different stimulus design ('dark square' condition instead of 'Kanizsa
# rotated'), session ID 20181029. The pilot session included three pRF runs.
# Here, the three pRF runs from session 20181029 are registered to session
# 20181108. The transformation matrix was calculated using ITK snap, based on
# the mean EPI images from both session, and converted into an FSL
# transformation matrix using the c3d_affine_tool:
#     c3d_affine_tool \
#     ~/20181029_to_20181108_itk.mat \
#     -info \
#     -ref ~/20181108_combined_mean.nii.gz \
#     -src ~/20181029_combined_mean.nii.gz \
#     -ras2fsl \
#     -o ~/20181029_to_20181108_fsl.mat
# Note: The pilot experiment (i.e. session 20181029) needs to be processed
#       first, so that the data can be registered here.


# -----------------------------------------------------------------------------
# ### Preparations

# Path of transformation matrix (20181029 to 20181108):
strPthMat="${pacman_anly_path}${pacman_sub_id}/07_pRF/20181029_to_20181108_fsl.mat"

# Target directory for extra-session pRF data:
strPthOut="${pacman_data_path}20181108/nii/retinotopy/extrasession"

# Path of mean EPI image from target session (i.e. 20181108), used as
# reference.
strPthRef="${pacman_data_path}20181108/nii/func_reg_tsnr/combined_mean.nii.gz"

# Input parent directory (containing motion-corrected, distortion-corrected,
# feat-high-pass-filtered pRF data).
strPthIn="${pacman_data_path}20181029/nii/feat_level_1_prf/"

# Create directory for extra-session pRF data:
mkdir ${strPthOut}
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# ### Register extra-session pRF data

flirt \
-interp trilinear \
-in ${strPthIn}prf_01.feat/filtered_func_data.nii.gz \
-ref ${strPthRef} \
-applyxfm -init ${strPthMat} \
-out ${strPthOut}/20181029_prf_01

flirt \
-interp trilinear \
-in ${strPthIn}prf_02.feat/filtered_func_data.nii.gz \
-ref ${strPthRef} \
-applyxfm -init ${strPthMat} \
-out ${strPthOut}/20181029_prf_02

flirt \
-interp trilinear \
-in ${strPthIn}prf_03.feat/filtered_func_data.nii.gz \
-ref ${strPthRef} \
-applyxfm -init ${strPthMat} \
-out ${strPthOut}/20181029_prf_03
# -----------------------------------------------------------------------------
