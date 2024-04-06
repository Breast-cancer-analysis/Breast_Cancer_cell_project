import pandas as pd
from functions.FOV_cell import Cellline
from functions.FOV_cell import FOV
from functions.FOV_cell import cell
import os

# 设置显示的最大行数，None表示不限制行数
pd.set_option('display.max_rows', None)

# 设置显示的最大列数，None表示不限制列数
pd.set_option('display.max_columns', None)

# 设置列宽，以避免被截断，None表示自动决定显示宽度
pd.set_option('display.max_colwidth', None)

# 设置显示的宽度，以避免换行，None表示自动决定显示宽度
pd.set_option('display.width', None)


bin_sizes = [1,10]
print(bin_sizes)
cell_line = ['10_none', '468', '47', '453', '159', '231', '51','wm', '10', '474']

path_name_2 = '/Users/ruihongyu/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Year_3/Y3_project/csv_PCC/'

for i in cell_line:
    # create a folder to store csv file about pccs
    folder_name = str(i)
    folder_path = os.path.join(path_name_2, folder_name)
    os.makedirs(folder_path)
    # create a cell line object
    cell_line = Cellline('/Users/ruihongyu/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Year_3/Y3_project/'+str(i), bin_sizes)
    cell_line.calculate_all_PCCs()
    for j in cell_line.FOVs:
        print(j.name)
        j.table.to_csv('/Users/ruihongyu/Library/CloudStorage/OneDrive-ImperialCollegeLondon/Year_3/Y3_project/csv_PCC/' + 
                       folder_name +'/' + j.name + '.csv', index= False)
        