from scipy.stats import kruskal
from functions.FOV_cell import get_all_filenames
import pickle
import numpy as np
from functions.plot_histogram import plot_histograms
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from sklearn.utils import resample
import scikit_posthocs as sp
from statsmodels.stats.multitest import multipletests
from scipy.stats import ttest_ind
import random
from functions.FOV_cell import plot_kde_from_dict

take_mean = True # if we are going to take mean for each FOV

groups = [231,'wm','MCF10A_TGFB','468', 'MCF10A', 'SUM159', 'T47D', 'BT474', 'Cal51' ,'453']
bin_width = [1]
variable = {}
last_result = pd.DataFrame()

for z in bin_width:
    for i in groups:
        temp = []
        data = pd.read_csv('../sttc_values/'+str(i)+'_sttc.csv')
        data = data.iloc[:, 2].tolist() # load each FOV's PCC

        variable[str(i)] = data

    if take_mean == False:
        #did not take a mean, so do KW test, first
        stat, p = kruskal(variable['231'],variable['wm'], variable['MCF10A_TGFB'], variable['468'])
        print('Kruskal-Wallis H statistic:', stat)
        print('p-value:', p)
        alpha = 0.05  
        if p < alpha:
            print(' Reject')
        else:
            print('Not reject')

        # do a post-hoc after KW test
        if p < 0.05:
            # dictonary to DataFrame，for posthoc_dunn
            data = []
            for key, values in variable.items():
                for value in values:
                    data.append([key, value])
            df = pd.DataFrame(data, columns=['Group', 'Value'])
    
            # conduct Dunn test as Post-hoc test
            
            ph_result = sp.posthoc_dunn(df, val_col='Value', group_col='Group', p_adjust='holm')
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            binary_result_df = ph_result.applymap(lambda x: 1 if x < 0.05 else 0)
            print(binary_result_df)

            # check whether the result change compare with last time length
            if last_result.equals(binary_result_df):
                print('no change')
            else:
                print('something changed')

            last_result = binary_result_df
            
            #print(ph_result)


    if take_mean == True:
        #take a mean, so do ANOVA test
        updated_dict = {k: [sum(random.choices(v, k=3)) / 3 for _ in range(len(v))] for k, v in variable.items()}
        df = pd.DataFrame([(key, var) for key, vals in updated_dict.items() for var in vals],
                    columns=['Group', 'Value'])
        

        # ols model？？
        model = ols('Value ~ C(Group)', data=df).fit()

        anova_results = sm.stats.anova_lm(model, typ=1)

        print(anova_results)

        print('\n')
        # post-hoc for the ANOVA
        data = []
        for key, values in variable.items():
            for value in values:
                data.append([key, value])
        df = pd.DataFrame(data, columns=['Group', 'Value'])

        groups = df['Group'].unique()
        comparisons = [(groups[i], groups[j]) for i in range(len(groups)) for j in range(i+1, len(groups))]

        p_values = []
        stats = []
        for group1, group2 in comparisons:
            data1 = df[df['Group'] == group1]['Value']
            data2 = df[df['Group'] == group2]['Value']
            stat, p = ttest_ind(data1, data2)
            p_values.append(p)
            stats.append(stat)


        reject, pvals_corrected, _, alpha_corrected = multipletests(p_values, alpha=0.05, method='bonferroni')

        for z in range(len(comparisons)):
            print(comparisons[z])
            print(stats[z])
            print('Reject null hypothesis:', reject[z])
            print('\n')

        print('Corrected p-values:', pvals_corrected)

    plot_histograms(variable)
    plot_kde_from_dict(variable, xlim=[-0.2, 0.4])
