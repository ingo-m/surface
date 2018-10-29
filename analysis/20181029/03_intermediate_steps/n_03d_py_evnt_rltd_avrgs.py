"""
Create event related averages from 4D nii files for jittered event onsets.

In this version, the nii files are UPSAMPLED in the temporal dimension before
creating event-related averages, in order to allow for condition onsets that
are not synchronised to the fMRI sampling rate (i.e. the TR).

Create average time courses from 4D nii files. The inputs to this script are a
list of 4D nii files, and a corresponding list of design matrices in FSL's
'custom 3 column' EV format, describing the occurence of the condition of
interest in the nii files. All nii files need to have the same image
dimensions, and in order for the averaging to be sensible, all condition blocks
need to be of the same length.

(C) Ingo Marquardt, 2017
"""

import os
import copy
import time
import numpy as np
import nibabel as nb
from scipy.interpolate import interp1d

# -----------------------------------------------------------------------------
# *** Check time
varTme_01 = time.clock()

# -----------------------------------------------------------------------------
# *** Define parameters

# Load environmental variables defining the input data path:
pacman_data_path = str(os.environ['pacman_data_path'])
pacman_sub_id = str(os.environ['pacman_sub_id'])
pacman_anly_path = str(os.environ['pacman_anly_path'])

# Parent directory:
strPathParent = (pacman_data_path
                 + pacman_sub_id
                 + '/nii/feat_level_1/')

# List of 4D nii files (location within parent directory):
lstIn_01 = ['func_08.feat/filtered_func_data.nii.gz']

# Directory containing design matrices (EV files):
strPathEV = (pacman_anly_path + 'FSL_MRI_Metadata/version_03c/')

# List of design matrices (EV files), in the same order as input 4D nii files
# (location within parent directory):
lstIn_02 = ['EV_func_08_Stimulus.txt']

# Output directory:
strPathOut = (pacman_data_path
              + pacman_sub_id
              + '/nii/func_reg_averages/')

# Output file name:
strOutFileName = 'ERA_PacMan_Dynamic_Long.nii.gz'

# Upsampling factor for temporal interpolation (e.g., if `varUp = 10`, there
# will be 10 time points for every volume):
varUp = 10

# Volume TR of input nii files:
varTR = 2.079

# Number of volumes that will be included in the average segment before the
# onset of the condition block. NOTE: We get the start time and the duration
# of each block from the design matrices (EV files). In order for the averaging
# to work (and in order for it to be sensible in a conceptual sense), all
# blocks that are included in the average need to have the same duration.
varVolsPre = 5

# Number of volumes that will be included in the average segment after the
# end of the condition block:
varVolsPst = 23

# Normalise time segments? If True, segments are normalised trial-by-trial;
# i.e. each time-course segment is divided by its own pre-stimulus baseline
# before averaging across trials.
lgcNorm = True

# If normalisation is performed, which time points to use as baseline, relative
# to the stimulus condition onset. (I.e., if you specify -3 and 0, the three
# volumes preceeding the onset of the stimulus are used - the interval is
# non-inclusive at the end.)
tplBase = (-3, 0)

# Whether or not to also produces individual event-related segments for each
# trial:
lgcSegs = False
if lgcSegs:
    # Basename for segments:
    strSegs = 'NA'

aa1 = varVolsPre + varVolsPst + (25.0 / varTR)

# -----------------------------------------------------------------------------
# *** Preparations

print('-Create average time courses')

# Number of input 4D nii files:
varNumIn_01 = len(lstIn_01)

# Number of input design matrices:
varNumIn_02 = len(lstIn_02)

# Empty list that will be filled with the list of csv data:
lstEV = [None] * varNumIn_02

# Load design matrices (EV files):
for index_01 in range(0, varNumIn_02):

    print('---Loading: ' + lstIn_02[index_01])

    # Read text file:
    aryTmp = np.loadtxt(
                        (strPathEV + lstIn_02[index_01]),
                        skiprows=0
                        )

    # Append current csv object to list:
    lstEV[index_01] = np.copy(aryTmp)

# Check whether directory for segments of each trial already exists, if not
# create it:
if lgcSegs:

    # Target directory for segments:
    strPathSegs = (strPathOut + 'segs')

    # Check whether target directory for segments exists:
    lgcDir = os.path.isdir(strPathSegs)

    # If directory does exist, delete it:
    if not(lgcDir):

        # Create direcotry for segments:
        os.mkdir(strPathSegs)

    print('---Trial segments will be saved at: ' + strPathSegs)

# We don't load the nii data yet, because loading all input nii files at the
# same time is not memory efficient.

# -----------------------------------------------------------------------------
# *** Create average

# Loop through runs:
for index_02 in range(0, varNumIn_01):

    print('---Processing run: ' + lstIn_01[index_02])

    # Occurences of condition blocks within current run:
    varTmpNumBlck = len(lstEV[index_02][:, 0])

    print('------Number of condition blocks: ' + str(varTmpNumBlck))

    # -------------------------------------------------------------------------
    # *** Load nii data

    print('------Loading 4D nii data')

    # Load input 4D nii files:
    niiTmp = nb.load(
                     (strPathParent + lstIn_01[index_02])
                     )
    # Load data of current run into memory:
    aryTmpRun = niiTmp.get_data()

    # -------------------------------------------------------------------------
    # *** Preparations after loading the first nii file

    if index_02 == 0:

        # Get header of first input image (headers, and therefore image
        # dimensions, are assummed to be identical across runs):
        hdr_01 = niiTmp.header

        # Image dimensions:
        aryDim = np.copy(hdr_01['dim'])

        # Calculate length of segments to be created during the averaging:
        varSegDur = int(np.around(
                                  (float(lstEV[0][0, 1]) / float(varTR)) +
                                  float(varVolsPre) +
                                  float(varVolsPst)
                                  ))

        # Number of time points after upsampling:
        varSegDurUp = varSegDur * int(varUp)

        # Array that will be filled with the individual average time series of
        # all runs:
        aryRunsAvrgs = np.zeros((
                                 varNumIn_01,
                                 aryDim[1],
                                 aryDim[2],
                                 aryDim[3],
                                 varSegDurUp
                                 )).astype(np.float32)

    # -------------------------------------------------------------------------
    # *** Preparations for temporal interpolation (upsampling)

    # Number of volumes (before upsampling):
    varNumVol = aryDim[4]

    # Position of original datapoints (before interpolation):
    vecPosOrig = np.linspace(0.0,
                             float(varNumVol),
                             num=varNumVol,
                             endpoint=False)

    # Create function for interpolation:
    func_interp = interp1d(vecPosOrig,
                           aryTmpRun,
                           kind='linear',
                           axis=3,
                           fill_value='extrapolate')

    # -------------------------------------------------------------------------
    # *** Loop through blocks

    print('------Creating segments for each block')

    # Array that will be filled with segments (of condition blocks) of the
    # current run:
    aryTmpBlcks = np.zeros((
                            varTmpNumBlck,
                            aryDim[1],
                            aryDim[2],
                            aryDim[3],
                            varSegDurUp
                            ),
                           dtype=np.float32)

    for index_03 in range(0, varTmpNumBlck):

        print('---------Block: ' + str(index_03 + 1))

        # ---------------------------------------------------------------------
        # *** Indexing

        # Start time of current block (in seconds, as in EV file):
        varTmpStr = lstEV[index_02][index_03, 0]

        # Convert start time to volumes:
        varTmpStr = float(varTmpStr) / float(varTR)

        # Duration of current block (in seconds, as in EV file):
        varTmpDur = lstEV[index_02][index_03, 1]

        # Convert duration to volumes:
        varTmpDur = float(varTmpDur) / float(varTR)

        # Stop time of current condition:
        varTmpStp = varTmpStr + varTmpDur

        # Subtract pre-condition interval from start time:
        varTmpStr = varTmpStr - varVolsPre

        # Add post-condition interval to stop time:
        varTmpStp = varTmpStp + varVolsPst

        # print(' ')
        # print('varTmpStr')
        # print(varTmpStr)
        # print('varTmpStp')
        # print(varTmpStp)
        # print(' ')
        # print('(varTmpStr * varTR)')
        # print((varTmpStr * varTR))
        # print('(varTmpStp * varTR)')
        # print((varTmpStp * varTR))

        # ---------------------------------------------------------------------
        # *** Temporal interpolation of current segment

        # Positions at which to sample (interpolate) time series:
        vecPosIntp = np.linspace(varTmpStr,
                                 varTmpStp,
                                 num=varSegDurUp,
                                 endpoint=True)

        # Apply interpolation function:
        aryTmpBlcks[index_03, :, :, :, :] = \
            func_interp(vecPosIntp).astype(np.float32)

        # Before upsampling:
        # aa1 = aryTmpRun[131, 15, 74,
        #                 int(np.around(varTmpStr)):int(np.around(varTmpStp))]
        # After upsampling:
        # aa2 = aryTmpBlcks[0, 131, 15, 74, :]

    # -------------------------------------------------------------------------
    # *** Normalisation

    if lgcNorm:

        # Start and stop indicies of baseline interval:
        varBseStr = int(np.around((varVolsPre + tplBase[0]) * varUp))
        varBseStp = int(np.around((varVolsPre + tplBase[1]) * varUp))

        # Get prestimulus baseline:
        aryBse = aryTmpBlcks[:, :, :, :, varBseStr:varBseStp]

        # Mean for each voxel over time (i.e. over the pre-stimulus
        # baseline):
        aryBseMne = np.mean(aryBse, axis=4).astype(np.float32)

        # Get indicies of voxels that have a non-zero prestimulus baseline:
        aryNonZero = np.not_equal(aryBseMne, 0.0)

        # Divide all voxels that are non-zero in the pre-stimulus baseline by
        # the prestimulus baseline:
        aryTmpBlcks[aryNonZero] = np.divide(aryTmpBlcks[aryNonZero],
                                            aryBseMne[aryNonZero, None]
                                            ).astype(np.float32)

    # -------------------------------------------------------------------------
    # *** Save segment

    if lgcSegs:

        # WORK IN PROGRESS

        # Loop through runs again in order to save segments:
        for index_03 in range(0, varTmpNumBlck):

            # Start and stop indicies of segment:
            # ...

            # Create temporary array for current segment:
            # ...

            # Since the resulting 4D nii file that contains the segment differs
            # from the input image in the time dimension, we have to adjust the
            # header before saving the result. Since all segments are of the
            # same size, we only have to do this once, for the first segment:
            if (index_02 == 0) and (index_03 == 0):

                # Retrieve image dimensions from header:
                hdr_02 = copy.deepcopy(hdr_01)

                # Replace time dimension in header with respective dimension of
                # single trial segment:
                hdr_02['dim'][4] = aryTmpTrial.shape[3]

            # Output file name:
            if index_02 < 9:
                strTmp01 = ('0' + str(index_02 + 1))
            else:
                strTmp01 = str(index_02 + 1)
            if index_03 < 9:
                strTmp02 = ('0' + str(index_03 + 1))
            else:
                strTmp02 = str(index_03 + 1)

            strTmp03 = (strPathSegs
                        + '/'
                        + strSegs
                        + '_run_'
                        + strTmp01
                        + '_trial_'
                        + strTmp02
                        + '.nii')

            # Create nii object:
            niiTmpTrial = nb.Nifti1Image(aryTmpTrial,
                                         niiTmp.affine,
                                         header=hdr_02
                                         )

            # Save nii image:
            nb.save(niiTmpTrial, strTmp03)

    # -------------------------------------------------------------------------
    # *** Calculate average within run

    print('------Calculating average within run')

    # In order to reduce memory demands (in case of a large number of runs), we
    # calculate the average time series within runs in a first step, and form
    # the overall average at the end. First, calculate the sum over the fifth
    # dimension (which represents the block number), producing a four-
    # dimensional array:
    aryTmp = np.sum(aryTmpBlcks,
                    axis=0,
                    keepdims=False).astype(np.float32)

    # Divide by number of blocks:
    aryTmp = np.true_divide(aryTmp, varTmpNumBlck).astype(np.float32)

    # Append array to list:
    aryRunsAvrgs[index_02, :, :, :, :] = np.copy(aryTmp).astype(np.float32)

# -----------------------------------------------------------------------------
# *** Calculate average across runs

print('---Calculating average across runs')

# Create the sum over the dimension of the array that represents run number,
# producing a four-dimensional array:
aryAvrg = np.sum(aryRunsAvrgs,
                 axis=0,
                 keepdims=False).astype(np.float32)

# Divide by number of runs:
aryAvrg = np.true_divide(aryAvrg, varNumIn_01).astype(np.float32)

# -----------------------------------------------------------------------------
# *** Save result

# Since the resulting 4D nii file that contains the average time series differs
# from the input image in the time dimension, we have to adjust the header
# before saving the result.

print('---Adjusting header for output nii file')

print('------Original image dimensions: ' + str(hdr_01['dim']))

# Replace time dimension in header with respective dimension of average time
# course:
hdr_01['dim'][4] = aryAvrg.shape[3]
print('------Adjusted image dimensions: ' + str(hdr_01['dim']))
print('---Saving resulting 4D nii file (average across runs)')

# Create nii object:
niiAvrg = nb.Nifti1Image(aryAvrg,
                         niiTmp.affine,
                         header=hdr_01
                         )

# Save nii image:
nb.save(niiAvrg,
        (strPathOut + strOutFileName)
        )

# -----------------------------------------------------------------------------
# *** Check time

varTme_02 = time.clock()
varTme_03 = varTme_02 - varTme_01
print('-Elapsed time: ' + str(varTme_03) + ' s')
print('-Done.')
# -----------------------------------------------------------------------------
