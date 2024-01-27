# get files
import matplotlib.pyplot as plt
import pickle
from FOV_cell import get_all_filenames
import numpy as np


def plot_PCC_binsize(file_path, shuffle_path, cell_line_name):
    # Open the file in binary read mode (rb)
    with open(file_path, 'rb') as file:
        # Deserialize and load the object from the file
        loaded_data = pickle.load(file)[-19:]

    with open(shuffle_path, 'rb') as file:
        # Deserialize and load the object from the file
        shuffle_data = pickle.load(file)[-19:]

    # Now, 'loaded_data' contains the deserialized object
    print(loaded_data)

    plt.plot(bin_sizes, loaded_data, color='black', marker='o')
    plt.plot(bin_sizes, shuffle_data, color='blue', linestyle='--', marker='x')

    # Add labels and a title
    plt.xlabel('Bin size')
    plt.ylabel('Correlation coefficient')
    plt.title('temporally correlated in ' + cell_line_name)

    plt.xscale('log')  # Set x-axis to log scale
    plt.yscale('log')  # Set y-axis to log scale

    # Show the plot
    plt.grid(True)  # Add a grid for better visualization
    plt.show()


# generate all the x-axis(bin-width)
log_space_numbers = np.logspace(0, 2, num=19, base=10)
bin_sizes = log_space_numbers.tolist()
print(bin_sizes)

# Specify the file path where the pickle file is located
file_path = '/Users/ruihongyu/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Year_3/Y3_project/result/all_bin_width_'

cell_line = [231]

for i in cell_line:
    shuffle_path = file_path + 'shuffle' + str(i) + '.plk'
    plot_PCC_binsize(file_path+str(i)+'.plk', shuffle_path, str(i))
