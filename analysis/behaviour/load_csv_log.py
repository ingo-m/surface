# -*- coding: utf-8 -*-
"""
Function of PacMan project.
"""

# Part of PacMan analysis library
# Copyright (C) 2018  Ingo Marquardt
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import csv


def load_csv_log(strCsvLog):
    """
    Extract percentage of hits from PacMan experiment log file.

    Parameters
    ----------
    strCsvLog : str
        Path of PacMan experiment log file.

    Returns
    -------
    varPcntHit : float
        Percentage of hits.
    """
    # Open csv log file:
    fleCsvLog = open(strCsvLog, 'r')

    # Read file  with ROI information:
    csvIn = csv.reader(fleCsvLog,
                       delimiter='\n',
                       skipinitialspace=True)

    # Create empty list for CSV data:
    lstCsv = []

    # Loop through csv object to fill list with csv data:
    for lstTmp in csvIn:
        for strTmp in lstTmp:
            lstCsv.append(strTmp[:])

    # Close file:
    fleCsvLog.close()

    # Find 'percentage of hits' entry in csv list:
    strTmp = next(x for x in lstCsv if 'Percentage of hits' in x)

    # Extract percentage of hits (last element):
    varPcntHit = float(strTmp.split()[-1])

    return varPcntHit
