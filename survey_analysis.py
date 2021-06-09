import pandas as pd
import numpy as np
import re
import os
from os import path
import seaborn as sns
import matplotlib.pyplot as plt
import scipy as sp
import scipy.stats as st
import itertools as it
import statsmodels.api as sa
import statsmodels.formula.api as sfa
import scikit_posthocs as sp
from scipy.stats import f_oneway
from scipy.stats import wilcoxon
from scipy.stats import friedmanchisquare
from scipy.stats import chisquare, chi2

##

df = pd.read_csv("/home/stephen/survey_cleaned.csv")

##
# set up our quade test dataframe
quade = df[["Q6 Black bee is the best bee for my environment",
            "Q7 Black bee was already here",
            "Q8 Conservation of black bee"]]
quade.columns = ["Best for environment",
                 "Already here",
                 "Conservation"]

# drop NAs, goes from 342 rows to 293 rows
quade.dropna(inplace=True)
quade
##
#quade.plot.hist()
sns.histplot(quade)
##
environment =  quade["Best for environment"].tolist()
already = quade["Already here"].tolist()
conserve = quade["Conservation"].tolist()

f_oneway(environment, already, conserve)
##
# run quade test on the dataframe
sp.posthoc_quade(quade)
##
sp.posthoc_wilcoxon(quade, group_col="Best for environment", val_col="Already here")
##
quade
##
# friedman
df_fr = pd.read_csv("/home/stephen/friedmantest.csv")
df_fr.columns
df_fr.columns = ["Honey Production",
                 "Gentleness",
                 "Low Swarming",
                 "Brood Health",
                 "Varroa resistance",
                 "Calmness on Comb",
                 "Pure Race",
                 "Genetic Diversity"]
df_fr.dropna(inplace=True)

stat, p = friedmanchisquare(df_fr["Honey Production"],
                            df_fr["Gentleness"],
                            df_fr["Low Swarming"],
                            df_fr["Brood Health"],
                            df_fr["Varroa resistance"],
                            df_fr["Calmness on Comb"],
                            df_fr["Pure Race"],
                            df_fr["Genetic Diversity"])
stat, p

# get sum of each column add it to a new row called sum
df_fr.loc['sum']= df_fr.sum()

# square this row and add it to a new row called sum_sqr
df_fr.loc['sum_sqr'] = np.square(df_fr.loc["sum"])
df_fr.head()
#  the total of the usm row
total_sum = df_fr.loc["sum"].sum()

# find the minimum and maximum values
min_sum = df_fr.loc["sum"].min()
max_sum = df_fr.loc["sum"].max()

#get the total of the sum_sqr row
total_sum_sq = df_fr.loc["sum_sqr"].sum()
total_sum
min_sum
max_sum
total_sum_sq

# get the value of the expected sum
avg_expected_sum = total_sum/8

# get the expect total sum value and sum_sqr values
avg_expected_sum_total = avg_expected_sum * 8
avg_expected_sum_sqr = avg_expected_sum * avg_expected_sum
avg_expected_sum_sqr_total = avg_expected_sum_sqr * 8
avg_expected_sum_sqr_total

# rank the dataframe and drop the sum, sum_sqr rows
df_fr_ranked = df_fr.rank(axis=1, method='average',na_option='keep', ascending=True, pct=False)
df_fr_ranked = df_fr_ranked.drop(index="sum")
df_fr_ranked = df_fr_ranked.drop(index="sum_sqr")

# add a new sum row based on the sum of the ranks
df_fr_ranked.loc["sum"] = df_fr_ranked.sum()
df_fr_ranked.loc["sum"]

# absolute rank sum values

from math import comb
math.comb(1,2)

1+1
























# get the minimum and maximum value of this sum row
min_sum_ranks = df_fr_ranked.loc["sum"].min()
max_sum_ranks = df_fr_ranked.loc["sum"].max()

# get the value of the expected rank sum
sum_ranks = df_fr_ranked.loc["sum"].sum()/8
sum_ranks

# get the number of responders, take one away for the sum row
no_of_responders = len(df_fr_ranked['Genetic Diversity']) - 1
no_of_responders

df_fr_ranked.loc["sum_sqr"] = np.square(df_fr_ranked.loc["sum"])
sum_of_ranked_sqrs = df_fr_ranked.loc["sum_sqr"].sum()
sum_of_ranked_sqrs
##

part_1 = 12/(no_of_responders * 8 * (8+1))
part_1


part_2 = sum_of_ranked_sqrs
part_2


part_3 = 3*no_of_responders*(8+1)
part_3

ft = (part_1 * part_2) -part_3
ft

critical_value = chi2.ppf(.05, df=7)
critical_value

pvalue = (ft - 7)

##

