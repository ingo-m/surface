# -*- coding: utf-8 -*-   #noqa
"""
Experimental stimuli for Pac-Man project, to be run in Psychopy.

##################################################################
# Additional control condition - dark frame on bright background #
##################################################################

The dark-frame control condition should fullfil the following
criteria:

(1) The inner (bright) surface bounded by the frame should have the
    the size & location as the 'real square' and the illusory Kanizsa
    surface; i.e. a side length of 2 * 3.0 deg visual angle.

(2) The area covered by the frame should be identical to that covered
    by the Kanizsa inducers. The radius of the Kanizsa inducers is
    1.5 deg visual angle, and 25% of their area is left open (the
    'mouth'). Thus, the area of one Kanizsa, A_k, inducer is:

        A_k = pi * 1.5 ** 2 * 0.75
            = 5.3

    It follows that the combined area of the four inducer stimuli, A_c,
    is:

        A_c = 5.3 * 4
            = 21.2

    Let x be the side length of the outer edge of the frame, and y be
    the side length of the inner edge of the frame. Further, let A_f be
    the area of the frame:

        A_f = (x ** 2) - (y ** 2)

    The area of the frame is supposed to match the combined area of the
    Kanizs inducers:

        A_f = A_c

    Thus,

             A_f = (x ** 2) - (y ** 2)
        (x ** 2) = A_f + (y ** 2)
               x = sqrt(A_f + (y ** 2))
               x = sqrt(21.2 + (6 ** 2))
               x = 7.56

    The side length of the outer edge of the frame is supposed to be 7.56 deg
    visual angle.

"""

# Part of py_pRF_mapping library
# Copyright (C) 2017 Marian Schneider & Ingo Marquardt
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

import os
import datetime
import numpy as np
from psychopy import visual, core, monitors, logging, event, gui, data

# -----------------------------------------------------------------------------
# *** Define general parameters

# Length of target events [s]:
varDurTar = 0.6

# Akin et al. (2014): "the figures oscillated sinusoidally with a half period
# of 480 ms". Thus, one full oscillation cycle took 960 ms, and the oscillation
# frequency was ca. 1.04 Hz. Our TR is 2.079, which is ca. 0.96 Hz.

# Distance between observer and monitor [cm]:
varMonDist = 99.0  # [99.0] for 7T scanner
# Width of monitor [cm]:
varMonWdth = 30.0  # [30.0] for 7T scanner
# Width of monitor [pixels]:
varPixX = 1920  # [1920.0] for 7T scanner
# Height of monitor [pixels]:
varPixY = 1200  # [1200.0] for 7T scanner

# Size (diameter) of Kanizsa inducers (Pac-Man) [degree of visual angle]:
varKnzSze = 3.0

# Position (x & y displacement from origin) of Kanizsa inducers (Pac-Man)
# [degree of visual angle]:
varKnzPos = 3.0

# Position (absolute x and y coordinates) of dark frame:
varFrmePos = (7.56 * 0.5)

# Luminance of the stimuli and background is matched to Kok and Lange (2014).
#
# Kok, P., & de Lange, F. P. (2014). Shape perception simultaneously up- and
# downregulates neural activity in the primary visual cortex.
#
# Luminance of bright stimuli is 246 [cd / m^2], corresponding to a psychopy
# pixel intensity of -0.26.
#
# Luminance of dark stimuli is 0.43 [cd / m^2], corresponding to a psychopy
# pixel intensity of -0.82.
#
# The conversion from pixel intensity to luminance is based on a luminance
# measurement performed on 13.09.2018.

# Background colour:
lstBckgrd = [-0.26, -0.26, -0.26]

# Pac-Man colour:
lstKnzClr = [-0.82, -0.82, -0.82]

# Time (in seconds) that participants have to respond to a target event in
# order for the event to be logged as a hit:
varHitTme = 2.0
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# *** GUI

# Name of the experiment:
strExpNme = 'Surface'

# Get date string as default session name:
strDate = str(datetime.datetime.now())
lstDate = strDate[0:10].split('-')
strDate = (lstDate[0] + lstDate[1] + lstDate[2])

# List with runs to choose from:
lstRuns = [str(x).zfill(2) for x in range(1, 11)]
lstRuns.append('Dummy')

# Dictionary with experiment metadata:
dicExpInfo = {'Run': lstRuns,
              'Test mode': ['No', 'Yes'],
              'Subject_ID': strDate}

# Pop-up GUI to let the user select parameters:
objGui = gui.DlgFromDict(dictionary=dicExpInfo,
                         title=strExpNme)

# On some systems (windows) the return values from the GUI are not as expected.
# Set their types explicitly:
dicExpInfo['Run'] = str(dicExpInfo['Run'])
dicExpInfo['Test mode'] = str(dicExpInfo['Test mode'])
dicExpInfo['Subject_ID'] = str(dicExpInfo['Subject_ID'])

# Close if user presses 'cancel':
if objGui.OK is False:
    core.quit()

# Testing (if True, timer is displayed):
if dicExpInfo['Test mode'] == 'Yes':
    lgcTest = True
else:
    lgcTest = False
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# *** Logging

# Set clock:
objClck = core.Clock()

# Switch that is used to control the logging of target events:
varSwtTrgtLog = 1

# Control the logging of participant responses:
varSwtRspLog = 0

# The key that the participant has to press after a target event:
strTrgtKey = '1'

# Counter for correct/incorrect responses:
varCntHit = 0  # Counter for hits
varCntMis = 0  # Counter for misses

# Set clock for logging:
logging.setDefaultClock(objClck)

# Add time stamp and experiment name to metadata:
dicExpInfo['Date'] = data.getDateStr().encode('utf-8')
dicExpInfo['Experiment_Name'] = strExpNme

# Path of this file:
strPthMain = os.path.dirname(os.path.abspath(__file__))

# Get parent path:
strPthPrnt = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Path of logging folder (parent to subject folder):
strPthLog = (strPthPrnt
             + os.path.sep
             + 'log')

# If it does not exist, create subject folder for logging information
# pertaining to this session:
if not os.path.isdir(strPthLog):
    os.makedirs(strPthLog)

# Path of subject folder:
strPthSub = (strPthLog
             + os.path.sep
             + str(dicExpInfo['Subject_ID'])
             )

# If it does not exist, create subject folder for logging information
# pertaining to this session:
if not os.path.isdir(strPthSub):
    os.makedirs(strPthSub)

# Name of log file:
strPthLog = (strPthSub
             + os.path.sep
             + '{}_{}_Run_{}_{}'.format(dicExpInfo['Subject_ID'],
                                        dicExpInfo['Experiment_Name'],
                                        dicExpInfo['Run'],
                                        dicExpInfo['Date'])
             )

# Create a log file and set logging verbosity:
fleLog = logging.LogFile(strPthLog + '.log', level=logging.DATA)

# Log parent path:
fleLog.write('Parent path: ' + strPthPrnt + '\n')

# Log run:
fleLog.write('Run: ' + str(dicExpInfo['Run']) + '\n')

# Log condition:
fleLog.write('Test mode: ' + dicExpInfo['Test mode'] + '\n')
fleLog.write('Subject_ID: ' + dicExpInfo['Subject_ID'] + '\n')

# Set console logging verbosity:
logging.console.setLevel(logging.WARNING)

# Array for logging of key presses:
aryKeys = np.array([], dtype=np.float32)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# *** Setup

# Create monitor object:
objMon = monitors.Monitor('Screen_7T_NOVA_32_Channel_Coil',
                          width=varMonWdth,
                          distance=varMonDist)

# Set size of monitor:
objMon.setSizePix([varPixX, varPixY])

# Log monitor info:
fleLog.write(('Monitor distance: varMonDist = '
              + str(varMonDist)
              + ' cm'
              + '\n'))
fleLog.write(('Monitor width: varMonWdth = '
              + str(varMonWdth)
              + ' cm'
              + '\n'))
fleLog.write(('Monitor width: varPixX = '
              + str(varPixX)
              + ' pixels'
              + '\n'))
fleLog.write(('Monitor height: varPixY = '
              + str(varPixY)
              + ' pixels'
              + '\n'))

# Set screen:
objWin = visual.Window(
    size=(varPixX, varPixY),
    screen=0,
    winType='pyglet',  # winType : None, ‘pyglet’, ‘pygame’
    allowGUI=False,
    allowStencil=True,
    fullscr=True,
    monitor=objMon,
    color=lstBckgrd,
    colorSpace='rgb',
    units='deg',
    blendMode='avg'
    )
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# *** Experimental stimuli

# (1a) Kaniza stimulus - upper left:
objKnz01 = visual.RadialStim(
    win=objWin,
    mask=None,
    units='deg',
    pos=(-varKnzPos, varKnzPos),
    size=varKnzSze,
    radialCycles=0,
    angularCycles=0,
    radialPhase=0.0,
    angularPhase=0.0,
    ori=180.0,
    texRes=64,
    angularRes=360,
    visibleWedge=(0.0, 270.0),
    colorSpace='rgb',
    color=lstKnzClr,
    opacity=1.0,
    contrast=-1.0,
    interpolate=False,
    autoLog=False,
    )

# (2a) Kaniza stimulus - upper right:
objKnz02 = visual.RadialStim(
    win=objWin,
    mask=None,
    units='deg',
    pos=(varKnzPos, varKnzPos),
    size=varKnzSze,
    radialCycles=0,
    angularCycles=0,
    radialPhase=0.0,
    angularPhase=0.0,
    ori=270.0,
    texRes=64,
    angularRes=360,
    visibleWedge=(0.0, 270.0),
    colorSpace='rgb',
    color=lstKnzClr,
    opacity=1.0,
    contrast=-1.0,
    interpolate=False,
    autoLog=False,
    )

# (3a) Kaniza stimulus - lower left:
objKnz03 = visual.RadialStim(
    win=objWin,
    mask=None,
    units='deg',
    pos=(-varKnzPos, -varKnzPos),
    size=varKnzSze,
    radialCycles=0,
    angularCycles=0,
    radialPhase=0.0,
    angularPhase=0.0,
    ori=90.0,
    texRes=64,
    angularRes=360,
    visibleWedge=(0.0, 270.0),
    colorSpace='rgb',
    color=lstKnzClr,
    opacity=1.0,
    contrast=-1.0,
    interpolate=False,
    autoLog=False,
    )

# (4a) Kaniza stimulus - lower right:
objKnz04 = visual.RadialStim(
    win=objWin,
    mask=None,
    units='deg',
    pos=(varKnzPos, -varKnzPos),
    size=varKnzSze,
    radialCycles=0,
    angularCycles=0,
    radialPhase=0.0,
    angularPhase=0.0,
    ori=0.0,
    texRes=64,
    angularRes=360,
    visibleWedge=(0.0, 270.0),
    colorSpace='rgb',
    color=lstKnzClr,
    opacity=1.0,
    contrast=-1.0,
    interpolate=False,
    autoLog=False,
    )

# Central square:
objSqrCntr = visual.ShapeStim(
    win=objWin,
    units='deg',
    lineWidth=0.0,
    lineColor=[0.0, 0.0, 0.0],
    lineColorSpace='rgb',
    fillColor=lstBckgrd,
    fillColorSpace='rgb',
    vertices=((-varKnzPos, varKnzPos),
              (varKnzPos, varKnzPos),
              (varKnzPos, -varKnzPos),
              (-varKnzPos, -varKnzPos)),
    closeShape=True,
    pos=(0, 0),
    size=1,
    ori=0.0,
    opacity=1.0,
    contrast=1.0,
    interpolate=False,
    autoLog=False,
    )

# Dark frame (dark square drawn behind central square)
objFrme = visual.ShapeStim(
    win=objWin,
    units='deg',
    lineWidth=0.0,
    lineColor=[0.0, 0.0, 0.0],
    lineColorSpace='rgb',
    fillColor=lstKnzClr,
    fillColorSpace='rgb',
    vertices=((-varFrmePos, varFrmePos),
              (varFrmePos, varFrmePos),
              (varFrmePos, -varFrmePos),
              (-varFrmePos, -varFrmePos)),
    closeShape=True,
    pos=(0, 0),
    size=1,
    ori=0.0,
    opacity=1.0,
    contrast=1.0,
    interpolate=False,
    autoLog=False,
    )

# Full screen square (for changing brackground colour):
objSqrFull = visual.ShapeStim(
    win=objWin,
    units='norm',
    lineWidth=0.0,
    lineColor=[0.0, 0.0, 0.0],
    lineColorSpace='rgb',
    fillColor=lstKnzClr,
    fillColorSpace='rgb',
    vertices=((-1.0, 1.0),
              (1.0, 1.0),
              (1.0, -1.0),
              (-1.0, -1.0)),
    closeShape=True,
    pos=(0, 0),
    size=1,
    ori=0.0,
    opacity=1.0,
    contrast=1.0,
    interpolate=False,
    autoLog=False,
    )

# (1b) Rotated Kaniza stimulus - upper left:
objKnzRot01 = visual.RadialStim(
    win=objWin,
    mask=None,
    units='deg',
    pos=(-varKnzPos, varKnzPos),
    size=varKnzSze,
    radialCycles=0,
    angularCycles=0,
    radialPhase=0.0,
    angularPhase=0.0,
    ori=0.0,
    texRes=64,
    angularRes=360,
    visibleWedge=(0.0, 270.0),
    colorSpace='rgb',
    color=lstKnzClr,
    opacity=1.0,
    contrast=-1.0,
    interpolate=False,
    autoLog=False,
    )

# (2b) Rotated Kaniza stimulus - upper right:
objKnzRot02 = visual.RadialStim(
    win=objWin,
    mask=None,
    units='deg',
    pos=(varKnzPos, varKnzPos),
    size=varKnzSze,
    radialCycles=0,
    angularCycles=0,
    radialPhase=0.0,
    angularPhase=0.0,
    ori=90.0,
    texRes=64,
    angularRes=360,
    visibleWedge=(0.0, 270.0),
    colorSpace='rgb',
    color=lstKnzClr,
    opacity=1.0,
    contrast=-1.0,
    interpolate=False,
    autoLog=False,
    )

# (3b) Rotated Kaniza stimulus - lower left:
objKnzRot03 = visual.RadialStim(
    win=objWin,
    mask=None,
    units='deg',
    pos=(-varKnzPos, -varKnzPos),
    size=varKnzSze,
    radialCycles=0,
    angularCycles=0,
    radialPhase=0.0,
    angularPhase=0.0,
    ori=270.0,
    texRes=64,
    angularRes=360,
    visibleWedge=(0.0, 270.0),
    colorSpace='rgb',
    color=lstKnzClr,
    opacity=1.0,
    contrast=-1.0,
    interpolate=False,
    autoLog=False,
    )

# (4b) Rotated Kaniza stimulus - lower right:
objKnzRot04 = visual.RadialStim(
    win=objWin,
    mask=None,
    units='deg',
    pos=(varKnzPos, -varKnzPos),
    size=varKnzSze,
    radialCycles=0,
    angularCycles=0,
    radialPhase=0.0,
    angularPhase=0.0,
    ori=180.0,
    texRes=64,
    angularRes=360,
    visibleWedge=(0.0, 270.0),
    colorSpace='rgb',
    color=lstKnzClr,
    opacity=1.0,
    contrast=-1.0,
    interpolate=False,
    autoLog=False,
    )

# Fixation dot:
objFix = visual.Circle(
    objWin,
    units='deg',
    pos=(0.0, 0.0),
    radius=0.05,
    edges=24,
    fillColor=[-0.69, 0.83, 0.63],
    fillColorSpace='rgb',
    lineColor=[-0.69, 0.83, 0.63],
    lineColorSpace='rgb',
    lineWidth=0.0,
    interpolate=False,
    autoLog=False,
    )

# Fication dot surround:
objFixSrd = visual.Circle(
    objWin,
    units='deg',
    pos=(0.0, 0.0),
    radius=0.09,
    edges=24,
    fillColor=[0.95, 0.04, -1.0],
    fillColorSpace='rgb',
    lineColor=[0.95, 0.04, -1.0],
    lineColorSpace='rgb',
    lineWidth=0.0,
    interpolate=False,
    autoLog=False,
    )

# Target:
objTarget = visual.Circle(
    objWin,
    units='deg',
    pos=(0.0, 0.0),
    edges=24,
    radius=0.09,
    fillColor=[0.95, 0.04, -1.0],
    fillColorSpace='rgb',
    lineColor=[0.95, 0.04, -1.0],
    lineColorSpace='rgb',
    lineWidth=0.0,
    interpolate=False,
    autoLog=False,
    )
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# *** Auxiliary stimuli

# Message:
# objTxtWlcm = visual.TextStim(objWin,
#                              text='Please wait a moment.',
#                              font="Courier New",
#                              pos=(0.0, 0.0),
#                              color=[1.0, 1.0, 1.0],
#                              colorSpace='rgb',
#                              opacity=1.0,
#                              contrast=1.0,
#                              ori=0.0,
#                              height=0.8,
#                              antialias=True,
#                              alignHoriz='center',
#                              alignVert='center',
#                              flipHoriz=False,
#                              flipVert=False,
#                              autoLog=False
#                              )

# Timer (only displayed in testing mode):
if lgcTest:
    # The text for the timer:
    objTxtTmr = visual.TextStim(objWin,
                                text='Time',
                                font="Courier New",
                                pos=(0, -5.0),
                                color=[1.0, 1.0, 1.0],
                                colorSpace='rgb',
                                opacity=1.0,
                                contrast=1.0,
                                ori=0.0,
                                height=0.4,
                                antialias=True,
                                alignHoriz='center',
                                alignVert='center',
                                flipHoriz=False,
                                flipVert=False,
                                autoLog=False
                                )

    # Background rectangle to increase visibility of the text:
    objRect = visual.Rect(objWin,
                          pos=(0, -5.0),
                          width=2.5,
                          height=0.6,
                          lineColorSpace='rgb',
                          fillColorSpace='rgb',
                          units='deg',
                          lineWidth=1.0,
                          lineColor=[-0.7, -0.7, -0.7],
                          fillColor=[-0.7, -0.7, -0.7],
                          autoLog=False
                          )
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# *** Trials

# Load event matrix from text file:
strPthDsgn = (strPthPrnt
              + os.path.sep
              + 'design_matrices'
              + os.path.sep
              + 'Run_'
              + dicExpInfo['Run']
              + '_eventmatrix.txt')

# Read design matrix:
aryDesign = np.loadtxt(strPthDsgn, delimiter=' ', unpack=False)

# Total number of events:
varNumEvnts = aryDesign.shape[0]
strTmp = ('Number of events: varNumEvnts = ' + str(varNumEvnts))
logging.data(strTmp)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# *** Function definitions

def func_exit():
    """
    Check whether exit-keys have been pressed.

    The exit keys are 'e' and 'x'; they have to be pressed at the same time.
    This is supposed to make it less likely that they experiment is aborted
    unpurposely.
    """
    # Check keyboard, save output to temporary string:
    lstExit = event.getKeys(keyList=['e', 'x'], timeStamped=False)

    # Whether the list has the correct length (if nothing has happened lstExit
    # will have length zero):
    if len(lstExit) != 0:

        if ('e' in lstExit) and ('x' in lstExit):

            # Log end of experiment:
            logging.data('------Experiment aborted by user.------')

            # Make the mouse cursor visible again:
            event.Mouse(visible=True)

            # Close everyting:
            objWin.close()
            core.quit()
            monitors.quit()
            logging.quit()
            event.quit()

            return 1

        else:
            return 0

    else:
        return 0
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# *** Presentation

# Draw fixation dot:
objFixSrd.draw(win=objWin)
objFix.draw(win=objWin)

objWin.flip()

# Hide the mouse cursor:
event.Mouse(visible=False)

# Wait for scanner trigger pulse & set clock after receiving trigger pulse
# (scanner trigger pulse is received as button press ('5')):
strTrgr = ['0']
while strTrgr[0][0] != '5':
    # Check for keypress:
    lstTmp = event.getKeys(keyList=['5'], timeStamped=False)
    # Whether the list has the correct length (if nothing has happened, lstTmp
    # will have length zero):
    if len(lstTmp) == 1:
        strTrgr = lstTmp[0][0]

# Trigger pulse received, reset clock:
objClck.reset(newT=0.0)

# Main timer which represents the starting point of the experiment:
varTme01 = objClck.getTime()

# Timer that is used to control the logging of stimulus events:
varTme03 = objClck.getTime()

# Start of the experiment:
for idx01 in range(varNumEvnts):  #noqa

    # Check whether exit keys have been pressed:
    if func_exit() == 1:
        break

    # Index for execution of target events:
    varIdxTrgt = 1

    # The first colume of the event matrix signifies the event type (REST is
    # coded as '1', STIMULUS as '3', and TARGET events are coded as '2'):
    varTmpEvntType = aryDesign[idx01][0]

    # The second column of the event matrix signifies the time (in seconds)
    # when the event starts:
    varTmpEvntStrt = aryDesign[idx01][1]

    # The third column of the event matrix signifies the duration (in seconds)
    # of the event:
    varTmpEvntDur = aryDesign[idx01][2]

    # Get the time:
    varTme02 = objClck.getTime()

    # Is the upcoming event a REST BLOCK?
    if varTmpEvntType == 1:

        # Log beginning of rest block:
        strTmp = ('REST start of block '
                  + str(idx01 + 1)
                  + ' scheduled for: '
                  + str(varTmpEvntStrt))
        logging.data(strTmp)

        # Switch target (show target or not?):
        varSwtTrgt = 0

        # Continue with the rest block?
        while varTme02 < (varTme01 + varTmpEvntStrt + varTmpEvntDur):

            # Draw fixation dot:
            objFixSrd.draw(win=objWin)
            objFix.draw(win=objWin)

            # Draw target?
            if varSwtTrgt == 1:

                    # Draw target:
                    objTarget.draw(win=objWin)

                    # Log target?
                    if varSwtTrgtLog == 1:

                        # Log target event:
                        strTmp = ('TARGET scheduled for: '
                                  + str(varTmpTrgtStrt))
                        logging.data(strTmp)

                        # Switch off (so that the target event is only logged
                        # once):
                        varSwtTrgtLog = 0

                        # Once after target onset we set varSwtRspLog to
                        # one so that the participant's respond can be logged:
                        varSwtRspLog = 1

                        # Likewise, just after target onset we set the timer
                        # for response logging to the current time so that the
                        # response will only be counted as a hit in a specified
                        # time interval after target onset:
                        varTme03 = objClck.getTime()

            # Timer (only displayed in testing mode):
            if lgcTest:

                # Set time since experiment onset as message text:
                objTxtTmr.text = str(np.around(varTme02, 1)) + ' s'

                # Draw background rectangle:
                objRect.draw()
                # Draw text:
                objTxtTmr.draw()

            # Flip drawn objects to screen:
            objWin.flip()

            # Check whether exit keys have been pressed:
            if func_exit() == 1:
                break

            # Check for and log participant's response:
            varTme02 = objClck.getTime()
            lstRsps = event.getKeys(keyList=[strTrgtKey], timeStamped=False)

            # Has the response not been reported yet, and is it still within
            # the time window?
            if (varSwtRspLog == 1) and (varTme02 <= (varTme03 + varHitTme)):

                # Check whether the list has the correct length:
                if len(lstRsps) == 1:

                    # Does the list contain the response key?
                    if lstRsps[0] == strTrgtKey:

                        # Log hit:
                        logging.data('Hit')

                        # Count hit:
                        varCntHit += 1

                        # After logging the hit, we have to switch off the
                        # response logging, so that the same hit is nor logged
                        # over and over again:
                        varSwtRspLog = 0

            elif (varSwtRspLog == 1) and (varTme02 > (varTme03 + varHitTme)):

                # Log miss:
                logging.data('Miss')

                # Count miss:
                varCntMis += 1

                # If the subject does not respond to the target within time, we
                # log this as a miss and set varSwtRspLog to zero (so that the
                # response won't be logged as a hit anymore afterwards):
                varSwtRspLog = 0

            # Check whether it's time to show a target on the next frame. Is
            # the upcoming event a target? We first need to check whether the
            # end of the design matrix has not been reached yet. This can
            # happen if there is no target event in the last condition block,
            # and the variable `varIdxTrgt` has been incremented in the second
            # last condition block.
            if (((idx01 + varIdxTrgt) < varNumEvnts) and
                    aryDesign[idx01+varIdxTrgt][0] == 2):

                # Onset time of upcoming target:
                varTmpTrgtStrt = aryDesign[idx01+varIdxTrgt][1]

                # Has the start time of the target event been reached?
                if varTme02 >= (varTme01 + varTmpTrgtStrt):

                    # Target switch on:
                    varSwtTrgt = 1

                    # Has the end time of the target event been reached?
                    if varTme02 >= (varTme01 + varTmpTrgtStrt + varDurTar):

                        # Switch the target off:
                        varSwtTrgt = 0

                        # Switch on the logging of the target event (so that
                        # the next target event will be logged):
                        varSwtTrgtLog = 1

                        # Only increase the index if the end of the design
                        # matrix has not been reached yet:
                        if (idx01 + varIdxTrgt) < varNumEvnts:

                            # Increase the index to check whether the next
                            # event in the design matrix is also a target
                            # event:
                            varIdxTrgt = varIdxTrgt + 1

            # Update current time:
            varTme02 = objClck.getTime()

        # Log end of rest block:
        strTmp = ('REST end of event ' + str(idx01 + 1))
        logging.data(strTmp)

    # Is the upcoming event a STIMULUS BLOCK?
    elif (3 <= varTmpEvntType):

        # Log beginning of stimulus block:
        strTmp = ('STIMULUS start of block '
                  + str(idx01 + 1)
                  + ', condition '
                  + str(varTmpEvntType)
                  + ', scheduled for: '
                  + str(varTmpEvntStrt))
        logging.data(strTmp)

        # Switch target (show target or not?):
        varSwtTrgt = 0

        # Continue with the stimulus block?
        while varTme02 < (varTme01 + varTmpEvntStrt + varTmpEvntDur):

            # Draw Kanizsa square:
            if (varTmpEvntType == 3):
                objKnz01.draw(win=objWin)
                objKnz02.draw(win=objWin)
                objKnz03.draw(win=objWin)
                objKnz04.draw(win=objWin)

            # Draw rotated Kanizsa squares:
            elif (varTmpEvntType == 4):
                objKnzRot01.draw(win=objWin)
                objKnzRot02.draw(win=objWin)
                objKnzRot03.draw(win=objWin)
                objKnzRot04.draw(win=objWin)

            # Draw bright square (on dark background):
            elif (varTmpEvntType == 5):
                objSqrFull.draw(win=objWin)
                objSqrCntr.draw(win=objWin)

            # Draw dark frame (dark square behind bright square):
            elif (varTmpEvntType == 6):
                objFrme.draw(win=objWin)
                objSqrCntr.draw(win=objWin)

            # Draw fixation dot:
            objFixSrd.draw(win=objWin)
            objFix.draw(win=objWin)

            # Draw target?
            if varSwtTrgt == 1:

                    # Draw target:
                    objTarget.draw(win=objWin)

                    # Log target?
                    if varSwtTrgtLog == 1:

                        # Log target event:
                        strTmp = ('TARGET scheduled for: '
                                  + str(varTmpTrgtStrt))
                        logging.data(strTmp)

                        # Switch off (so that the target event is only logged
                        # once):
                        varSwtTrgtLog = 0

                        # Once after target onset we set varSwtRspLog to
                        # one so that the participant's respond can be logged:
                        varSwtRspLog = 1

                        # Likewise, just after target onset we set the timer
                        # for response logging to the current time so that the
                        # response will only be counted as a hit in a specified
                        # time interval after target onset:
                        varTme03 = objClck.getTime()

            # Timer (only displayed in testing mode):
            if lgcTest:

                # Set time since experiment onset as message text:
                objTxtTmr.text = str(np.around(varTme02, 1)) + ' s'

                # Draw background rectangle:
                objRect.draw()
                # Draw text:
                objTxtTmr.draw()

            # Flip drawn objects to screen:
            objWin.flip()

            # Check whether exit keys have been pressed:
            if func_exit() == 1:
                break

            # Check for and log participant's response:
            varTme02 = objClck.getTime()
            lstRsps = event.getKeys(keyList=[strTrgtKey], timeStamped=False)

            # Has the response not been reported yet, and is it still within
            # the time window?
            if (varSwtRspLog == 1) and (varTme02 <= (varTme03 + varHitTme)):

                # Check whether the list has the correct length:
                if len(lstRsps) == 1:

                    # Does the list contain the response key?
                    if lstRsps[0] == strTrgtKey:

                        # Log hit:
                        logging.data('Hit')

                        # Count hit:
                        varCntHit += 1

                        # After logging the hit, we have to switch off the
                        # response logging, so that the same hit is nor logged
                        # over and over again:
                        varSwtRspLog = 0

            elif (varSwtRspLog == 1) and (varTme02 > (varTme03 + varHitTme)):

                # Log miss:
                logging.data('Miss')

                # Count miss:
                varCntMis += 1

                # If the subject does not respond to the target within time, we
                # log this as a miss and set varSwtRspLog to zero (so that the
                # response won't be logged as a hit anymore afterwards):
                varSwtRspLog = 0

            # Check whether it's time to show a target on the next frame. Is
            # the upcoming event a target? We first need to check whether the
            # end of the design matrix has not been reached yet. This can
            # happen if there is no target event in the last condition block,
            # and the variable `varIdxTrgt` has been incremented in the second
            # last condition block.
            if (((idx01 + varIdxTrgt) < varNumEvnts) and
                    aryDesign[idx01+varIdxTrgt][0] == 2):

                # Onset time of upcoming target:
                varTmpTrgtStrt = aryDesign[idx01+varIdxTrgt][1]

                # Has the start time of the target event been reached?
                if varTme02 >= (varTme01 + varTmpTrgtStrt):

                    # Target switch on:
                    varSwtTrgt = 1

                    # Has the end time of the target event been reached?
                    if varTme02 >= (varTme01 + varTmpTrgtStrt + varDurTar):

                        # Switch the target off:
                        varSwtTrgt = 0

                        # Switch on the logging of the target event (so that
                        # the next target event will be logged):
                        varSwtTrgtLog = 1

                        # Only increase the index if the end of the design
                        # matrix has not been reached yet:
                        if (idx01 + varIdxTrgt) < varNumEvnts:

                            # Increase the index to check whether the next
                            # event in the design matrix is also a target
                            # event:
                            varIdxTrgt = varIdxTrgt + 1

            # Update current time:
            varTme02 = objClck.getTime()

        # Log end of stimulus block:
        strTmp = ('STIMULUS end of event ' + unicode(idx01 + 1))
        logging.data(strTmp)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# *** Feedback

logging.data('------End of the experiment.------')

# Performance feedback only if there were any targets:
if 0.0 < float(varCntHit + varCntMis):

    # Ratio of hits:
    varHitRatio = float(varCntHit) / float(varCntHit + varCntMis)

    # Present participant with feedback on her target detection performance:
    if 0.99 < varHitRatio:
        # Perfect performance:
        strFeedback = ('You have detected '
                       + str(varCntHit)
                       + ' targets out of '
                       + str(varCntHit + varCntMis)
                       + '\n'
                       + 'Keep up the good work :)')
    elif 0.9 < varHitRatio:
        # OKish performance:
        strFeedback = ('You have detected '
                       + str(varCntHit)
                       + ' targets out of '
                       + str(varCntHit + varCntMis)
                       + '\n'
                       + 'There is still room for improvement ;)')
    else:
        # Low performance:
        strFeedback = ('You have detected '
                       + str(varCntHit)
                       + ' targets out of '
                       + str(varCntHit + varCntMis)
                       + '\n'
                       + 'Please try to focus more :(')

    # Create text object:
    objTxtTmr = visual.TextStim(objWin,
                                text=strFeedback,
                                font="Courier New",
                                pos=(0.0, 0.0),
                                color=(1.0, 1.0, 1.0),
                                colorSpace='rgb',
                                opacity=1.0,
                                contrast=1.0,
                                ori=0.0,
                                height=0.5,
                                antialias=True,
                                alignHoriz='center',
                                alignVert='center',
                                flipHoriz=False,
                                flipVert=False,
                                autoLog=False)

    # Show feedback text:
    varTme04 = objClck.getTime()
    while varTme02 < (varTme04 + 3.0):
        objTxtTmr.draw()
        objWin.flip()
        varTme02 = objClck.getTime()

    # Log total number of hits and misses:
    logging.data(('Number of hits: ' + str(varCntHit)))
    logging.data(('Number of misses: ' + str(varCntMis)))
    logging.data(('Percentage of hits: '
                  + str(np.around((varHitRatio * 100.0), decimals=1))))
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# *** End of the experiment

# Make the mouse cursor visible again:
event.Mouse(visible=True)

# Close everyting:
objWin.close()
core.quit()
monitors.quit()
logging.quit()
event.quit()
# -----------------------------------------------------------------------------
