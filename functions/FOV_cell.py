import os
import pandas as pd
import numpy as np
import itertools

class Cellline:
    def __init__(self, cell_folder, time_bins):
        self.time_bins = time_bins #time bins sizes need to be calculated later
        self.cell_files = self.get_all_filenames(cell_folder)
        self.FOVs = [FOV(i,self) for i in self.cell_files]
        self.overall_std = self.calculate_overall_std()
        self.num_of_FOVs = len(self.FOVs)

    def get_all_filenames(self, directory_path):
        filenames = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                filenames.append(os.path.join(root, file))
        return filenames
    
    def calculate_overall_std(self):
        # this is the fucntion to calcualte the overll cell line's std as Trevi insist
        # it will be used later to calculate the 
        total_length = sum(cell.time_length for fov in self.FOVs for cell in fov.cells)
        if total_length == 0:
            return None
        
        overall_mean = sum(cell.mean * cell.time_length for fov in self.FOVs for cell in fov.cells) / total_length
        
        # overall variance
        overall_variance = sum(((cell.std ** 2) + (cell.mean - overall_mean) ** 2) * cell.time_length for fov in self.FOVs for cell in fov.cells) / total_length
        
        # overall std calcualted from variance
        overall_std = np.sqrt(overall_variance)
        return overall_std
    
    def calculate_all_PCCs(self):
        # this is a function to calculat the PCC for all FOVs we get in this cell line
        for i in self.FOVs:
            i.calculate_PCC()
    
class FOV:
    def __init__(self, file_path, cell_line):
        self.cell_line = cell_line
        self.name = file_path.split('/')[-1][:-4]
        self.df = pd.read_csv(file_path)
        self.num_of_cells = len(self.df)
        self.cells = self.get_all_cells() #all cell class in this list
        self.cells_no_event = []
        self.pairs_names = [i[1] for i in enumerate(itertools.combinations([i.num for i in self.cells], 2))]
        self.pairs_objects = [i[1] for i in enumerate(itertools.combinations([i for i in self.cells], 2))]
        self.table = self.create_empty_table()

    def get_all_cells(self):
        # each element is a cell object
        all_cells = []
        for i in range(self.num_of_cells):
            all_cells.append(cell(self.df.iloc[i], self))
        return all_cells
    
    def updata_all_spike_train(self, bin_size):
        # this function can update all the cell's spike trains in this FOV for different bin width
        # all spike trains must be updated before calculate PCC
        for cell in self.cells:
            cell.get_spike_train(bin_width = bin_size)

    def create_empty_table(self):
        # one csv file for each FOV
        data = {
            'cell1': [item[0] for item in self.pairs_names],
            'cell2': [item[1] for item in self.pairs_names]
            }
        column_names = ['cell1','cell2'] + [str(i) for i in self.cell_line.time_bins]
        return pd.DataFrame(data, columns=column_names)
    
    def calculate_PCC(self):
        # this is the fucntion calculat the PCC and put it back to the table
        column_in_table = 2
        # iterate all the bins
        for i in self.cell_line.time_bins:
            self.updata_all_spike_train(bin_size=i)# update all spike trains
            row_in_tale = 0
            # iterate all the pairs obeject
            for j in self.pairs_objects:
                self.table.iloc[row_in_tale, column_in_table] = np.abs(
                np.corrcoef(j[0].spike_train, j[1].spike_train)[0, 1]
                )
                row_in_tale += 1
            column_in_table += 1
                

class cell:
    def __init__(self, data, FOV):
        self.FOV = FOV
        self.time_series = data.iloc[3:].values.tolist()
        self.num = self.get_cell_number(data)
        self.std = np.std(self.time_series) 
        self.time_length = len(self.time_series)
        self.no_event = False
        self.mean = sum(self.time_series)/self.time_length
        self.spike_train = None

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

        threshold = 1 - n_std * self.FOV.cell_line.overall_std

        # every time_bin
        for i in range(len(bins) - 1):
            bin_start = bins[i]
            bin_end = bins[i + 1]

            if any(abs(self.time_series[j]) < threshold for j, t in enumerate(time) if bin_start <= t < bin_end):
                spike_train[i] = 1

        if spike_train == [0 for _ in range(len(bins) - 1)]:
            self.no_event = True
            self.FOV.cells_no_event.append(self.num)

        self.spike_train = spike_train



def get_all_filenames(directory_path):
    filenames = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            filenames.append(os.path.join(root, file))
    return filenames
