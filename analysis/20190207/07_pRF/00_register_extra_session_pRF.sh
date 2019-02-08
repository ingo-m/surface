#!/bin/bash


# For subject 20190207 there are additional pRF runs from two previous
# sessions:
#     20181029: 3 pRF runs
#     20181108: 3 pRF runs
#     20190207: 2 pRF runs (this session)
# Here, the extra-session pRF runs are registered to session 20190207. The
# transformation matrices were calculated using ITK snap, based on the mean
# EPI images from from the respective sessions, and converted into an FSL
# transformation matrix using the c3d_affine_tool:
#     c3d_affine_tool \
#     ~/20181029_to_20190207_itk.mat \
#     -info \
#     -ref ~/20190207_combined_mean.nii.gz \
#     -src ~/20181029_combined_mean.nii.gz \
#     -ras2fsl \
#     -o ~/20181029_to_20190207_fsl.mat
# and
#     c3d_affine_tool \
#     ~/20181108_to_20190207_itk.mat \
#     -info \
#     -ref ~/20190207_combined_mean.nii.gz \
#     -src ~/20181108_combined_mean.nii.gz \
#     -ras2fsl \
#     -o ~/20181108_to_20190207_fsl.mat
# Note: The previosu experiments (i.e. sessions 20181029 & 20181108) need to be
# processed first, so that the data can be registered here.


# -----------------------------------------------------------------------------
# ### Preparations

# Path of transformation matrices:
strPthMat01="${pacman_anly_path}${pacman_sub_id}/07_pRF/20181029_to_20190207_fsl.mat"
strPthMat02="${pacman_anly_path}${pacman_sub_id}/07_pRF/20181108_to_20190207_fsl.mat"

# Target directory for extra-session pRF data:
strPthOut="${pacman_data_path}20190207/nii/retinotopy/extrasession"

# Path of mean EPI image from target session (i.e. 20190207), used as
# reference.
strPthRef="${pacman_data_path}20190207/nii/func_reg_tsnr/combined_mean.nii.gz"

# Input parent directory (containing motion-corrected, distortion-corrected,
# feat-high-pass-filtered extra-session pRF data).
strPthIn="${pacman_data_path}BIDS/${pacman_sub_id_bids}/extrasession_prf/"

# Create directory for extra-session pRF data:
# mkdir ${strPthOut}
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# ### Register extra-session pRF data - 20181029

flirt \
-interp trilinear \
-in ${strPthIn}20181029_prf_01.nii.gz \
-ref ${strPthRef} \
-applyxfm -init ${strPthMat01} \
-out ${strPthOut}/20181029_prf_01

flirt \
-interp trilinear \
-in ${strPthIn}20181029_prf_02.nii.gz \
-ref ${strPthRef} \
-applyxfm -init ${strPthMat01} \
-out ${strPthOut}/20181029_prf_02

flirt \
-interp trilinear \
-in ${strPthIn}20181029_prf_03.nii.gz \
-ref ${strPthRef} \
-applyxfm -init ${strPthMat01} \
-out ${strPthOut}/20181029_prf_03
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# ### Register extra-session pRF data - 20181108

flirt \
-interp trilinear \
-in ${strPthIn}20181108_prf_01.nii.gz \
-ref ${strPthRef} \
-applyxfm -init ${strPthMat02} \
-out ${strPthOut}/20181108_prf_01

flirt \
-interp trilinear \
-in ${strPthIn}20181108_prf_02.nii.gz \
-ref ${strPthRef} \
-applyxfm -init ${strPthMat02} \
-out ${strPthOut}/20181108_prf_02

flirt \
-interp trilinear \
-in ${strPthIn}20181108_prf_03.nii.gz \
-ref ${strPthRef} \
-applyxfm -init ${strPthMat02} \
-out ${strPthOut}/20181108_prf_03
# -----------------------------------------------------------------------------
