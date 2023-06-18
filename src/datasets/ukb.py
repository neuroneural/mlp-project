# pylint: disable=too-many-function-args, invalid-name
""" UKB ICA dataset loading script"""
import numpy as np
import pandas as pd

from omegaconf import DictConfig


def load_data(
    cfg: DictConfig,
    dataset_path: str = "/anonpath/datasets/ukb/UKB_sex_data.npz",
    indices_path: str = "/anonpath/datasets/ukb/correct_indices_GSP.csv",
):
    """
    Return UKB data

    Input:
    dataset_path: str = "/anonpath/datasets/ukb/UKB_sex_data.npz"
    - path to the dataset with lablels
    indices_path: str = "/anonpath/datasets/ukb/correct_indices_GSP.csv"
    - path to correct indices/components

    Output:
    features, labels
    """

    data = None
    labels = None
    with np.load(dataset_path) as npzfile:
        data = npzfile["features"]
        labels = npzfile["labels"]

    if cfg.dataset.filter_indices:
        # get correct indices/components
        indices = pd.read_csv(indices_path, header=None)
        idx = indices[0].values - 1
        data = data[:, idx, :]

    data = np.swapaxes(data, 1, 2)
    # data.shape = [n_samples, time_length, feature_size]

    return data, labels
