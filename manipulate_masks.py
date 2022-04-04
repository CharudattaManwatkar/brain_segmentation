import numpy as np
import nii_to_hdf5 as nph

# TODO: What if masks have more than 3 values?

def combine_masks(all_images):
    combined_masks = np.where(all_images>0, 1, 0)
    return combined_masks

def discard_outer_mask(all_images):
    core_masks = np.where(all_images==1, 1, 0)
    return core_masks

def main():
    for file_filter in ('ManuallyCorrected', 't1Gd'):
        all_images = nph.load_to_numpy(file_filter=file_filter)
        masks_combined = combine_masks(all_images)
        nph.numpy_to_hdf5(masks_combined,
                          filename=file_filter+'_combined_masks.h5')
        del masks_combined
        core_masks = discard_outer_mask(all_images)
        nph.numpy_to_hdf5(core_masks,
                          filename=file_filter+'_core_masks.h5')
        del core_masks



