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
from statsmodels.nonparametric.kde import KDEUnivariate

take_mean = True # if we are going to take mean for each FOV

groups = [231,'wm','MCF10A_TGFB']
bin_width = [10]
variable = {}
last_result = pd.DataFrame()

for z in bin_width:
    for i in groups:
        temp = []
        data = pd.read_csv('../sttc_values/'+str(i)+'_sttc.csv')
        data = data.iloc[:, 2].tolist() # load each FOV's PCC

        variable[str(i)] = data


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

        print(comparisons)
        print(len(comparisons))
        print(stats)
        print('Reject null hypothesis:', reject)
        print('Corrected p-values:', pvals_corrected)

        print('\n \n')

    plot_histograms(variable)
