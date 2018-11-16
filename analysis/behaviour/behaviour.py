# -*- coding: utf-8 -*-
"""
Read experiment log files and evaluate behavioural performance.

Experiment log files are read, and subjects' behavioural performance on
central fixation task is evaluated.
"""

# Part of PacMan analysis library
# Copyright (C) 2018  Ingo Marquardt
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.


import glob
import numpy as np
from load_csv_log import load_csv_log


# *****************************************************************************
# *** Define parameters

# List of subject identifiers:
lstSubIds = ['20181029',
             '20181105',
             '20181107',
             '20181108']

# Path of log files. Subject ID, subject ID, and filname left open.
strPthLog = '/media/sf_D_DRIVE/MRI_Data_PhD/09_surface/{}/log/surface_stim/log/{}/{}.log'
# *****************************************************************************


# *****************************************************************************
# *** Read log files

print('-Evaluiate behavioural performance')

# Number of subjects:
varNumSub = len(lstSubIds)

# List for percent hits:
lstHits = []

for idxSub in range(varNumSub):

    print(('--Subject ' + lstSubIds[idxSub]))

    # Current log directory path (with wildcard for filname):
    strTmp = strPthLog.format(lstSubIds[idxSub], lstSubIds[idxSub], '*')

    # Get list of log files for current subjcet:
    lstFls = sorted(glob.glob(strTmp))

    # Loop through log files (i.e. runs):
    for idxRun in range(len(lstFls)):

        try:
            # Get percent of hits from log file:
            varPcntHit = load_csv_log(lstFls[idxRun])

            print(('---Run ' + str(idxRun + 1) + ': ' + str(varPcntHit)))

            lstHits.append(varPcntHit)

        except StopIteration:
            # If the run was aborted, there is no information on percent hits
            # in the log file.
            pass

# List to array:
aryHits = np.array(lstHits)

# Average performance across subjects:
varMne = np.mean(aryHits)
varSd = np.std(aryHits)

print(('--Mean percent hits across subjects: ' + str(varMne)))
print(('--Standard deviation:                ' + str(varSd)))
# *****************************************************************************
