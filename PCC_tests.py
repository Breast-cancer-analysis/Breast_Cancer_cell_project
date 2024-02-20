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


take_mean = True # if we are going to take mean for each FOV

group = [231, 453, 474, 51, 159, 10, 47, 468]
bin_width = [1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100]
variable = {}
last_result = pd.DataFrame()

for z in bin_width:
    for i in group:
        all_file = get_all_filenames('../result/'+str(i)+'/bin_width_'+str(z)+'/')
        temp = []
        for j in all_file:
            with open(j,'rb') as file:
                data = pickle.load(file)
            data = data.tolist()
            if take_mean == True and len(data) != 0:
                temp.append(data)
            elif take_mean == False and len != 0:
                temp.append(data)
            elif take_mean == True and len(data) == 0:
                continue

        if take_mean == False:
            variable[str(i)] = [item for sublist in temp for item in sublist]
        else:
            variable[str(i)] = [item for sublist in temp for item in sublist]



    if take_mean == False:
        #did not take a mean, so do KW test, first
        stat, p = kruskal(variable['231'], variable['453'] ,variable['474'], variable['51'], variable['159'],variable['10'],variable['47'],variable['468'])
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

    elif take_mean == True:
        #take a mean, so do ANOVA test
        updated_dict = {k: resample(v, replace=True, n_samples=len(data), random_state=1) for k, v in variable.items()}
        df = pd.DataFrame([(key, var) for key, vals in variable.items() for var in vals],
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
        for group1, group2 in comparisons:
            data1 = df[df['Group'] == group1]['Value']
            data2 = df[df['Group'] == group2]['Value']
            stat, p = ttest_ind(data1, data2)
            p_values.append(p)


        reject, pvals_corrected, _, alpha_corrected = multipletests(p_values, alpha=0.05, method='bonferroni')

        print(comparisons)
        print(len(comparisons))
        print('Reject null hypothesis:', reject)
        print('Corrected p-values:', pvals_corrected)

        print('\n \n')

    plot_histograms(variable)
