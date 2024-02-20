from functions import correlation_functions as corrf
from functions.FOV_cell import get_all_filenames
from functions.FOV_cell import FOV
from functions.FOV_cell import cell
import pickle
import numpy as np
import os
import random

log_space_numbers = np.logspace(0, 2, num=19, base=10)
bin_sizes = log_space_numbers.tolist()
print(bin_sizes)

shuffle_mode = False

temp_mean_list = []
mean_list_bin = []
path_name = '/Users/ruihongyu/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Year_3/Y3_project/result/'
cell_line = ['10_none']


# cell_line = [231] # used to test the if the result is the same as Foust do
for i in cell_line:
    if shuffle_mode == False:
        # only create folder to store detailed PCC information when we are not in shuffle mode
        folder_name = str(i)
        # Combine the folder name with the desired path
        folder_path = os.path.join(path_name, folder_name)
        # Use os.makedirs() to create the folder and any necessary parent directories
        os.makedirs(folder_path)

    csv_list = get_all_filenames(
        '/Users/ruihongyu/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Year_3/Y3_project/'+str(i))
    print(csv_list)
    for d in bin_sizes:
        if shuffle_mode == False:
            # only create folder to store detailed PCC information when we are not in shuffle mode
            folder_name = 'bin_width_'+str(d)
            # Combine the folder name with the desired path
            folder_path = os.path.join(path_name+str(i), folder_name)
            # Use os.makedirs() to create the folder and any necessary parent directories
            os.makedirs(folder_path)

        for j in csv_list:
            # iterate each file(each FOV)
            view = FOV(j)
            print(view.name)
            all_spike = []
            for z in view.cells:
                # iterate each cell
                # there are two outputs for the get_spike_train function
                temp_list = z.get_spike_train(bin_width=d)[0]

                if shuffle_mode == True:
                    random.shuffle(temp_list)

                # some cell have no event at all, need to exclude them
                if z.no_event == False:
                    all_spike.append(temp_list)
                elif z.no_event == True:
                    view.cells_no_event.append(z)

            correlation_list = corrf.calculate_pairwise_corrs(
                np.array(all_spike))
            # print(correlation_list)

            if len(correlation_list) != 0:
                # some FOV just get one cell on it, no way to calcualte pair PCC of that
                # the mean of certain FOV
                temp_mean_list.append(
                    sum(correlation_list)/len(correlation_list))

            if shuffle_mode == False:
                # only save those details when we are not in the shuffle mode
                file_name = 'PCC_' + view.name + '.plk'
                # saving each PCC for each pairs for this FOV, bin_width and cell lines
                with open(path_name+str(i)+'/bin_width_'+str(d)+'/' + file_name, 'wb') as file:
                    pickle.dump(correlation_list, file)
        mean_list_bin.append(sum(temp_mean_list)/len(temp_mean_list))

        temp_mean_list = []
        # print(temp_mean_list)
    # the PCC mean we gonna plot
    if shuffle_mode == False:
        with open(path_name + 'all_bin_width_' + str(i) + '.plk', 'wb') as file:
            pickle.dump(mean_list_bin, file)
    elif shuffle_mode == True:
        with open(path_name + 'all_bin_width_shuffle' + str(i) + '.plk', 'wb') as file:
            pickle.dump(mean_list_bin, file)

    print(mean_list_bin)

    mean_list_bin = []
