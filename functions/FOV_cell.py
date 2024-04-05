import os
import pandas as pd
import numpy as np


class FOV:
    def __init__(self, file_path):
        self.name = file_path.split('/')[-1][:-4]
        self.df = pd.read_csv(file_path)
        self.num_of_cells = len(self.df)
        self.cells = self.get_all_cells() #all cell class in this list
        self.cells_no_event = []

    def get_all_cells(self):
        # each element is a cell object
        all_cells = []
        for i in range(self.num_of_cells):
            all_cells.append(cell(self.df.iloc[i]))

        return all_cells
    
    def get_distance_matrix(self):
        # for each FOV, get a distane matrix
        return None


class cell:
    def __init__(self, data):
        self.time_series = data.iloc[3:].values.tolist()
        self.num = self.get_cell_number(data)
        self.std = np.std(self.time_series)
        self.time_length = len(self.time_series)
        self.no_event = False



    def get_cell_number(self, data):
        # the actually index(or number) of a cell is witten in 'cell' columne
        return data.iloc[2].split('_')[-1]

    def get_spike_train(self, n_std=2.5, bin_width=1):
        # bin width are the real time??
        samp_t = 0.2  # sampling time interval

        # time, like the real time, in unit of second
        time = [i * samp_t for i in range(len(self.time_series))]

        # time-bin, all value in this list is a 'real time', meaning having a unit of second
        bins = [i * bin_width for i in range(int(max(time) / bin_width) + 1)]
        bins.append(max(time))
        
        # ## for testing the function: 
        # print("lastest time in 'bins'",bins[-1])
        # print("lastest time in 'time'",max(time))
        # print("last number in 'time'",time[-1])
        # print('length of bin:', len(bins))

        spike_train = [0 for _ in range(len(bins) - 1)]

        threshold = 1 - n_std * self.std

        # every time_bin
        for i in range(len(bins) - 1):
            bin_start = bins[i]
            bin_end = bins[i + 1]

            if any(abs(self.time_series[j]) < threshold for j, t in enumerate(time) if bin_start <= t < bin_end):
                spike_train[i] = 1

        if spike_train == [0 for _ in range(len(bins) - 1)]:
            self.no_event = True

        print('length of spikes:',len(spike_train))
        return spike_train, bins



def get_all_filenames(directory_path):
    filenames = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            filenames.append(os.path.join(root, file))
    return filenames
