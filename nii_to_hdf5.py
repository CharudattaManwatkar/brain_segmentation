import os
import numpy as np
import nibabel as nib
import h5py


def load_to_numpy(rootdir='BraTS2017TestingData', file_filter=''):
    '''
    Load .nii.gz files as numpy arrays

    Keyword Arguments:
    rootdir -- Root direcotry where all the folders containing different
            .nii.gz files are stored
    file_filter -- Unique substring of the filename of .nii.gz files set
                that you want to load. E.g. "flair", "GlistrBoost", etc.
                Please be sure to use a unique substring (for example use
                "GlistrBoost." and not "GlistrBoost" because using the latter
                will make the function also try to access
                "GlistrBoostManuallyCorrected")
    '''

    # Collect paths of all relevant files
    filepaths = []
    for dir_path, dir_lst, file_lst in os.walk(rootdir):
        filepaths += [os.path.join(dir_path, f)
                      for f in file_lst if os.path.splitext(f)[-1] == '.gz'
                      if file_filter in f]

    # Final array initialization
    all_images = np.empty((len(filepaths), 240, 240, 155))

    # Read files
    idx = 0
    for fp in filepaths:
        nib_obj = nib.load(fp)
        img = np.array(nib_obj.dataobj)
        all_images[idx] = img
        idx += 1

    return all_images


def numpy_to_hdf5(all_images, filename='temp.h5', dataset_name='dataset'):
    '''
    Save numpy arrays as .h5 file
    '''
    h5f = h5py.File(filename, 'w')
    h5f.create_dataset(dataset_name, data=all_images)
    h5f.close()


def main(rootdir='BraTS2017TestingData'):
    all_images = load_to_numpy(rootdir)
    numpy_to_hdf5(all_images)


if __name__ == '__main__':
    main()
