
#main_dir="/data/NIMH_scratch/kleinrl/shared/cluster_fractional_anisotrophy"
#main_dir=$(pwd)

data_dir="$main_dir/data"
roi_dir="$main_dir/rois"

epi=$main_dir"/data/sub-02_ses-07_task-movie_run-01_VASO_spc.nii"
mask=$roi_dir"/sess07-run01_slice84_clustNum9_mask.nii"
epi_masked=$main_dir"/data/sub-02_ses-07_task-movie_run-01_VASO_spc_masked.nii"
epi_clustered=$main_dir"/data/sub-02_ses-07_task-movie_run-01_VASO_spc_clustered_9.nii"


export PATH="$(pwd)/code:$PATH"


# SLICE DLPFC FEF PP
3dcalc -a $epi -b $mask -expr 'a*b' -prefix $epi_masked

cluster.py --epi $epi_masked --clustNum 9 --prefix $epi_clustered 

get_cluster_FA.py --prefix clust9_r3.nii  --epi $epi_clustered --r 3 




# searchlight_trad_FA.py 
# searchlight_LAYNII_FA.py 









# # SLICE DLPFC FEF PP
# 3dcalc -a $epi -b $mask -expr 'a*b' -prefix $epi_masked

# cluster.py --epi $epi_masked --clustNum 9 --prefix $epi_clustered 

# get_cluster_FA.py --prefix clust9_r3.nii  --epi $epi_clustered --r 3 

# $ freeview $epi_clustered:LUT clust9_r3.nii