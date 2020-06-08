import csv
from math import log10, floor
from pathlib import Path
from typing import List

import numpy as np


def save_to_csv(file_path: Path, model_data: List[str], x: np.ndarray, y: np.ndarray):
    """
    Save data to csv.

    :param file_path: file's path
    :param model_data: models parameters
    :param x: x data
    :param y: y data
    """
    with open(file_path, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(model_data)
        for row in zip(x, y):
            writer.writerow(row)


def round_sig(number: float, sig: int=2):
    """
    Round number to significant places.

    :param number: number to be rounded
    :param sig: number of significant places
    :return: rounded number
    """
    if number == 0:
        return 0

    return round(number, sig-int(floor(log10(abs(number))))-1)
