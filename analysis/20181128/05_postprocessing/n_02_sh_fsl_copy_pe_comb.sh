#!/bin/bash


###############################################################################
# Copy and rename statistical maps.                                           #
###############################################################################


#------------------------------------------------------------------------------
# Define session IDs & paths:

strPathParent01="${pacman_data_path}${pacman_sub_id}/nii/feat_level_2_comb/"

# Order of conditions (sst = sustained, trn = transient):
# bright_square_txtr_sst
# bright_square_txtr_trn
# bright_square_uni_sst
# bright_square_uni_trn
# pacman_static_txtr_sst
# pacman_static_txtr_trn
# pacman_static_uni_sst
# pacman_static_uni_trn
# target

# Input (feat directories):
lstIn=(feat_level_2_bright_square_txtr_sst \
       feat_level_2_bright_square_txtr_trn \
       feat_level_2_bright_square_uni_sst \
       feat_level_2_bright_square_uni_trn \
       feat_level_2_pacman_static_txtr_sst \
       feat_level_2_pacman_static_txtr_trn \
       feat_level_2_pacman_static_uni_sst \
       feat_level_2_pacman_static_uni_trn \
       feat_level_2_target)

# Output (file names):
lstOt=(bright_square_txtr_sst \
       bright_square_txtr_trn \
       bright_square_uni_sst \
       bright_square_uni_trn \
       pacman_static_txtr_sst \
       pacman_static_txtr_trn \
       pacman_static_uni_sst \
       pacman_static_uni_trn \
       target)

strPathParent02=".gfeat/cope1.feat/stats/pe1.nii.gz"

strPathOutput="${pacman_data_path}${pacman_sub_id}/nii/stat_maps_comb/"
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Copy and rename statistical maps:

echo "---Copy and rename statistical maps---"
date

# Check number of files to be processed:
varNumIn=${#lstIn[@]}

# Since indexing starts from zero, we subtract one:
varNumIn=$((varNumIn - 1))

for index01 in $(seq 0 $varNumIn)
do

	strTmpIn="${strPathParent01}${lstIn[index01]}${strPathParent02}"
	strTmpOut="${strPathOutput}feat_level_2_${lstOt[index01]}_pe.nii.gz"
	echo "------cp ${strTmpIn} ${strTmpOut}"
	cp ${strTmpIn} ${strTmpOut}

done

date
echo "done"
#------------------------------------------------------------------------------
