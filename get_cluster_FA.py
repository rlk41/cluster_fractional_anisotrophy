#!/usr/bin/env python


import numpy as np 
import nibabel as nib 
from sklearn.decomposition import PCA
import argparse 


def get_FA(X, n_components = 2): 
    # n_components = 2 
    # sv1 = np.array([[2,2], [1,2],[0,1],[0,0],[-1,0],[-2,-1]])
    # sv2 = np.array([[1,1],[1,0],[1,-1],[0,1],[0,0],[0,-1],[-1,1],[-1,0],[-1,-1]])

    # get_FA(sv1)             
    # get_FA(sv2)


    pca = PCA(n_components=n_components)

    pca.fit(X)

    pc_ev_mean = np.mean( pca.explained_variance_ratio_)

    pc_val = np.sqrt(np.sum([ (p-pc_ev_mean)**2 for p in pca.explained_variance_ratio_ ]))

    # pc_val = np.sqrt((pca.explained_variance_ratio_[0]-pc_ev_mean)**2 + 
    #                  (pca.explained_variance_ratio_[1]-pc_ev_mean)**2 + 
    #                  (pca.explained_variance_ratio_[2]-pc_ev_mean)**2)
    
    
    # len_exp_var = len(pca.explained_variance_ratio_)
    
    # for i in range(len_exp_var):
    #     for ii in range(i, len_exp_var):
    #         print(i,ii) 
            
            
    #pc1, pca.ex
    
    
    pc_val1 = np.sqrt(np.sum(pca.explained_variance_ratio_**2))
    
    fa = np.sqrt(1.5)* (pc_val/pc_val1)
    
    print([pca.explained_variance_ratio_, fa])


    return fa, pc_val


def get_searchlight_FA(slice_data, r=2, n_components=2, type="pc_val"): 
    
    
    out = np.zeros(shape=slice_data.shape)
    
    unq_bool = slice_data != 0 
    unq_inds = np.where(unq_bool )
    
    xs,ys,zs = unq_inds[0], unq_inds[1], unq_inds[2] 
    
    for i in range(len(xs)):
        
        x,y,z = xs[i], ys[i], zs[i]
        
        curr_val = slice_data[x,y,z]
        
        x_low, x_up = x-r, x+r
        y_low, y_up = y-r, y+r
        z_low, z_up = z-r, z+r

        #print("x: {}-{}, y: {}-{}, z: {}-{}".format(x_low, x_up, y_low, y_up, z_low, z_up))

        sl = slice_data[x_low:x_up, y_low:y_up, z_low:z_up]
        
        select_voxs = np.array(np.where(sl == curr_val))
        
        #print(select_voxs)
    
    
        if select_voxs.shape[1] > 1: 
            

            fa, pc_val = get_FA(select_voxs, n_components=n_components )
            #print(fa) 
            
        else: 
            fa, pc_val = 0, 0 
        
        if type == 'fa':
            out[x,y,z] = fa
        elif type == 'pc_val':
            out[x,y,z] = pc_val
        else: 
            out[x,y,z] = pc_val
        
    
    
    return out 


            
            
            

    
    
if __name__ == "__main__":



    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--prefix', type=str)
    parser.add_argument('--epi', type=str)
    parser.add_argument('--r', type=str)

    args = parser.parse_args()


    epi             = args.epi
    prefix          = args.prefix
    r               = args.r 


    """
    slice_path      = "/home/kleinrl/shared/collay_ratio/analyses/sess07-run01_clustNum9/sess07-run01_slice84_clustNum9.nii"
    slice_path      = "/home/kleinrl/shared/collay_ratio/analyses/sess07-run01_slice84_clustNum9/sess07-run01_slice84_clustNum9.nii"
    r=4
    """
    
    epi_img       = nib.load(epi)
    epi_data      = epi_img.get_fdata()



    type        = "pc_val"
    out         = get_searchlight_FA(epi_data, r=r, type=type, n_components=2)
    
    
    
    
    
    
    outpath     = "{}".format(slice_path.rstrip(".nii")+ "_anisotrophy-r{}_{}.nii".format(str(r).zfill(2), type))
    clipped_img = nib.Nifti1Image(out, slice_img.affine, slice_img.header)
    nib.save(clipped_img, outpath)








    """    
    type='pc_val'
    for r in range(21): 
        out         = get_searchlight_FA(slice_data, r=r, type=type)
        outpath     = "{}".format(slice_path.rstrip(".nii")+ "_anisotrophy-r{}_{}.nii".format(str(r).zfill(2), type))
        clipped_img = nib.Nifti1Image(out, slice_img.affine, slice_img.header)
        nib.save(clipped_img, outpath)


    type="fa"
    for r in range(21): 
        out         = get_searchlight_FA(slice_data, r=r, type=type)
        outpath     = "{}".format(slice_path.rstrip(".nii")+ "_anisotrophy-r{}_{}.nii".format(str(r).zfill(2), type))
        clipped_img = nib.Nifti1Image(out, slice_img.affine, slice_img.header)
        nib.save(clipped_img, outpath)

    """
    
    
    """
    get_cluster_FA.py --prefix clust9_r3.nii  --slice_path $slice --r 3 
    
    """