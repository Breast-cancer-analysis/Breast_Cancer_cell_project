## this script used to test FOV_cell
## now, it is used to test the Data Availability

from functions import correlation_functions as corrf
from functions.FOV_cell import get_all_filenames
from functions.FOV_cell import FOV
from functions.FOV_cell import cell
import pickle
import numpy as np
import os
import random

log_space_numbers = np.logspace(0, 2, num=21, base=10)
bin_sizes = log_space_numbers.tolist()

temp_mean_list = []
mean_list_bin = []
path_name = '/Users/ruihongyu/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Year_3/Y3_project/result/'
cell_line = ['10_none','10','47','474','453','468','51','159','231','wm']

csv_list = get_all_filenames(
        '/Users/ruihongyu/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Year_3/Y3_project/'+str(cell_line[9]))

number_of_cells = 0
number_of_views = 0

for j in csv_list:
    view = FOV(j)
    number_of_cells += view.num_of_cells
    number_of_views += 1
    # print(view.name)
    # all_spike = []
    # for z in view.cells:
    #     # iterate each cell
    #     # there are two outputs for the get_spike_train function
    #     temp_list = z.get_spike_train(bin_width=10)[0]

    #     # some cell have no event at all, need to exclude them
    #     if z.no_event == False:
    #         all_spike.append(temp_list)
    #     elif z.no_event == True:
    #         view.cells_no_event.append(z)


print('number of cells: ', number_of_cells)

print('number of FOVs: ', number_of_views)
