import matplotlib.pyplot as plt
import numpy as np

def plot_histograms(data_dict, bin_size=None, x_label='Value', y_label='Density', title=None):
    """
    Plot histograms for multiple groups stored in a dictionary.
    
    :param data_dict: Dictionary with keys as labels and values as data lists
    :param bin_size: The number of bins for the histogram or None to auto-choose
    :param x_label: X-axis label
    :param y_label: Y-axis label
    :param title: Plot title
    """
    # Create figure and axis
    plt.figure(figsize=(6, 6))
    
    # Determine bin size if not provided
    if bin_size is None:
        # Set the bin size to be the max range of the datasets divided by 30
        all_data = np.concatenate(list(data_dict.values()))
        bin_size = (max(all_data) - min(all_data)) / 100
    
    # Calculate the bins
    bins = np.arange(min(all_data), max(all_data), bin_size)
    
    # Plot each histogram
    for label, data in data_dict.items():
        plt.hist(data, bins, alpha=0.5, label=label, density=True)
    
    # Add legend, labels, and title
    plt.legend(loc='upper right')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    
    # Show plot
    plt.show()

# Example usage:
# data_groups = {
#     'Group 1': np.random.normal(100, 10, 200),
#     'Group 2': np.random.normal(90, 20, 200),
#     'Group 3': np.random.normal(80, 30, 200)
# }
# plot_histograms(data_groups, x_label='Scores', y_label='Number of Observations', title='Score Distributions')