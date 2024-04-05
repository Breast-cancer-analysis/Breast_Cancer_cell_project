## not a working code....

import numpy as np
import pandas as pd
import pickle


def save_pickle(path_name, variable):
    # save a variable into pickle file
    with open(path_name) as file:
        pickle.dump(variable, file)


cell_lines = [231]
# set up the bin_sizes
bin_sizes = [i for i in range(1, 11)]
for i in range(2, 11):
    bin_sizes.append(i*10)


for i in cell_lines:
    for j in bin_sizes:
        