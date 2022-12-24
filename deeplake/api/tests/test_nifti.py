from nibabel.testing import data_path  # type: ignore

import nibabel as nib  # type: ignore
import numpy as np

import deeplake
import os


def test_nifti(memory_ds):
    with memory_ds as ds:
        # 4D .nii.gz
        ds.create_tensor("nii_gz_4d", htype="nifti", sample_compression="nii.gz")

        nii_gz_4d = os.path.join(data_path, "example4d.nii.gz")
        sample = deeplake.read(nii_gz_4d)
        img = nib.load(nii_gz_4d)

        assert sample.shape == img.shape
        np.testing.assert_array_equal(sample.array, img.get_fdata())

        ds.nii_gz_4d.append(sample)
        np.testing.assert_array_equal(ds.nii_gz_4d.numpy()[0], img.get_fdata())
        assert ds.nii_gz_4d.shape == (1, *sample.shape)

        # 3D .nii.gz
        ds.create_tensor("nii_gz", htype="nifti", sample_compression="nii.gz")

        nii_gz = os.path.join(data_path, "standard.nii.gz")
        sample = deeplake.read(nii_gz)
        img = nib.load(nii_gz)

        assert sample.shape == img.shape
        np.testing.assert_array_equal(sample.array, img.get_fdata())

        ds.nii_gz.append(sample)
        np.testing.assert_array_equal(ds.nii_gz.numpy()[0], img.get_fdata())
        assert ds.nii_gz.shape == (1, *sample.shape)

        # 3D nii
        ds.create_tensor("nii", htype="nifti", sample_compression="nii")

        nii = os.path.join(data_path, "anatomical.nii")
        sample = deeplake.read(nii)
        img = nib.load(nii)

        assert sample.shape == img.shape
        np.testing.assert_array_equal(sample.array, img.get_fdata())

        ds.nii.append(sample)
        np.testing.assert_array_equal(ds.nii.numpy()[0], img.get_fdata())
        assert ds.nii.shape == (1, *sample.shape)


def test_nifti_sample_info(memory_ds):
    with memory_ds as ds:
        ds.create_tensor("abc", htype="nifti", sample_compression="nii.gz")
        ds.abc.append(deeplake.read(os.path.join(data_path, "example4d.nii.gz")))

        sample_info = ds.abc[0].sample_info
        for key in ("affine", "zooms"):
            assert key in sample_info
