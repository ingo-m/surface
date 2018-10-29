"""
Create FSL EV files.

The purpose of this script is to create EV files for an FSL FEAT analysis
from custom-made event matrices used for stimulus presentation.

(C) Ingo Marquardt, 2017
"""


# ------------------------------------------------------------------------------
# *** Import modules

import numpy as np
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# *** Define parameters

# The name of the events, in the order of their indexing in the event matrix.
# I.e., if REST is coded as 1 and TARGET as 2, REST needs to be first, and
# TARGET second in this list, etc.. However, in the ParCon Experiment, the
# stimuli are coded in reverse order, the stimulus with the highest index has
# the lowest contrast. Therefore, we have to reverse the order here again so
# that in the resulting EV files, stimulus level 1 will be the stimulus with
# the weakest luminance contrast and 4 that with the highest contrast.

# Event types surface perception experiment:
lstEventTypes = ['Rest',
                 'Target',
                 'Kanizsa',
                 'Dark_square',
                 'Bright_square']

# The number of different event types in the event matrix file. For each type
# a separate EV file will be created.
varNumCon = len(lstEventTypes)

# Input & output:

strPathInput  = '/home/john/PhD/GitLab/surface/analysis/FSL_MRI_Metadata/version_01/'  #noqa
strPathOutput = strPathInput
lstNamesEventfiles = ['Run_01_eventmatrix',
                      'Run_02_eventmatrix',
                      'Run_03_eventmatrix',
                      'Run_04_eventmatrix',
                      'Run_05_eventmatrix',
                      'Run_06_eventmatrix']
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# *** Create EV files

# Number of runs:
varNumRuns = len(lstNamesEventfiles)

# Loop through runs:
for idxRun in range(0, varNumRuns):

    # Temporary path to the log file:
    print('---Processing ' + lstNamesEventfiles[idxRun])
    strPathTemp = (strPathInput + lstNamesEventfiles[idxRun] + '.txt')

    # Read log files:
    aryData = np.loadtxt(strPathTemp,
                         dtype='float',
                         comments='#',
                         delimiter=' ',
                         skiprows=0,
                         usecols=(0, 1, 2))

#    # The original aray was loaded as string. We create an array that contains
#    # the timing information from the log file in floating point notation or
#    # integer:
#    aryData[:,0] = aryData[:,0].astype('float')
#    aryData[:,1] = aryData[:,1].astype('float')
#    aryData[:,2] = aryData[:,2].astype('float')

    # Number of events in the file:
    varNumTrial = len(aryData[:, 0])

    # Create EV files:

    # For loop that cycles through the event types (conditions) and creates a
    # separate EV file for each of them:
    for idxCon in range(0, varNumCon):

        print('------Creating EV file for event type: ' +
              lstEventTypes[idxCon])

        # For loop that cycles through the lines of the event matrix file in
        # order to count the number of occurenecs of the current event (i.e.
        # the number of trials):
        varTmpCount = 0
        for idxTrial in range(0, varNumTrial):
            varTmp = aryData[idxTrial, 0]
            if int(idxCon + 1) == varTmp:
                varTmpCount = varTmpCount + 1
        print('------Number of occurences of event: ' + str(varTmpCount))

        # Create output array:
        aryOutput = np.ones([varTmpCount, 3])

        # For loop that cycles through the lines of the event matrix file in
        # order to create the EV file. We need an index to access the output
        # array:
        varTmpCount = 0
        for idxTrial in range(0, varNumTrial):
            # Check whether the current lines corresponds to the current event
            # type (first column of the event matrix):
            varTmp = aryData[idxTrial, 0]
            # The variable 'idxCon' starts at one, so we have to add one in
            # order to check whether the current line corresponds to the event
            # type:
            if int(idxCon + 1) == varTmp:
                # First column of the output matrix (time point of start of
                # event):
                aryOutput[varTmpCount, 0] = aryData[idxTrial, 1]
                # Second column of the output matrix (duration of the event):
                aryOutput[varTmpCount, 1] = aryData[idxTrial, 2]
                # The third column remains filled with ones.
                # Increment the index:
                varTmpCount = varTmpCount + 1

        # Create file name:
        if idxRun < 9:
            strTmpFilename = (strPathOutput +
                              'EV_func_0' +
                              str((idxRun + 1)) +
                              '_' +
                              lstEventTypes[idxCon] +
                              '.txt')
        else:
            strTmpFilename = (strPathOutput +
                              'EV_func_' +
                              str((idxRun + 1)) +
                              '_' +
                              lstEventTypes[idxCon] +
                              '.txt')

        # Save EV file:
        np.savetxt(strTmpFilename,
                   aryOutput,
                   fmt='%.2f %.2f %.1f',
                   delimiter=' ',
                   newline='\n')
# ------------------------------------------------------------------------------

print('done')
