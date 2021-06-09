import pandas as pd
import numpy as np
import re
import os
from os import path
import seaborn as sns
# from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.patheffects as path_effects
import matplotlib.gridspec as gridspec

##


def change_width(axes, new_value):
    for patch in axes.patches:
        current_width = patch.get_width()
        diff = current_width - new_value

        # we change the bar width
        patch.set_width(new_value)

        # we recenter the bar
        patch.set_x(patch.get_x() + diff * .5)
##


df = pd.read_csv("/home/stephen/survey_cleaned.csv")
##
for_y = df.loc[(df["Q2 Number of Colonies"] < 100) & (df["Q1 Years Beekeeping?"] < 70)]
fig = sns.regplot(x=for_y["Q1 Years Beekeeping?"],
                  y=for_y["Q2 Number of Colonies"],
                  robust=True, ci=None, scatter_kws={"s": 3, "color": "navy"},
                  line_kws={"color": "pink"})
plt.xlim(0, 61)
plt.title("Relationship between years beekeeping and colonies owned", fontsize=12)
sns.despine()
plt.xlabel("Years Beekeeping", fontsize=10)
plt.ylabel("Number of colonies", fontsize=10)
plt.tight_layout()
# plt.show(fig)
plt.savefig("/home/stephen/Desktop/survey_plots/years_and_colonies.png", bbox_inches="tight", dpi=200)
# plt.close()
##
# Years beekeeping
years = df.loc[:, "Q1 Years Beekeeping?"].dropna()
years_bins = [1, 2, 3, 4, 5, 10, 20, 30, 40, 50, 60]
years_labels = ["0-1", "2-3", "4-5", "6-10", "10-19", "20-29", "30-39", "40-49", "50-59", "60+"]
years["years_range"] = pd.cut(years, years_bins, labels=years_labels, include_lowest=True)
print(years["years_range"])
years["years_range"].hist()
df.loc[:, "Years Range"] = years["years_range"]
df.loc[:, "Years Range"].value_counts()

##
# Hive type
hive_types = ["nat", "com", "lang", "rose", "top", "cdb", "warre",  "log"]
df["all_hives"].str.count("swienty").sum()

hive_sums = []
for i in hive_types:
    hive_sums.append(df["all_hives"].str.count(f'{i}').sum())

hive_types2 = ["National", "Commercial", "Langstroth", "Rose", "Top-Bar", "CDB", "Warre", "Log"]
fig = sns.barplot(hive_types2, hive_sums, palette="muted", edgecolor="k", linewidth=0.8)

for p in fig.patches:
    fig.annotate(format(p.get_height(), '.0f'),
                 (p.get_x() + p.get_width() / 2.,
                  p.get_height()),
                 ha="center", va="center",
                 xytext=(0, 9),
                 textcoords="offset points")
plt.title("Hive types used by Beekeepers in Ireland")
plt.xlabel("Hive Types")
plt.xticks(rotation=25, fontsize=9)
plt.ylabel("Count")
plt.ylim((0, 265))
plt.tight_layout()
sns.despine()
plt.show()
plt.savefig("/home/stephen/Desktop/survey_plots/Hive_types.png", bbox_inches="tight", dpi=200)
# df["all_hives"]
# plt.close()

##
# NIHBS member
nihbs = df["Q4 NIHBS member"].value_counts()
percent_nihbs = nihbs[1] / (nihbs[0] + nihbs[1]) * 100

##
total = float(len(df))
fig = sns.countplot(x="Q4 NIHBS member", data=df, palette="deep", edgecolor="k", linewidth=0.8)
plt.title('NIHBS membership', fontsize=16)
for p in fig.patches:
    percentage = '{:.1f}'.format(p.get_height())
    x = p.get_x() + .40
    y = p.get_height()+3
    fig.annotate(percentage, (x, y), ha='center')
plt.xlabel("Member of NIHBS?")
plt.ylim(0, 210)
change_width(fig, .45)
sns.despine()
plt.ylabel("Count")
# plt.show()
plt.savefig("/home/stephen/Desktop/survey_plots/NIHBS_member_countplot.png", bbox_inches="tight", dpi=200)
# plt.close()
##
# Keep black bee?
black_bee = df["Q5 Keeps dark bees"].value_counts()
perc_black = black_bee[0] / (black_bee[0] + black_bee[1] + black_bee[2]) * 100
perc_dont_know = black_bee[2] / (black_bee[0] + black_bee[1] + black_bee[2]) * 100
df["Q5 Keeps dark bees"].value_counts()
fig = sns.countplot(x="Q5 Keeps dark bees", data=df, palette="muted", edgecolor="k", linewidth=0.8)
for p in fig.patches:
    fig.annotate(format(p.get_height(), '.1f'),
                 (p.get_x() + p.get_width() / 2.,
                  p.get_height()),
                 ha="center", va="center",
                 xytext=(0, 9),
                 textcoords="offset points")
plt.ylim(0, 341)
plt.title("Number of Beekeepers keeping black bees")
sns.despine()
plt.ylabel("Count")
plt.xlabel("Do you keep native black bees?")
# plt.show()
plt.savefig("/home/stephen/Desktop/survey_plots/keep_black_bee_countplot_number.png", bbox_inches="tight", dpi=200)
# plt.close()
##
total = float(len(df))
fig = sns.countplot(x="Q5 Keeps dark bees", data=df, palette="muted", edgecolor="k", linewidth=0.8)
plt.title('Percentage of people keeping Dark Bees', fontsize=14)

for p in fig.patches:
    percentage = '{:.1f}%'.format(100 * p.get_height()/total)
    x = p.get_x() + .45
    y = p.get_height()+3
    fig.annotate(percentage, (x, y), ha='center')
plt.xlabel("Keeps Black Bees?")
sns.despine()
plt.ylabel("Count")
plt.xlabel("Do you keep native black bees?")
# plt.show()
plt.savefig("/home/stephen/Desktop/survey_plots/keep_black_bee_countplot_percentage.png", bbox_inches="tight", dpi=200)
# plt.close()

##

keep_black_df = df[["Q6 Black bee is the best bee for my environment", "Q7 Black bee was already here",
                    "Q8 Conservation of black bee"]]
keep_black_df.columns = ["Best for my environment", "Was already here", "Conservation"]
keep_black_df.dropna(inplace=True)
keep_black_df["id"] = keep_black_df.index
keep_black_long = pd.melt(keep_black_df, id_vars="id")
grouped_keep_black_df = keep_black_long.groupby(["variable"], as_index=False)["value"].sum()
grouped_keep_black_df.columns = ["Trait", "Score"]
grouped_keep_black_df["Score"] = grouped_keep_black_df["Score"] / len(df["Respondent ID"] * 100)
fig = sns.barplot(x=grouped_keep_black_df.Trait, y=grouped_keep_black_df.Score,
                  palette="deep", edgecolor="k", linewidth=0.8)
for p in fig.patches:
    fig.annotate(format(p.get_height(), '.1f'),
                 (p.get_x() + p.get_width() / 2.,
                  p.get_height()),
                 ha="center", va="center",
                 xytext=(0, 9),
                 textcoords="offset points")
plt.xticks(fontsize=8)
plt.ylim(0, 5)
plt.xlabel("Honeybee Traits", fontsize=13)
plt.title("Why do beekeepers keep the Black Bee?")
plt.tight_layout()
sns.despine()
# plt.show()
plt.savefig("/home/stephen/Desktop/survey_plots/keep_black_why.png", bbox_inches="tight", dpi=200)
# plt.close()
##
fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(12, 5), dpi=100)
fig.subplots_adjust(wspace=.6)
bbox_props = dict(boxstyle="square,pad=0.2", fc="w", ec="k", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-"), bbox=bbox_props, zorder=0, va="center")
df1 = df['Q6 Black bee is the best bee for my environment'].dropna()
df1.columns = ["selection"]
df_1 = df1.value_counts().reset_index().rename(columns={"index": "Response",
                                                                 'Q6 Black bee is the best bee for my environment':
                                                                     "Number of beekeepers"})
df_1.sort_values(by=['Number of beekeepers'], ascending=True, inplace=True)
sizes_ax1 = df_1["Number of beekeepers"].to_list()
labels = ["1", "2", "3", "4", "5"]
wedges_1, texts_1, pcts_1 = ax1.pie(sizes_ax1, wedgeprops={'width': .5, 'edgecolor': 'white'},
                                    startangle=-25, autopct='%.1f%%', pctdistance=.85,
                                    colors=["tan", "slategrey", "goldenrod", "indianred", "seagreen"])

for i, p in enumerate(wedges_1):
    ang = (p.theta2 - p.theta1)/2 + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax1.annotate(labels[i], xy=(x, y), xytext=(1.1*np.sign(x), 1.1*y),
                 horizontalalignment=horizontalalignment, **kw)
plt.setp(pcts_1, color="white", fontsize=7.5, bbox=dict(boxstyle="round4", facecolor="#445A64"))
ax1.set_title("Black bee is the best bee\nfor my environment")

df2 = df['Q7 Black bee was already here'].dropna()
df2.columns = ["selection"]
df_2 = df2.value_counts().reset_index().rename(columns={"index": "Response",
                                                                 'Q7 Black bee was already here':
                                                                     "Number of beekeepers"})
df_2.sort_values(by=['Number of beekeepers'], ascending=True, inplace=True)
sizes_ax2 = df_2["Number of beekeepers"].to_list()
labels = ["1", "2", "3", "4", "5"]
wedges_2, texts_2, pcts_2 = ax2.pie(sizes_ax2, wedgeprops={'width': .5, 'edgecolor': 'white'},
                                    startangle=-72, autopct='%.1f%%', pctdistance=.85,
                                    colors=["tan", "slategrey", "goldenrod", "indianred", "seagreen"])

for i, p in enumerate(wedges_2):
    ang = (p.theta2 - p.theta1)/2 + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax2.annotate(labels[i], xy=(x, y), xytext=(1.1*np.sign(x), 1.1*y),
                 horizontalalignment=horizontalalignment, **kw)
plt.setp(pcts_2, color="white", fontsize=7.5, bbox=dict(boxstyle="round4", facecolor="#445A64"))
ax2.set_title("Black bee was already in my area")
ax2.axvline(linewidth=1, color="k", x=-1.23)

df3 = df['Q8 Conservation of black bee'].dropna()
df3.columns = ["selection"]
df_3 = df3.value_counts().reset_index().rename(columns={"index": "Response",
                                                                 'Q8 Conservation of black bee':
                                                                     "Number of beekeepers"})
df_3.sort_values(by=['Number of beekeepers'], ascending=True, inplace=True)
sizes_ax3 = df_3["Number of beekeepers"].to_list()
labels = ["1", "2", "3", "4", "5"]
wedges_3, texts_3, pcts_3 = ax3.pie(sizes_ax3, wedgeprops={'width': .5, 'edgecolor': 'white'},
                                    startangle=20, autopct='%.1f%%', pctdistance=.85,
                                    colors=["tan", "slategrey", "goldenrod", "indianred", "seagreen"])

for i, p in enumerate(wedges_3):
    ang = (p.theta2 - p.theta1)/2 + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax3.annotate(labels[i], xy=(x, y), xytext=(1.1*np.sign(x), 1.27*y),
                 horizontalalignment=horizontalalignment, **kw)
plt.setp(pcts_3, color="white", fontsize=7.5, bbox=dict(boxstyle="round4", facecolor="#445A64"))
ax3.set_title("Conservation of the black bee")
ax3.axvline(linewidth=1, color="k", x=-1.23)


plt.suptitle("Why do beekeepers choose to keep the black bee?", fontsize=18, y=1)
plt.tight_layout()
plt.savefig("/home/stephen/Desktop/survey_plots/why_choose_black_bee.png", dpi=150)
plt.show()

##
df_queen_origin = df[["Q10 Queens mated in own apiary",
                      "Q11 Queens mates in own area",
                      "Q12 Queens mated at a mating station",
                      "Q13 Queens bought from pure race breeder in Ireland",
                      "Q14 Queens bought from a pure race breeder abroad",
                      "Q15 Queens bought from other place"]]
df_queen_origin.columns = ("Own apiary",
                           "Own area",
                           "Mating station",
                           "Irish pure race breeder",
                           "Foreign pure race breeder",
                           "Bought from elsewhere")
origin_count = df_queen_origin.count().reset_index().rename(columns={"index": "Origin", 0: "Number of beekeepers"})
yy = origin_count["Number of beekeepers"]
fig = sns.barplot(y=origin_count["Origin"],
                  x=origin_count["Number of beekeepers"],
                  palette="muted", edgecolor="k", linewidth=0.8)

for index, data in enumerate(yy):
    plt.text(data + 3, index + .1, str(data), color="black", fontsize=8)
plt.tight_layout(pad=1.5)
plt.ylabel("Origin", fontsize=10)
plt.tick_params(axis="y", which='major', labelsize=9)
plt.title("Origin of Queens in Irish apiaries")
sns.despine()

plt.savefig("/home/stephen/Desktop/survey_plots/origins.png", bbox_inches="tight", dpi=200)
# plt.close()
##
varroa_losses = df["Q16 Percentage of Varroa-related winter losses"]
varroa_losses.columns = ["losses"]
vdf = varroa_losses.value_counts().reset_index().rename(columns={"index": "Response",
                                                                 "Q16 Percentage of Varroa-related winter losses":
                                                                     "Number of beekeepers"})


vdf.sort_values(by=['Number of beekeepers'], ascending=True, inplace=True)
sizes = vdf["Number of beekeepers"].to_list()
fig, ax = plt.subplots(figsize=(10, 5), dpi=200)
labels1 = ["Serious problem \nevery year (frequent losses) [4]",
           "Things under control \nthrough treatments) [56]",
           "Occasional losses due \nto Varroa(10-20%/year) [75]",
           "Not a problem \n(~5% of losses/year) [185]",
           ]
wedges, texts, pcts = ax.pie(sizes, wedgeprops={'width': .5, 'edgecolor': 'white'},
                             startangle=-63, autopct='%.1f%%', pctdistance=.7,
                             colors=["olive", "royalblue", "seagreen", "indianred"])
bbox_props = dict(boxstyle="square,pad=0.2", fc="w", ec="k", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2 + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(labels1[i], xy=(x, y), xytext=(1.25*np.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment, **kw)

plt.setp(pcts, color="white", fontsize=9, bbox=dict(boxstyle="round4", facecolor="#445A64"))
plt.title("Varroa's impact on colony losses", fontsize=14, y=1)
plt.show()
plt.savefig("/home/stephen/Desktop/survey_plots/varroa_problem_donut.png", bbox_inches="tight", dpi=200)
##
often = df["Q17 How often do you inspect your apiary for Varroa"].copy().dropna()
total = float(len(often))
fig = sns.countplot(x="Q17 How often do you inspect your apiary for Varroa", data=df,
                    palette="muted", edgecolor="k", linewidth=0.8,
                    order=often.value_counts().index)
plt.title('How often do beekeepers carry\n out Varroa inspections', fontsize=13)

for p in fig.patches:
    percentage = '{:.1f}%'.format(100 * p.get_height()/total)
    x = p.get_x() + .45
    y = p.get_height()+3
    fig.annotate(percentage, (x, y), ha='center')

plt.xlabel("How often", fontsize=12)
locs, labels = plt.xticks()
plt.xticks(locs, ["Several times", "Once a year", "All year long", "Never", "After treatment"])
sns.despine()
plt.ylabel("Count", fontsize=12)
plt.show()
plt.savefig("/home/stephen/Desktop/survey_plots/how_often_inspection.png", bbox_inches="tight", dpi=200)

##
df_treatments = df[["Q31 Approved chemical treatments in spring/autumn",
                    "Q32 Oxalic acid in winter",
                    "Q33 oxalic acid and Queen caged",
                    "Q34 Oxalic acid and nuc creation",
                    "Q35 Removal of drone brood",
                    "Q36 Removal of all brood",
                    "Q37 Frequent nuc creation/requeening"]]
df_treatments.columns = ("Chemical treatments in spring/autumn",
                         "Oxalic acid (winter)",
                         "Oxalic acid and cage queen",
                         "Oxalic acid and create nuc",
                         "Remove drone brood",
                         "Remove all brood",
                         "Frequent nuc creation/re-queening")
treatment_count = df_treatments.count().reset_index().rename(columns={"index": "Treatment", 0: "Number of beekeepers"})
yy = treatment_count["Number of beekeepers"]

# treatment_count.plot.bar()
fig = sns.barplot(y=treatment_count["Treatment"],
                  x=treatment_count["Number of beekeepers"],
                  palette="muted", edgecolor="k", linewidth=0.8)

for index, data in enumerate(yy):
    plt.text(data + 3, index + .1, str(data), color="black", fontsize=8)
plt.title("Varroa treatment methods", fontsize=14)
fig.yaxis.set_tick_params(labelsize="small")
plt.xlabel("Count", fontsize=12)
plt.ylabel("Treatment", fontsize=12)
sns.despine()
plt.tight_layout()

plt.savefig("/home/stephen/Desktop/survey_plots/varroa_treatments.png", bbox_inches="tight", dpi=200)
plt.show()
# plt.close()
##

catplot_df = pd.read_csv("/home/stephen/friedmantest.csv")
catplot_df.dropna(inplace=True)
catplot_df.columns = ["Honey Production", "Gentleness", "Low Swarming Behaviour", "Brood Health", "Varroa Resistance",
                      "Calmness on Comb", "Pure Race", "Genetic Diversity"]
catplot_df["id"] = catplot_df.index
total = len(catplot_df)
catdf_long = pd.melt(catplot_df, id_vars="id")
grouped_df = catdf_long.groupby(["variable"], as_index=False)["value"].sum()
grouped_df.columns = ["Trait", "Score"]

grouped_df["Score"] = (grouped_df["Score"] / total)
grouped_df = grouped_df.sort_values(by="Score", ascending=False)
fig = sns.barplot(x=grouped_df.Trait, y=grouped_df.Score, palette="deep", edgecolor="k", linewidth=0.8)
for p in fig.patches:
    fig.annotate(format(p.get_height(), '.1f'),
                 (p.get_x() + p.get_width() / 2.,
                  p.get_height()),
                 ha="center", va="center",
                 xytext=(0, 9),
                 textcoords="offset points")
plt.xticks(rotation=20, horizontalalignment="right", fontsize=8)
plt.ylim(0, 5)
plt.ylabel("Average Score")
plt.xlabel("Honeybee Traits")
plt.title("Honeybee Trait Importance")
plt.tight_layout()
sns.despine()
# plt.show(fig)
plt.savefig("/home/stephen/Desktop/survey_plots/honeybee_traits.png", bbox_inches="tight", dpi=200)
# plt.close()

##
# trait importance boxplots

boxplot_df = pd.read_csv("/home/stephen/friedmantest.csv")
boxplot_df.columns = ["Honey Production", "Gentleness", "Low Swarming Behaviour", "Brood Health", "Varroa Resistance",
                      "Calmness on Comb", "Pure Race", "Genetic Diversity"]
boxplot_df = boxplot_df.dropna()
boxplot_df["id"] = boxplot_df.index
boxdf_long = pd.melt(boxplot_df, id_vars="id")

fig = sns.boxplot(x=boxdf_long.variable, y=boxdf_long.value, data=boxdf_long, palette="muted", linewidth=0.75)
ax = fig.axes


def add_median_labels(axes):
    lines = axes.get_lines()
    # determine number of lines per box (this varies with/without fliers)
    boxes = [c for c in axes.get_children() if type(c).__name__ == 'PathPatch']
    lines_per_box = int(len(lines) / len(boxes))
    # iterate over median lines
    for median in lines[4:len(lines):lines_per_box]:
        # display median value at center of median line
        x, y = (data.mean() for data in median.get_data())
        # choose value depending on horizontal or vertical plot orientation
        value = x if (median.get_xdata()[1]-median.get_xdata()[0]) == 0 else y
        text = axes.text(x, y, f'{value:.1f}', ha='center', va='center',
                         fontweight='bold', size=7, color='white', bbox=dict(boxstyle="round4", facecolor="#445A64"))
        # create median-colored border around white text for contrast
        text.set_path_effects([
            path_effects.Stroke(linewidth=3, foreground=median.get_color()),
            path_effects.Normal(),
        ])


plt.xticks(rotation=20, horizontalalignment="right", fontsize=8)
plt.ylim(1, 5.3)
plt.xlabel("Traits", fontsize=13)
plt.ylabel("Score", fontsize=13)
plt.title("Honeybee Trait Importance")
# plt.tight_layout()
fig.figure.tight_layout()
sns.despine()
add_median_labels(fig.axes)
# plt.show(fig)

plt.savefig("/home/stephen/Desktop/survey_plots/honeybee_traits_boxplot_colours.png", bbox_inches="tight", dpi=200)
plt.close()

##

swap_df = df[["Q53 Keep own bees even if a resistant line was created"]]

swap_df = swap_df.rename(columns={"Q53 Keep own bees even if a resistant line was created":
                                  "Keep own bees even if a resistant line was created"})
swap_df = swap_df.replace(np.nan, "Yes")
swap_df = swap_df.replace("My own bees as before, without change", "No")
swap_df = swap_df.value_counts().to_frame().reset_index()
swap_df.columns = ("Answer", "Count")

fig = sns.barplot(x=swap_df.Answer, y=swap_df.Count, palette="muted", edgecolor="k", linewidth=0.8)
for p in fig.patches:
    fig.annotate(format(p.get_height(), '.1f'),
                 (p.get_x() + p.get_width() / 2.,
                  p.get_height()-4),
                 ha="center", va="center",
                 xytext=(0, 9), color="black", size=9,
                 textcoords="offset points")

plt.xlabel("Answer", fontsize=11)
plt.ylabel("Count", fontsize=11)
plt.title("Would you swap to a Varroa resistant line of bees?", y=1.02)
plt.tight_layout()
change_width(fig, .45)
sns.despine()
# plt.show(fig)
plt.savefig("/home/stephen/Desktop/survey_plots/swap_bee_lines.png", bbox_inches="tight", dpi=200)
# plt.close()
##

varroa_focus = df["Q62 Proportion of breeding focus on Varroa"]
varroa_focus.replace("50% Varroa resistance, 50% other characteristics (honey production, gentleness etc.)",
                     "50% Varroa resistance, 50% other", inplace=True)
varroa_focus.replace("20% Varroa resistance, 80% other characteristics (honey production, gentleness etc.)",
                     "20% Varroa resistance, 80% other", inplace=True)

varroa_focus = varroa_focus.value_counts().to_frame().reset_index().rename(
    columns={"index": "Answers", "Q62 Proportion of breeding focus on Varroa": "Number of beekeepers"})

varroa_focus.sort_values(by=['Number of beekeepers'], ascending=True, inplace=True)
sizes = varroa_focus["Number of beekeepers"].to_list()

fig, ax = plt.subplots(figsize=(10, 5), dpi=200)

labels1 = ['100% Varroa resistance', '20% Varroa resistance,\n80% other', '50% Varroa resistance,\n50% other']

wedges, texts, pcts = ax.pie(sizes,
                             wedgeprops={'width': 0.5, 'edgecolor': 'white'},
                             startangle=-63, autopct='%.1f%%', pctdistance=.7,
                             colors=["royalblue", "seagreen", "indianred"]
                             )

bbox_props = dict(boxstyle="square,pad=0.2", fc="w", ec="k", lw=0.72)

kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2 + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(labels1[i] + " [" + str(sizes[i]) + "]", xy=(x, y), xytext=(1.25*np.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment, **kw)

plt.setp(pcts, color="white", fontsize=9, bbox=dict(boxstyle="round4", facecolor="#445A64"))

plt.title("Beekeepers opinions on Varroa research", fontsize=14)
plt.savefig("/home/stephen/Desktop/survey_plots/varroa_opinions.png", bbox_inches="tight", dpi=200)
##
##
# Word clouds to get a picture of what is being said in the open ended answers
plt.figure()
why_keep_dark_bees_word_cloud_text = df.loc[:, "Q9 Other reason to keep black bee"].replace(np.nan, '')
bee_mask = np.array(Image.open("/home/stephen/Desktop/honeybeemask.png"))
stop_words = ["got"] + list(STOPWORDS)
why_keep_dark_bees_word_cloud = WordCloud(background_color="white", max_words=40, mask=bee_mask,
                                          stopwords=stop_words,
                                          contour_width=3, contour_color="black")
why_keep_dark_bees_word_cloud.generate(' '.join(why_keep_dark_bees_word_cloud_text))
plt.imshow(why_keep_dark_bees_word_cloud, interpolation="bilinear")
plt.axis("off")
plt.title("Reasons beekeepers keep the black bee")
plt.savefig("/home/stephen/Desktop/survey_plots/wordcloud_keepnativebee.png", bbox_inches="tight", dpi=200)
##
##
plt.figure()
Other_important_traits_text = df.loc[:, "Q50 Other important traits"].replace(np.nan, '')
Other_important_traits_word_cloud = WordCloud().generate(' '.join(Other_important_traits_text))
plt.imshow(Other_important_traits_word_cloud)
plt.axis("off")
plt.show()
##
plt.figure()
would_not_test_text = df.loc[:, "Q64 Would not test stock for varroa resistant genes"].replace(np.nan, '')
Would_not_test_word_cloud = WordCloud().generate(' '.join(would_not_test_text))
plt.imshow(Would_not_test_word_cloud)
plt.axis("off")
plt.show()
##
plt.figure()
not_willing_research_text = df.loc[:, "Q67 Would not be willing to participate in research"].replace(np.nan, '')
not_willing_research_word_cloud = WordCloud().generate(' '.join(not_willing_research_text))
plt.imshow(not_willing_research_word_cloud)
plt.axis("off")
plt.show()

##
# figure out the hive number ranges of respondents
hives = df.loc[:, ["Q2 Number of Colonies"]]

hive_bins = [1, 3, 5, 10, 30, 60, 75, 100, 150, 250, 1000]
hive_labels = ["1-2", "3-5", "6-10", "11-30", "31-60", "61-75", "76-100", "101-150", "150-250", "250-1000"]
hives["hives_range"] = pd.cut(hives.loc[:, "Q2 Number of Colonies"], hive_bins, labels=hive_labels, include_lowest=True)
print(hives["hives_range"])

df.loc[:, "Hives Range"] = hives["hives_range"]
df.loc[:, "Hives Range"].value_counts()
hives.sort_values("Q2 Number of Colonies", inplace=True)


hives_grouped_df = hives.groupby(["hives_range"], as_index=False).count()

fig = sns.barplot(x=hives_grouped_df["hives_range"], y=hives_grouped_df["Q2 Number of Colonies"], palette="deep",
                  edgecolor="k", linewidth=0.8)
plt.title("Number of colonies kept by beekeepers")
plt.xlabel("Range of colonies")
plt.xticks(rotation=25)
plt.ylabel("Number of beekeepers")
plt.tight_layout()
sns.despine()
# plt.show()
plt.savefig("/home/stephen/Desktop/survey_plots/numberof_hives.png", bbox_inches="tight")
##
# Selection the way to find a solution for Varroa?

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 5), dpi=80,
                               gridspec_kw={"width_ratios": [2, 1.4]})
fig.subplots_adjust(wspace=.6)

bbox_props = dict(boxstyle="square,pad=0.2", fc="w", ec="k", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

shd_df = df['Q41 Should selection be carried out'].dropna()
shd_df.columns = ["selection"]

shdf = shd_df.value_counts().reset_index().rename(columns={"index": "Response",
                                                           'Q41 Should selection be carried out':
                                                           "Number of beekeepers"})

shdf.sort_values(by=['Number of beekeepers'], ascending=False, inplace=True)

shdf.columns = ("Answer", "Count")

sns.barplot(x=shdf.Answer, y=shdf.Count, palette="muted", edgecolor="k", linewidth=0.8, ax=ax1)
sns.despine()
for p in ax1.patches:
    ax1.annotate(format(p.get_height(), '.1f'),
                 (p.get_x() + p.get_width() / 2.,
                  p.get_height() - 1.2),
                 ha="center", va="center",
                 xytext=(0, 9), color="black", size=9,
                 textcoords="offset points")

ax1.set_xticklabels(["Yes, breed from \nonly the best queens", "Partially", "No"])
ax1.set_xlabel("Answer", fontsize=12)
ax1.set_ylabel("Count", fontsize=12)

ax1.set_title("Should selection be carried out?", y=1.07)


sele_df = df['Q51 Is selection a way to find a solution to Varroa'].dropna()
sele_df.columns = ["selection"]

sdf = sele_df.value_counts().reset_index().rename(columns={"index": "Response",
                                                           'Q51 Is selection a way to find a solution to Varroa':
                                                           "Number of beekeepers"})

sdf.sort_values(by=['Number of beekeepers'], ascending=True, inplace=True)
sizes_ax2 = sdf["Number of beekeepers"].to_list()


labels_ax2 = ['No, I fight Varroa \neffectively other ways',
              'Other answer given',
              'No, I think that other \nfactors are mainly\nimplicated',
              'I have not had to select',
              'Yes, offers ways\n to enable bees\n to survive',
              'Yes, as long as\n it does not reduce\n genetic diversity']
wedges_2, texts_2, pcts_2 = ax2.pie(sizes_ax2, wedgeprops={'width': .5, 'edgecolor': 'white'},
                                    startangle=-43, autopct='%.1f%%', pctdistance=.7,
                                    colors=["olive", "teal", "royalblue", "seagreen",
                                            "indianred", "darkturquoise", "r"])

bbox_props = dict(boxstyle="square,pad=0.2", fc="w", ec="w", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges_2):
    ang = (p.theta2 - p.theta1)/2 + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax2.annotate(labels_ax2[i] + " [" + str(sizes_ax2[i]) + "]", xy=(x, y), xytext=(1.15*np.sign(x), 1.4*y),
                 horizontalalignment=horizontalalignment, **kw)

ax2.set_title("Is selection the solution to Varroa?", y=1.13)
plt.setp(pcts_2, color="white", fontsize=9, bbox=dict(boxstyle="round4", facecolor="#445A64"))

plt.suptitle("Selection and varroa", fontsize=18, y=.98)
plt.tight_layout()
# plt.show()
plt.savefig("/home/stephen/Desktop/survey_plots/varroa_solution.png", bbox_inches="tight", dpi=200)

##
# Varroa tests

tests_df = df[["Q19 Varroa mortality, before treatment", "Q20 Varroa mortality, after treatment",
               "Q21 Varroa on bees", "Q22 Varroa in drone brood", "Q23 Varroa in worker brood",
               "Q24 Varroa reproduction"]]

tests_df.columns = ["Dead Varroa, before treatment", "Dead Varroa, after treatment",
                    "Varroa on bees", "Varroa in drone brood", "Varroa in worker brood",
                    "Varroa reproduction"]

tests_v = tests_df[[i for i in tests_df.columns]].astype("str")\
    .stack()\
    .value_counts()\
    .drop("nan")\
    .sort_values(ascending=False)

fig = sns.barplot(x=tests_v.index, y=tests_v, palette="muted", edgecolor="k", linewidth=0.8)
for p in fig.patches:
    percentage = '{:.1f}%'.format(100 * p.get_height()/total)
    x = p.get_x() + .45
    y = p.get_height()+3
    fig.annotate(percentage, (x, y), ha='center')
plt.xticks(rotation=20, horizontalalignment="right", fontsize=8)
plt.xlabel("Types of Varroa tests", fontsize=13)
plt.ylabel("Count", fontsize=13)
plt.ylim(0, 170)
plt.title(r"What percentage of beekeepers carry" + "\n" + "out these Varroa tests?", fontsize=13, y=1.08)
plt.tight_layout()
sns.despine()
# plt.show(fig)
plt.savefig("/home/stephen/Desktop/survey_plots/varroa_tests.png", bbox_inches="tight", dpi=200)

##
swarm_df = df["Q39 Practice swarm control"].replace("Yes (please specify which method and how often)", "Yes")\
    .dropna().value_counts()

fig = sns.barplot(x=swarm_df.index, y=swarm_df, palette="muted", edgecolor="k", linewidth=0.8)
for p in fig.patches:
    fig.annotate(format(p.get_height(), '.1f'),
                 (p.get_x() + p.get_width() / 2.,
                  p.get_height() - 4),
                 ha="center", va="center",
                 xytext=(0, 9), color="black", size=9,
                 textcoords="offset points")
change_width(fig, .55)
sns.despine()
plt.title("Proportion of Irish beekeepers who practice swarm control", y=1.05)
plt.xlabel("Swarm control")
plt.ylabel("Count")
plt.show()
plt.savefig("/home/stephen/Desktop/survey_plots/swarm_control.png", dpi=200)
##
fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(16, 8), dpi=80)

gs = gridspec.GridSpec(2, 15, hspace=.3, height_ratios=[1, 1])
gs.update(wspace=0.3)
ax2 = plt.subplot(gs[0, 1:5], )
ax3 = plt.subplot(gs[0, 6:10], )
ax4 = plt.subplot(gs[0, 11:15])
ax6 = plt.subplot(gs[1, 1:5])
ax7 = plt.subplot(gs[1, 6:10])
ax9 = plt.subplot(gs[1, 11:15])


fig.subplots_adjust(wspace=.3)
# swap to new line of bees or keep own

swapping_df = df[["Q53 Keep own bees even if a resistant line was created",
                  "Q54 Swap to new resistant line if they are better than own",
                  "Q55 Swap to new resistant line even if the produce 25% less honey",
                  "Q56 Swap to new resistant bees even if they produce 50% less honey",
                  "Q57 Swap to new resistant bees even if they barely produce honey",
                  "Q58 Swap to new resistant line even if they are more aggressive",
                  "Q59 Swap to new resistant bees even if they swarm more"]]

len(swapping_df)

len(swapping_df.dropna(how="all"))

swapping_df.dropna(how="all", inplace=True)

ax1_df = swapping_df["Q53 Keep own bees even if a resistant line was created"].fillna("Yes")\
    .replace({"My own bees as before, without change": "No"}).value_counts().reset_index().iloc[::-1]
ax1_df.columns = ("Answer", "Count")
total = ax1_df.sum()
sns.barplot(x=ax1_df.Answer, y=ax1_df.Count, palette="muted", edgecolor="k", linewidth=0.8, ax=ax1)
for p in ax1.patches:
    ax1.annotate(format(p.get_height(), '.1f'),
                 (p.get_x() + p.get_width() / 2.,
                  p.get_height()-4),
                 ha="center", va="center",
                 xytext=(0, 9), color="black", size=9,
                 textcoords="offset points")
    percentage = '{:.1f}%'.format(100 * p.get_height()/total[1])
    x = p.get_x() + .41
    y = p.get_height()-12
    ax1.annotate(percentage, (x, y), ha='center', color="w")

ax1.set_title("If they were the same\n in all other ways?")
ax1.set_xlabel(" ")
ax1.set_ylabel("Count")
change_width(ax1, .45)


ax2_df = swapping_df["Q54 Swap to new resistant line if they are better than own"].fillna("No")\
    .replace({"Resistant native bees, but only if they are at least good or better than my current bees": "Yes"})\
    .value_counts()\
    .to_frame()\
    .reset_index()\
    .sort_values(by="Q54 Swap to new resistant line if they are better than own", ascending=True)

ax2_df.columns = ("Answer", "Count")
total = ax2_df.sum()

sns.barplot(x=ax2_df.Answer, y=ax2_df.Count, palette="muted", edgecolor="k", linewidth=0.8, ax=ax2)
for p in ax2.patches:
    ax2.annotate(format(p.get_height(), '.1f'),
                 (p.get_x() + p.get_width() / 2.,
                  p.get_height()-4),
                 ha="center", va="center",
                 xytext=(0, 9), color="black", size=9,
                 textcoords="offset points")
    percentage = '{:.1f}%'.format(100 * p.get_height()/total[1])
    x = p.get_x() + .41
    y = p.get_height()-8
    ax2.annotate(percentage, (x, y), ha='center', color="w")
ax2.set_xlabel(" ")
ax2.set_ylabel(" ")
ax2.set_title("If they are better than\n your current bees")
change_width(ax2, .45)

ax3_df = swapping_df["Q55 Swap to new resistant line even if the produce 25% less honey"].fillna("No")\
    .replace({"Resistant native bees, even if they produce 25% less honey.": "Yes"})\
    .value_counts().to_frame().reset_index()
ax3_df.columns = ("Answer", "Count")
total = ax3_df.sum()
sns.barplot(x=ax3_df.Answer, y=ax3_df.Count, palette="muted", edgecolor="k", linewidth=0.8, ax=ax3)
for p in ax3.patches:
    ax3.annotate(format(p.get_height(), '.1f'),
                 (p.get_x() + p.get_width() / 2.,
                  p.get_height()-4),
                 ha="center", va="center",
                 xytext=(0, 9), color="black", size=9,
                 textcoords="offset points")
    percentage = '{:.1f}%'.format(100 * p.get_height()/total[1])
    x = p.get_x() + .41
    y = p.get_height()-11
    ax3.annotate(percentage, (x, y), ha='center', color="w")
ax3.set_xlabel(" ")
ax3.set_ylabel(" ")
ax3.set_title("If they produced 25% less honey?")
change_width(ax3, .45)


ax4_df = swapping_df["Q56 Swap to new resistant bees even if they produce 50% less honey"].fillna("No")\
    .replace({"Resistant native bees, even if they produce 50% less honey.": "Yes"})\
    .value_counts().to_frame().reset_index()
ax4_df.columns = ("Answer", "Count")
total = ax4_df.sum()
sns.barplot(x=ax4_df.Answer, y=ax4_df.Count, palette="muted", edgecolor="k", linewidth=0.8, ax=ax4)
for p in ax4.patches:
    ax4.annotate(format(p.get_height(), '.1f'),
                 (p.get_x() + p.get_width() / 2.,
                  p.get_height()-4),
                 ha="center", va="center",
                 xytext=(0, 9), color="black", size=9,
                 textcoords="offset points")
    percentage = '{:.1f}%'.format(100 * p.get_height()/total[1])
    x = p.get_x() + .41
    y = p.get_height()-17
    ax4.annotate(percentage, (x, y), ha='center', color="w")
ax4.set_xlabel(" ")
ax4.set_ylabel("Count")
ax4.set_title("If they produced 50% less honey")
change_width(ax4, .45)


ax6_df = swapping_df["Q57 Swap to new resistant bees even if they barely produce honey"].fillna("No")\
    .replace({"Resistant native bees, even if they barely produce honey": "Yes"})\
    .value_counts().to_frame().reset_index()
total = ax6_df.sum()
ax6_df.columns = ("Answer", "Count")
sns.barplot(x=ax6_df.Answer, y=ax6_df.Count, palette="muted", edgecolor="k", linewidth=0.8, ax=ax6)
for p in ax6.patches:
    ax6.annotate(format(p.get_height(), '.1f'),
                 (p.get_x() + p.get_width() / 2.,
                  p.get_height()-4),
                 ha="center", va="center",
                 xytext=(0, 9), color="black", size=9,
                 textcoords="offset points")
    percentage = '{:.1f}%'.format(100 * p.get_height()/total[1])
    x = p.get_x() + .41
    y = p.get_height()-14
    ax6.annotate(percentage, (x, y), ha='center', color="w")
ax6.set_xlabel(" ")
ax6.set_ylabel(" ")
ax6.set_title("If they produced barely any honey")
change_width(ax6, .45)

ax7_df = swapping_df["Q58 Swap to new resistant line even if they are more aggressive"].fillna("No")\
    .replace({"Resistant native bees, even if they are more aggressive": "Yes"})\
    .value_counts().to_frame().reset_index()
total = ax7_df.sum()
ax7_df.columns = ("Answer", "Count")
sns.barplot(x=ax7_df.Answer, y=ax7_df.Count, palette="muted", edgecolor="k", linewidth=0.8, ax=ax7)
for p in ax7.patches:
    ax7.annotate(format(p.get_height(), '.1f'),
                 (p.get_x() + p.get_width() / 2.,
                  p.get_height()-4),
                 ha="center", va="center",
                 xytext=(0, 9), color="black", size=9,
                 textcoords="offset points")
    percentage = '{:.1f}%'.format(100 * p.get_height()/total[1])
    x = p.get_x() + .41
    y = p.get_height()-18
    ax7.annotate(percentage, (x, y), ha='center', color="w")
ax7.set_xlabel(" ")
ax7.set_ylabel(" ")
ax7.set_title("If they are more aggressive")
change_width(ax7, .45)


ax9_df = swapping_df["Q59 Swap to new resistant bees even if they swarm more"].fillna("No")\
    .replace({"Resistant native bees, even if they have a higher swarming inclination.": "Yes"})\
    .value_counts().to_frame().reset_index()
total = ax9_df.sum()
ax9_df.columns = ("Answer", "Count")
sns.barplot(x=ax9_df.Answer, y=ax9_df.Count, palette="muted", edgecolor="k", linewidth=0.8, ax=ax9)
for p in ax9.patches:
    ax9.annotate(format(p.get_height(), '.1f'),
                 (p.get_x() + p.get_width() / 2.,
                  p.get_height()-8),
                 ha="center", va="center",
                 xytext=(0, 9), color="black", size=9,
                 textcoords="offset points")
    percentage = '{:.1f}%'.format(100 * p.get_height()/total[1])
    x = p.get_x() + .41
    y = p.get_height()-17
    ax9.annotate(percentage, (x, y), ha='center', color="w")
ax9.set_xlabel(" ")
ax9.set_ylabel(" ")
ax9.set_title("If they swarm more")
change_width(ax9, .45)

sns.despine()
plt.tight_layout()
plt.suptitle("Would beekeepers swap to a new Varroa resistant line of bees", y=1, fontsize=16)
plt.savefig("/home/stephen/Desktop/survey_plots/swap_to_new_resistant_dark_bee.png",
            bbox_inches="tight", dpi=200)

##

# doesnt treat for varroa

dt_df = df["Q30 Varroa treatment (I don't treat)"].fillna("I do treat").value_counts().reset_index()
dt_df.columns = ("Answer", "Count")

fig = sns.barplot(x=dt_df.Answer, y=dt_df.Count, palette="muted", edgecolor="k", linewidth=0.8)
change_width(fig, .45)
plt.xlabel("Answer")
plt.ylabel("Count")
plt.title("Do you treat for Varroa?")

for p in fig.patches:
    fig.annotate(format(p.get_height(), '.1f'),
                 (p.get_x() + p.get_width() / 2.,
                  p.get_height()-4),
                 ha="center", va="center",
                 xytext=(0, 9), color="black", size=9,
                 textcoords="offset points")
sns.despine()

plt.show()
plt.savefig("/home/stephen/Desktop/survey_plots/treat_yes_or_no.png", dpi=200)
##

dont_treat = df[df["Q30 Varroa treatment (I don't treat)"] == "I don't treat"]
do_treat = df[df["Q30 Varroa treatment (I don't treat)"].fillna(1) == 1]


dont_treat["Q5 Keeps dark bees"].value_counts()
do_treat["Q5 Keeps dark bees"].value_counts()

dont_treat["Q16 Percentage of Varroa-related winter losses"].value_counts()

dont_treat["Q30 Varroa treatment (I don't treat)"].value_counts()
# dont_treat[(dont_treat["Q16 Percentage of Varroa-related winter losses"] ==
                  #"Varroa is a problem for me every year, but I have things under control through treatments)")]

dont_treat = dont_treat.drop([125])
dont_treat["Q16 Percentage of Varroa-related winter losses"].value_counts()
do_treat["Q16 Percentage of Varroa-related winter losses"].value_counts()
do_treat["Q30 Varroa treatment (I don't treat)"].value_counts()

df["Q16 Percentage of Varroa-related winter losses"].value_counts()
df["Q30 Varroa treatment (I don't treat)"].value_counts()


##
ax1_df = swapping_df["Q53 Keep own bees even if a resistant line was created"].fillna("Yes")\
    .replace({"My own bees as before, without change": "No"}).value_counts().reset_index().iloc[::-1]
ax1_df.columns = ("Answer", "Count")
total = ax1_df.sum()
fig = sns.barplot(x=ax1_df.Answer, y=ax1_df.Count, palette="muted", edgecolor="k", linewidth=0.8)
for p in fig.patches:
    fig.annotate(format(p.get_height(), '.1f'),
                 (p.get_x() + p.get_width() / 2.,
                  p.get_height()-4),
                 ha="center", va="center",
                 xytext=(0, 9), color="black", size=9,
                 textcoords="offset points")
    percentage = '{:.1f}%'.format(100 * p.get_height()/total[1])
    x = p.get_x() + .41
    y = p.get_height()-12
    fig.annotate(percentage, (x, y), ha='center', color="w")

plt.title("Would you swap to a Varroa resistant\n line of Irish Honeybees?")
plt.xlabel("Answer")
plt.ylabel("Count")
change_width(fig, .45)
sns.despine()
plt.savefig("/home/stephen/Desktop/survey_plots/keep_bees_no_matter_what.png", dpi=200)
plt.show()

##
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(11, 5), dpi=80)

gs = gridspec.GridSpec(1, 10, hspace=.1, top=.75, left=.001)
ax1 = plt.subplot(gs[0, 1:5], )
ax2 = plt.subplot(gs[0, 6:10], )
swap2_df = df[["Q60 Swap to new hybrid resistant line or keep own bees",
               "Q61 Swap to new varroa resistant foreign dark bees"]]\
           .dropna()

ax1_df = swap2_df["Q60 Swap to new hybrid resistant line or keep own bees"]\
         .value_counts().to_frame().reset_index()\
         .replace("The dark bee, even if it is not resistant", "No")\
         .replace("The resistant bee, even if it is not a pure dark bee", "Yes")

ax1_df.columns = ("Answer", "Count")

total = ax1_df.sum()
sns.barplot(x=ax1_df.Answer, y=ax1_df.Count, palette="muted", edgecolor="k", linewidth=0.8, ax=ax1)
for p in ax1.patches:
    ax1.annotate(format(p.get_height(), '.1f'),
                 (p.get_x() + p.get_width() / 2.,
                  p.get_height()-4),
                 ha="center", va="center",
                 xytext=(0, 9), color="black", size=9,
                 textcoords="offset points")
    percentage = '{:.1f}%'.format(100 * p.get_height()/total[1])
    x = p.get_x() + .41
    y = p.get_height()-12
    ax1.annotate(percentage, (x, y), ha='center', color="w")
ax1.set_title("Would you swap to a Varroa resistant line\nof C-Lineage (Italian, Carniolan etc.) \nHoneybees?")
ax1.set_xlabel("Answer")
ax1.set_ylabel("Count")
change_width(ax1, .45)
sns.despine()


ax2_df = swap2_df["Q61 Swap to new varroa resistant foreign dark bees"]\
         .value_counts().to_frame().reset_index()\
         .replace("My\xa0own local bees, even if it is not resistant", "No")\
         .replace("Resistant dark bee, even if it does not come from Ireland", "Yes")

ax2_df.columns = ("Answer", "Count")

total = ax2_df.sum()
sns.barplot(x=ax2_df.Answer, y=ax2_df.Count, palette="muted", edgecolor="k", linewidth=0.8, ax=ax2)
for p in ax2.patches:
    ax2.annotate(format(p.get_height(), '.1f'),
                 (p.get_x() + p.get_width() / 2.,
                  p.get_height()-4),
                 ha="center", va="center",
                 xytext=(0, 9), color="black", size=9,
                 textcoords="offset points")
    percentage = '{:.1f}%'.format(100 * p.get_height()/total[1])
    x = p.get_x() + .41
    y = p.get_height()-12
    ax2.annotate(percentage, (x, y), ha='center', color="w")
ax2.set_title("Would you swap to a Varroa resistant line\nof Dark Bees which come from another\ncountry? (Switzerland etc.)")
ax2.set_xlabel("Answer")
ax2.set_ylabel("Count")
change_width(ax2, .45)
sns.despine()
plt.suptitle("Would Irish beekeepers swap to a Varroa resistant line?", fontsize=16)

plt.savefig("/home/stephen/Desktop/survey_plots/swap_hybrid_foreign.png", dpi=200)
plt.show()
##
