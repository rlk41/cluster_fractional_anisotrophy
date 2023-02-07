#!/usr/bin/env python


import argparse 
import nibabel as nib 
import numpy as np 
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import cut_tree, fcluster, cophenet


        
    
if __name__ == "__main__":



    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--clustNum', type=int)
    parser.add_argument('--prefix', type=str)
    parser.add_argument('--epi', type=str)

    args = parser.parse_args()


    clustNum        = args.clustNum
    prefix          = args.prefix
    epi             = args.epi 


    
    """
    epi="/data/NIMH_scratch/kleinrl/shared/cluster_fractional_anisotrophy/data/sub-02_ses-07_task-movie_run-01_VASO_spc_masked.nii"
    clustNum=9 
    prefix="/data/NIMH_scratch/kleinrl/shared/cluster_fractional_anisotrophy/data/sub-02_ses-07_task-movie_run-01_VASO_spc_clustered_9.nii"
    """



    img_epi         = nib.load(epi)
    data_epi        = img_epi.get_fdata()
    data_epi_flat   = np.mean(data_epi, axis=3)
    
    out = np.zeros(shape=data_epi_flat.shape)


    inds_bool = data_epi_flat != 0 
    inds = np.where(inds_bool )

    ts = data_epi[inds_bool]


    D = np.corrcoef(ts)
    Z = sch.linkage(D, method='ward')


    clustOwnership = fcluster(Z, criterion='maxclust', t=clustNum)

    for i in range(len(inds[0])): 
        x,y,z = inds[0][i], inds[1][i], inds[2][i]
        val = clustOwnership[i]
        out[x,y,z] = val 
        
        
    
    clipped_img = nib.Nifti1Image(out, img_epi.affine, img_epi.header)
    
    
    if not prefix: 
            "clustNum_{}.nii".format(clustNum)
    nib.save(clipped_img, prefix)










