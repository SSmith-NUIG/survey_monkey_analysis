import pandas as pd
import numpy as np
import re
import os
from os import path
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.patheffects as path_effects
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches

def change_width(axes, new_value):
    for patch in axes.patches:
        current_width = patch.get_width()
        diff = current_width - new_value

        # we change the bar width
        patch.set_width(new_value)

        # we recenter the bar
        patch.set_x(patch.get_x() + diff * .5)

df = pd.read_csv("/home/stephen/survey_cleaned.csv")

# MAKE FINAL PLOTS FOR JOURNAL SUBMISSION
# three plots of why keep black bee
# number of colonies kept by beekeepers # number of varroa losses
# how often do inspections # varroa selection donut

#fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(16, 8), dpi=80)
fig = plt.figure(dpi=300, tight_layout=True)
fig.set_size_inches(8.27, 11.69, forward=True)
plt.figtext(0.12, .92, "A", fontsize=16, fontweight="bold")
gs = gridspec.GridSpec(3, 21, hspace=.4, height_ratios=[1, 1, 1.1],bottom=0.15)

ax1 = plt.subplot(gs[0, 0:7])
ax2 = plt.subplot(gs[0, 7:14])
ax3 = plt.subplot(gs[0, 14:21])

ax4 = plt.subplot(gs[1, 0:8])
ax5 = plt.subplot(gs[1, 10:11])
ax5.axis("off")
ax6 = plt.subplot(gs[1, 11:20])

ax7 = plt.subplot(gs[2, 0:8])
ax8 = plt.subplot(gs[2, 10:11])
ax8.axis("off")
ax9 = plt.subplot(gs[2, 11:21])

fig.subplots_adjust(wspace=.1)
fig.text(10, 20, "function", fontsize=25)
# AX1
bbox_props = dict(boxstyle="square,pad=0.2", fc="w", ec="k", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-", color="black"), bbox=bbox_props, zorder=0, va="center")
df1 = df['Q6 Black bee is the best bee for my environment'].dropna()
df1.columns = ["selection"]
df_1 = df1.value_counts().reset_index().rename(columns={"index": "Response",
                                                                 'Q6 Black bee is the best bee for my environment':
                                                                     "Number of beekeepers"})
df_1.sort_values(by=['Number of beekeepers'], ascending=True, inplace=True)
sizes_ax1 = df_1["Number of beekeepers"].to_list()
labels = ["1", "2", "3", "4", "5"]
wedges_1, texts_1, pcts_1 = ax1.pie(sizes_ax1, wedgeprops={'width': .5, 'edgecolor': 'white'},
                                    startangle=-25, autopct='%.1f%%', pctdistance=.9,
                                    colors=["tan", "slategrey", "goldenrod", "indianred", "seagreen"])

pctdists1 = [1,1.05,1,1,1]
xi,yi= pcts_1[0].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists1[0]*ri*np.cos(phi)
y = pctdists1[0]*ri*np.sin(phi)+-.13
pcts_1[0].set_position((x,y))

xi,yi= pcts_1[1].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists1[1]*ri*np.cos(phi)+.08
y = pctdists1[1]*ri*np.sin(phi)+.15
pcts_1[1].set_position((x,y))

xi,yi= pcts_1[2].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists1[2]*ri*np.cos(phi)
y = pctdists1[2]*ri*np.sin(phi)+.08
pcts_1[2].set_position((x,y))



plt.setp(pcts_1, color="white", fontsize=12, bbox=dict(boxstyle="round4", facecolor="#445A64"))
ax1.set_title("Black bee is the best bee\nfor my environment", y=0.95)

# AX2
df2 = df['Q7 Black bee was already here'].dropna()
df2.columns = ["selection"]
df_2 = df2.value_counts().reset_index().rename(columns={"index": "Response",
                                                                 'Q7 Black bee was already here':
                                                                     "Number of beekeepers"})
df_2.sort_values(by=['Number of beekeepers'], ascending=True, inplace=True)
sizes_ax2 = df_2["Number of beekeepers"].to_list()
labels = ["1", "2", "3", "4", "5"]
wedges_2, texts_2, pcts_2 = ax2.pie(sizes_ax2, wedgeprops={'width': .5, 'edgecolor': 'white'},
                                    startangle=-72, autopct='%.1f%%', pctdistance=.9,
                                    colors=["tan", "slategrey", "goldenrod", "indianred", "seagreen"])



pctdists2 = [1,1.05,1,1,1]

xi,yi= pcts_2[0].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists2[0]*ri*np.cos(phi)
y = pctdists2[0]*ri*np.sin(phi)-.1
pcts_2[0].set_position((x,y))

xi,yi= pcts_2[1].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists2[1]*ri*np.cos(phi)+.1
y = pctdists2[1]*ri*np.sin(phi)+.13
pcts_2[1].set_position((x,y))

xi,yi= pcts_2[4].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists2[4]*ri*np.cos(phi)+.15
y = pctdists2[4]*ri*np.sin(phi)-.5
pcts_2[4].set_position((x,y))

plt.setp(pcts_2, color="white", fontsize=12, bbox=dict(boxstyle="round4", facecolor="#445A64"))
ax2.set_title("Black bee was \nalready in my area", y=.95)
ax2.axvline(linewidth=1, color="k", x=-1.23)



# AX3
df3 = df['Q8 Conservation of black bee'].dropna()
df3.columns = ["selection"]
df_3 = df3.value_counts().reset_index().rename(columns={"index": "Response",
                                                                 'Q8 Conservation of black bee':
                                                                     "Number of beekeepers"})
df_3.sort_values(by=['Number of beekeepers'], ascending=True, inplace=True)
sizes_ax3 = df_3["Number of beekeepers"].to_list()
labels = ["1", "2", "3", "4", "5"]
wedges_3, texts_3, pcts_3 = ax3.pie(sizes_ax3, wedgeprops={'width': .5, 'edgecolor': 'white'},
                                    startangle=20, autopct='%.1f%%', pctdistance=.9,
                                    colors=["tan", "slategrey", "goldenrod", "indianred", "seagreen"])

plt.setp(pcts_3, color="white", fontsize=12, bbox=dict(boxstyle="round4", facecolor="#445A64"))
pctdists3 = [.7, 1.07, 1.07, 1.05, 1.05]


xi,yi= pcts_3[0].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists3[0]*ri*np.cos(phi)+.35
y = pctdists3[0]*ri*np.sin(phi)-.15
pcts_3[0].set_position((x,y))

xi,yi= pcts_3[1].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists3[1]*ri*np.cos(phi)+.15
y = pctdists3[1]*ri*np.sin(phi)
pcts_3[1].set_position((x,y))

xi,yi= pcts_3[2].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists3[2]*ri*np.cos(phi)-.05
y = pctdists3[2]*ri*np.sin(phi)+.08
pcts_3[2].set_position((x,y))

xi,yi= pcts_3[3].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists3[3]*ri*np.cos(phi)-.25
y = pctdists3[3]*ri*np.sin(phi)
pcts_3[3].set_position((x,y))

xi,yi= pcts_3[4].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists3[4]*ri*np.cos(phi)-.1
y = pctdists3[4]*ri*np.sin(phi)+.15
pcts_3[4].set_position((x,y))

ax3.set_title("Conservation of \nthe black bee", y=.95)
ax3.axvline(linewidth=1, color="k", x=-1.23)
#"tan", "slategrey", "goldenrod", "indianred", "seagreen"
five = mpatches.Patch(color='seagreen', label='5')
four = mpatches.Patch(color='indianred', label='4')
three = mpatches.Patch(color='goldenrod', label='3')
two = mpatches.Patch(color='slategrey', label='2')
one = mpatches.Patch(color='tan', label='1')

ax3.legend(handles=[five,four,three,two,one], loc=1,bbox_to_anchor=(.85, 0.3, 0.5, 0.5), title="Rating", prop={'size':9})

# AX4
hives = df.loc[:, ["Q2 Number of Colonies"]]
hive_bins = [1, 3, 5, 10, 30, 60, 75, 100, 150, 250, 1000]
hive_labels = ["1-2", "3-5", "6-10", "11-30", "31-60", "61-75", "76-100", "101-150", "150-250", "250-1000"]
hives["hives_range"] = pd.cut(hives.loc[:, "Q2 Number of Colonies"], hive_bins, labels=hive_labels, include_lowest=True)

df.loc[:, "Hives Range"] = hives["hives_range"]
df.loc[:, "Hives Range"].value_counts()
hives.sort_values("Q2 Number of Colonies", inplace=True)
hives_grouped_df = hives.groupby(["hives_range"], as_index=False).count()

sns.barplot(y=hives_grouped_df["hives_range"], x=hives_grouped_df["Q2 Number of Colonies"], palette="deep",
                  edgecolor="k", linewidth=0.8, ax=ax4)
yy = hives_grouped_df["Q2 Number of Colonies"]
for index, data in enumerate(yy):
    ax4.text(data + 3, index + .1, str(data), color="black", fontsize=12)
ax4.set_title("B", size=16, loc="left", fontweight="bold")
ax4.set_ylabel("Number of colonies", size=16)
ax4.set_xlabel("Number of beekeepers", fontsize=16)
plt.show()

# AX6
varroa_losses = df["Q16 Percentage of Varroa-related winter losses"]
varroa_losses.value_counts()
varroa_losses.columns = ["losses"]
vdf = varroa_losses.value_counts().reset_index().rename(columns={"index": "Response",
                                                                 "Q16 Percentage of Varroa-related winter losses":
                                                                     "Number of beekeepers"})

vdf.sort_values(by=['Number of beekeepers'], ascending=True, inplace=True)
sizes = vdf["Number of beekeepers"].to_list()
labels1 = ["Serious problem\n every year\n(25%+) (4)",
           "Things under \ncontrol through\n treatments (56)",
           "Occasional losses\n(10–20%) (75)",
           "Low losses \n(~5%) (185)"
           ]
ax6_wedges, ax6_texts, ax6_pcts = ax6.pie(sizes, wedgeprops={'width': .5, 'edgecolor': 'white'},
                             startangle=-63, autopct='%.1f%%', pctdistance=.7,
                             colors=["olive", "royalblue", "seagreen", "indianred"])
bbox_props = dict(boxstyle="square,pad=0.2", fc="w", ec="w", lw=0.6)
kw = dict(arrowprops=dict(arrowstyle="-", facecolor="black", color="black"), bbox=bbox_props, zorder=0, va="center")
for i, p in enumerate(ax6_wedges):
    ang = (p.theta2 - p.theta1)/2 + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax6.annotate(labels1[i], xy=(x, y), xytext=(1.2*np.sign(x), 1.7*y),
                horizontalalignment=horizontalalignment, **kw)

plt.setp(ax6_pcts, color="white", fontsize=12, bbox=dict(boxstyle="round4", facecolor="#445A64"))

pctdists6 = [1, 1, 1, 1, 1]

xi,yi= ax6_pcts[0].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists6[0]*ri*np.cos(phi)
y = pctdists6[0]*ri*np.sin(phi)
ax6_pcts[0].set_position((x,y))

xi,yi= ax6_pcts[1].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists6[1]*ri*np.cos(phi)+.3
y = pctdists6[1]*ri*np.sin(phi)+.1
ax6_pcts[1].set_position((x,y))

xi,yi= ax6_pcts[2].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists6[2]*ri*np.cos(phi)+.2
y = pctdists6[2]*ri*np.sin(phi)+.1
ax6_pcts[2].set_position((x,y))

xi,yi= ax6_pcts[3].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists6[3]*ri*np.cos(phi)-.3
y = pctdists6[3]*ri*np.sin(phi)+.2
ax6_pcts[3].set_position((x,y))

ax6.set_title("C", fontsize=16, loc="left", fontweight="bold")

# AX7
df_treatments = df[["Q31 Approved chemical treatments in spring/autumn",
                    "Q32 Oxalic acid in winter",
                    "Q33 oxalic acid and Queen caged",
                    "Q34 Oxalic acid and nuc creation",
                    "Q35 Removal of drone brood",
                    "Q36 Removal of all brood",
                    "Q37 Frequent nuc creation/requeening"]]
df_treatments.columns = ("Treat in spring+autumn",
                         "Winter oxalic acid",
                         "Oxalic acid + cage queen",
                         "Oxalic acid + nuc",
                         "Remove drone brood",
                         "Remove all brood",
                         "Nuc creation/re-queen")
treatment_count = df_treatments.count().reset_index().rename(columns={"index": "Treatment", 0: "Number of beekeepers"})
yy = treatment_count["Number of beekeepers"]

# treatment_count.plot.bar()
sns.barplot(x=treatment_count["Treatment"],
            y=treatment_count["Number of beekeepers"],
            palette="muted", edgecolor="k", linewidth=0.8, ax=ax7)
for p in ax7.patches:
    ax7.annotate(format(p.get_height(), '.0f'),
                 (p.get_x() + p.get_width() / 2.,
                  p.get_height()-2),
                 ha="center", va="center",
                 xytext=(0, 9), color="black", size=12,
                 textcoords="offset points")
    x = p.get_x() + .41
    y = p.get_height()-12
#for index, data in enumerate(yy):
#    ax7.text(data, index, str(data), color="black", fontsize=13)

ax7.set_xlabel(" ", fontsize=1)
ax7.set_ylabel("Number of beekeepers", fontsize=16)
ax7xlabels = ax7.get_xticklabels()
ax7.set_xticklabels(ax7xlabels, rotation=50, ha="right", fontsize=12)
ax7.set_title("D", fontsize=16, y=1.01, loc="left", fontweight="bold")

#ax7.tick_params(axis='x', labelrotation=45, labelright=True)
sns.despine()
# AX9
bbox_props = dict(boxstyle="square,pad=0.2", fc="w", ec="k", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

sele_df = df['Q51 Is selection a way to find a solution to Varroa'].dropna()
sele_df.columns = ["selection"]

sdf = sele_df.value_counts().reset_index().rename(columns={"index": "Response",
                                                           'Q51 Is selection a way to find a solution to Varroa':
                                                           "Number of beekeepers"})

sdf.sort_values(by=['Number of beekeepers'], ascending=True, inplace=True)
sizes_ax9 = sdf["Number of beekeepers"].to_list()


labels_ax9 = ['I fight Varroa \neffectively\n other ways',
              'Other',
              'Other \nfactors are mainly\nimplicated',
              'I have not \nhad to select',
              'It will \nenable bees\n to survive',
              'As long \nas it does not \nreduce genetic\n diversity']
wedges_9, texts_9, pcts_9 = ax9.pie(sizes_ax9, wedgeprops={'width': .5, 'edgecolor': 'white'},
                                    startangle=-43, autopct='%.1f%%', pctdistance=.7,
                                    colors=["olive", "teal", "royalblue", "seagreen",
                                            "indianred", "darkturquoise", "r"])

bbox_props = dict(fc="w", ec="w", lw=0.73, alpha=0)
kw = dict(arrowprops=dict(arrowstyle="-",facecolor="black", color="black"),
          bbox=bbox_props, zorder=0, va="center",
          annotation_clip=False)

for i, p in enumerate(wedges_9):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))-.1
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = f"angle,angleA=0,angleB={ang}"
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    plt.annotate(labels_ax9[i] + " (" + str(sizes_ax9[i]) + ")", xy=(x, y), xytext=(1.1*np.sign(x), 1.2*y),
                 horizontalalignment=horizontalalignment, **kw)

plt.setp(pcts_9, color="white", fontsize=12, bbox=dict(boxstyle="round4", facecolor="#445A64"))
pctdists9 = [1, 1, 1, 1, 1, 1]
xi,yi= pcts_9[0].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists9[0]*ri*np.cos(phi)-.15
y = pctdists9[0]*ri*np.sin(phi)-.1
pcts_9[0].set_position((x,y))

xi,yi= pcts_9[1].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists9[1]*ri*np.cos(phi)-.1
y = pctdists9[1]*ri*np.sin(phi)
pcts_9[1].set_position((x,y))

xi,yi= pcts_9[2].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists9[2]*ri*np.cos(phi)-.1
y = pctdists9[2]*ri*np.sin(phi)
pcts_9[2].set_position((x,y))

xi,yi= pcts_9[3].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists9[3]*ri*np.cos(phi)-.1
y = pctdists9[3]*ri*np.sin(phi)+.1
pcts_9[3].set_position((x,y))

xi,yi= pcts_9[4].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists9[4]*ri*np.cos(phi)
y = pctdists9[4]*ri*np.sin(phi)+.1
pcts_9[4].set_position((x,y))

xi,yi= pcts_9[5].get_position()
ri = np.sqrt(xi**2+yi**2)
phi = np.arctan2(yi,xi)
x = pctdists9[5]*ri*np.cos(phi)-.1
y = pctdists9[5]*ri*np.sin(phi)-.2
pcts_9[5].set_position((x,y))
sns.despine()
ax9.set_title("E", fontsize=16, y=.98, loc="left", fontweight="bold")


plt.savefig("/home/stephen/wtf2.png")
