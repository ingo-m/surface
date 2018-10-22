"""
Create FSL EV files.

Create EV files for an FSL FEAT analysis from custom-made event matrices used
for stimulus presentation.

(C) Ingo Marquardt, 2017
"""


# -----------------------------------------------------------------------------
# *** Import modules

import os
import numpy as np
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# *** Define parameters

# Load environmental variable defining the input data path:
pacman_anly_path = str(os.environ['pacman_anly_path'])

# Input directory:
strPathInput  = (pacman_anly_path
                 + 'FSL_MRI_Metadata/version_03c_transients/')

# Output directory:
strPathOutput = strPathInput

# Input file name (with run number left open):
strFleNme = 'PacMan_run_{}_eventmatrix.txt'

# The name of the events, in the order of their indexing in the event matrix.
# I.e., if REST is coded as 1 and TARGET as 2, REST needs to be first, and
# TARGET second in this list, etc.

# PacMan version 03c:
# * Runs 01, 03, 05 are 'PacMan_Dynamic'
# * Runs 02, 04, 06 are 'Control_Dynamic'
# * Run 08 is 'PacMan_Dynamic' with long rest and stimulus blocks
# This has to be considered when setting up the 2nd level feat analysis.
lstEventTypes = ['Rest',
                 'Target',
                 'Stimulus']

# List of runs (run 07 is the pRF mapping run):
lstRuns = ['01', '02', '03', '04', '05', '06', '08']

# The number of different event types in the event matrix file. For each type
# a separate EV file will be created.
varNumCon = len(lstEventTypes)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# *** Create EV files

# Number of runs:
varNumRuns = len(lstRuns)

# Loop through runs:
for idxRun in range(0, varNumRuns):

    # Temporary path to the log file:
    print('---Processing ' + lstRuns[idxRun])
    strPathTemp = (strPathInput + strFleNme.format(lstRuns[idxRun]))

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

        # Create output array. Number of entries is twice the number of event
        # occurences, in order to model both onset and offset of the event.
        aryOutput = np.ones([(varTmpCount * 2), 3])

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

                # ## Create EV file entry for ONSET response event

                # First column of the output matrix (time point of start of
                # event):
                aryOutput[varTmpCount, 0] = aryData[idxTrial, 1]

                # ## Create EV file entry for OFFSET response event

                # First column of the output matrix (time point of start of
                # event):
                aryOutput[(varTmpCount + 1), 0] = np.sum([aryData[idxTrial, 1],
                                                          aryData[idxTrial, 2]])

                # Second column of the output matrix (duration of the event)
                # remains filled with ones (because the onset response is
                # modelled as a transient event).

                # The third column remains filled with ones.

                # Increment the index:
                varTmpCount = varTmpCount + 2

        # Create file name:
        strTmpFilename = (strPathOutput +
                          'EV_func_' +
                          lstRuns[idxRun] +
                          '_' +
                          lstEventTypes[idxCon] +
                          '.txt')

        # Save EV file:
        np.savetxt(strTmpFilename,
                   aryOutput,
                   fmt='%.2f %.2f %.1f',
                   delimiter=' ',
                   newline='\n')
# -----------------------------------------------------------------------------

print('done')
