#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 13:11:20 2021

@author: stephen
"""

import pandas as pd
import numpy as np
import re
import os
from os import path
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image

pd.set_option('display.max_rows', 366)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

##
# %%
df = pd.read_csv("/home/stephen/Desktop/Honey_bee/survey_condensed.csv")
df.head()
headers = df.loc[0]
questions = ["Respondent ID",
             "Collectors_ID",
             "Q1 Years Beekeeping?",
             "Q2 Number of Colonies",
             "Q3 Hive type",
             "Q4 NIHBS member",
             "Q5 Keeps dark bees",
             "Q6 Black bee is the best bee for my environment",
             "Q7 Black bee was already here",
             "Q8 Conservation of black bee",
             "Q9 Other reason to keep black bee",
             "Q10 Queens mated in own apiary",
             "Q11 Queens mates in own area",
             "Q12 Queens mated at a mating station",
             "Q13 Queens bought from pure race breeder in Ireland",
             "Q14 Queens bought from a pure race breeder abroad",
             "Q15 Queens bought from other place",
             "Q16 Percentage of Varroa-related winter losses",
             "Q17 How often do you inspect your apiary for Varroa",
             "Q18 Do you keep a record of this treatment",
             "Q19 Varroa mortality, before treatment",
             "Q20 Varroa mortality, after treatment",
             "Q21 Varroa on bees",
             "Q22 Varroa in drone brood",
             "Q23 Varroa in worker brood",
             "Q24 Varroa reproduction",
             "Q25 Other Varroa inspections",
             "Q26 Hygienic behaviour (pin-test)",
             "Q27 Hygienic behaviour (other)",
             "Q28 Treats all colonies the same",
             "Q29 Never treats for Varroa (why?)",
             "Q30 Varroa treatment (I don't treat)",
             "Q31 Approved chemical treatments in spring/autumn",
             "Q32 Oxalic acid in winter",
             "Q33 oxalic acid and Queen caged",
             "Q34 Oxalic acid and nuc creation",
             "Q35 Removal of drone brood",
             "Q36 Removal of all brood",
             "Q37 Frequent nuc creation/requeening",
             "Q38 Other varroa treatment",
             "Q39 Practice swarm control",
             "Q40 Swarm control methods",
             "Q41 Should selection be carried out",
             "Q42 Honey production",
             "Q43 Gentleness",
             "Q44 Low swarming behaviour",
             "Q45 Brood health",
             "Q46 Varroa resistance",
             "Q47 Calmness on comb",
             "Q48 Pure race",
             "Q49 Genetic diversity",
             "Q50 Other important traits",
             "Q51 Is selection a way to find a solution to Varroa",
             "Q52 Other answers to selection question",
             "Q53 Keep own bees even if a resistant line was created",
             "Q54 Swap to new resistant line if they are better than own",
             "Q55 Swap to new resistant line even if the produce 25% less honey",
             "Q56 Swap to new resistant bees even if they produce 50% less honey",
             "Q57 Swap to new resistant bees even if they barely produce honey",
             "Q58 Swap to new resistant line even if they are more aggressive",
             "Q59 Swap to new resistant bees even if they swarm more",
             "Q60 Swap to new hybrid resistant line or keep own bees",
             "Q61 Swap to new varroa resistant foreign dark bees",
             "Q62 Proportion of breeding focus on Varroa",
             "Q63 Would test stock for varroa resistant genes",
             "Q64 Would not test stock for varroa resistant genes",
             "Q65 Should research work for long-term Varroa resistance",
             "Q66 Would be willing to participate in research",
             "Q67 Would not be willing to participate in research"]
##
df.columns = questions

# %%

df.columns
##
df.head()
##
# drop the now unneeded row that contains partial questions from surveymonkey
df = df.drop(0)
##
# check to see if this worked
df.head()
##
df["Respondent ID"].astype(int)
##
# get rid of anything other than digits in the
# how many years have you been a beekeeper and how many hives do you have
df.loc[:, "Q1 Years Beekeeping?"] = df.loc[:, "Q1 Years Beekeeping?"].astype(str).str.replace('\D+', '')
df.loc[:, "Q1 Years Beekeeping?"] = pd.to_numeric(df.loc[:, "Q1 Years Beekeeping?"])
df.loc[:, "Q2 Number of Colonies"] = df.loc[:, "Q2 Number of Colonies"].astype(str).str.replace('\D+', '')
df.loc[:, "Q2 Number of Colonies"] = pd.to_numeric(df.loc[:, "Q2 Number of Colonies"])
##

##
# turn all answers in the type of hives column lowercase
df.loc[:, "Q3 Hive type"] = df.loc[:, "Q3 Hive type"].str.lower()
hive_types = ["nat", "com", "lang", "rose", "top", "warre", "cdb", "swienty", "log"]

# create new columns based on the names of hives in the hive_types list
for i in hive_types:
    df[f'{i}_hives'] = df.loc[:, "Q3 Hive type"].str.extract(rf'({i})').replace(np.nan, '', regex=True)
##
# create a new column which contains all of the hive types that each respondent uses
df["all_hives"] = [' '.join([a, b, c, d, e, f, g, h, i]) for a, b, c, d, e, f, g, h, i in zip(df.loc[:, "nat_hives"],
                                                                                              df.loc[:, "com_hives"],
                                                                                              df.loc[:, "lang_hives"],
                                                                                              df.loc[:, "rose_hives"],
                                                                                              df.loc[:, "warre_hives"],
                                                                                              df.loc[:, "top_hives"],
                                                                                              df.loc[:, "cdb_hives"],
                                                                                              df.loc[:,
                                                                                              "swienty_hives"],
                                                                                              df.loc[:, "log_hives"])]
# remove any whitespace created during the previous join
df["all_hives"] = df["all_hives"].str.split().agg(" ".join)
##
# test summing a column of hive types
df["all_hives"].str.count("nat").sum()

##

# turn all answers lower case for Q4 and Q5
df.loc[:, "Q4 NIHBS member"] = df.loc[:, "Q4 NIHBS member"].str.lower()
df.loc[:, "Q5 Keeps dark bees"] = df.loc[:, "Q5 Keeps dark bees"].str.lower()

##
# replace all characters except numbers for questions 6, 7, 8
df.loc[:, "Q6 Black bee is the best bee for my environment"] = \
    df.loc[:, "Q6 Black bee is the best bee for my environment"].astype(str).str.replace(r'\D+', '')
df.loc[:, "Q6 Black bee is the best bee for my environment"] = \
    pd.to_numeric(df.loc[:, "Q6 Black bee is the best bee for my environment"])

df.loc[:, "Q7 Black bee was already here"] = \
    df.loc[:, "Q7 Black bee was already here"].astype(str).str.replace(r'\D+', '')
df.loc[:, "Q7 Black bee was already here"] = pd.to_numeric(df.loc[:, "Q7 Black bee was already here"])

df.loc[:, "Q8 Conservation of black bee"] = \
    df.loc[:, "Q8 Conservation of black bee"].astype(str).str.replace(r'\D+', '')
df.loc[:, "Q8 Conservation of black bee"] = pd.to_numeric(df.loc[:, "Q8 Conservation of black bee"])

##
df.loc[:, "Q9 Other reason to keep black bee"] = df.loc[:, "Q9 Other reason to keep black bee"].str.lower()

##
# Q10-14 no change needed
##

# Q15 make all lower case.
df.loc[:, "Q15 Queens bought from other place"] = df.loc[:, "Q15 Queens bought from other place"].str.lower()
##


##
# Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24 no changes needed
##
# Q25 make all responses lowercase
df.loc[:, "Q25 Other Varroa inspections"] = df.loc[:, "Q25 Other Varroa inspections"].str.lower()
##
# Q26, Q27, Q28 no changes needed
##
# Q29 make all responses lowercase
df.loc[:, "Q29 Never treats for Varroa (why?)"] = df.loc[:, "Q29 Never treats for Varroa (why?)"].str.lower()
##
# Qs 30, 31, 32, 33, 34, 35, 36, 37 no changes needed

##

dont_treat_df = df.loc[(df["Q30 Varroa treatment (I don't treat)"]=="I don't treat") &
                       (df["Q1 Years Beekeeping?"].astype(float) > 5) &
                       (df["Q2 Number of Colonies"] > 10) &
                       (df["Q66 Would be willing to participate in research"]=="Yes")]
dont_treat_df["Respondent ID"] = dont_treat_df["Respondent ID"].astype(int)
dont_treat_df.to_csv("/home/stephen/dont_treat.csv", index=False, sep=",")

do_treat_df = df.loc[(df["Q30 Varroa treatment (I don't treat)"].isnull()) &
                       (df["Q1 Years Beekeeping?"].astype(float) > 5) &
                       (df["Q2 Number of Colonies"] > 10) &
                       (df["Q66 Would be willing to participate in research"]=="Yes")]
do_treat_df["Respondent ID"] = do_treat_df["Respondent ID"].astype(int)
do_treat_df.to_csv("/home/stephen/do_treat.csv", index=False, sep=",")



##
# Q38 make all responses lowercase
df.loc[:, "Q38 Other varroa treatment"] = df.loc[:, "Q38 Other varroa treatment"].str.lower()
##
# Q39 no changes needed.

##
# Q 40 make all responses lowercase
df.loc[:, "Q40 Swarm control methods"] = df.loc[:, "Q40 Swarm control methods"].str.lower()
##
# Q 41 no changes needed
##
# Q 42 43 44 45 46 47 48 49 remove all characters except digits
df.loc[:, "Q42 Honey production"] = df.loc[:, "Q42 Honey production"].astype(str).str.replace(r'\D+', '')
df.loc[:, "Q42 Honey production"] = pd.to_numeric(df.loc[:, "Q42 Honey production"])

df.loc[:, "Q43 Gentleness"] = df.loc[:, "Q43 Gentleness"].astype(str).str.replace(r'\D+', '')
df.loc[:, "Q43 Gentleness"] = pd.to_numeric(df.loc[:, "Q43 Gentleness"])

df.loc[:, "Q44 Low swarming behaviour"] = df.loc[:, "Q44 Low swarming behaviour"].astype(str).str.replace(r'\D+', '')
df.loc[:, "Q44 Low swarming behaviour"] = pd.to_numeric(df.loc[:, "Q44 Low swarming behaviour"])

df.loc[:, "Q45 Brood health"] = df.loc[:, "Q45 Brood health"].astype(str).str.replace(r'\D+', '')
df.loc[:, "Q45 Brood health"] = pd.to_numeric(df.loc[:, "Q45 Brood health"])

df.loc[:, "Q46 Varroa resistance"] = df.loc[:, "Q46 Varroa resistance"].astype(str).str.replace(r'\D+', '')
df.loc[:, "Q46 Varroa resistance"] = pd.to_numeric(df.loc[:, "Q46 Varroa resistance"])

df.loc[:, "Q47 Calmness on comb"] = df.loc[:, "Q47 Calmness on comb"].astype(str).str.replace(r'\D+', '')
df.loc[:, "Q47 Calmness on comb"] = pd.to_numeric(df.loc[:, "Q47 Calmness on comb"])

df.loc[:, "Q48 Pure race"] = df.loc[:, "Q48 Pure race"].astype(str).str.replace(r'\D+', '')
df.loc[:, "Q48 Pure race"] = pd.to_numeric(df.loc[:, "Q48 Pure race"])

df.loc[:, "Q49 Genetic diversity"] = df.loc[:, "Q49 Genetic diversity"].astype(str).str.replace(r'\D+', '')
df.loc[:, "Q49 Genetic diversity"] = pd.to_numeric(df.loc[:, "Q49 Genetic diversity"])
##
df.to_csv("/home/stephen/friedmantest.csv", columns=["Q42 Honey production",
                                                     "Q43 Gentleness",
                                                     "Q44 Low swarming behaviour",
                                                     "Q45 Brood health",
                                                     "Q46 Varroa resistance",
                                                     "Q47 Calmness on comb",
                                                     "Q48 Pure race",
                                                     "Q49 Genetic diversity", ], index=False)

##
# Q 50 make all responses lowercase
##
df.loc[:, "Q50 Other important traits"] = df.loc[:, "Q50 Other important traits"].str.lower()
##
# Q51 no changes needed
##
# Q52 make all responses lowercase
df.loc[:, "Q52 Other answers to selection question"] = df.loc[:, "Q52 Other answers to selection question"].str.lower()
##
# Q53, 54, 55, 56, 57, 58, 59, 60, 61, 62 no changes needed
##




##
# Q 63 64 make all responses lowercase
df.loc[:, "Q63 Would test stock for varroa resistant genes"] = \
    df.loc[:, "Q63 Would test stock for varroa resistant genes"].str.lower()
df.loc[:, "Q64 Would not test stock for varroa resistant genes"] = \
    df.loc[:, "Q64 Would not test stock for varroa resistant genes"].str.lower()
##
# Q65, 66 no changes needed
##
# Q 67 make all responses lowercase
df.loc[:, "Q67 Would not be willing to participate in research"] = \
    df.loc[:, "Q67 Would not be willing to participate in research"].str.lower()
##
# write cleaned data to a new file
df.to_csv("/home/stephen/survey_cleaned.csv", index=False, sep=",")
# Friedman test on questions 6, 7, 8
# Null hypothesis: No main reason to keep black bee
# Alternative hypothesis: One reason is more important than the others
# k = 3

# Possibly do quade test instead?



##
df.describe(include="all")

##

##
# figure out the year ranges of respondents

##

