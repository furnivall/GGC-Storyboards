'''
This script will build the matplotlib graphs that populate top and bottom left of the storyboard (i.e. Stat/Mand and
absence)
'''

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.font_manager
import numpy as np
print(matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf'))

def stat_mand_graph():
    df = pd.read_excel('C:/Learnpro_Extracts/lp-graphdata.xlsx')

    pos = list(range(len(df['Month'])))
    width= 0.05

    courses = ['Month', 'Equality', 'Fire Safety',
           'Health & Safety', 'Infection Control',
           'Info Governance', 'Manual Handling', 'Protection',
           'Security', 'Violence']

    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(5.795, 2.25))
    #fig, ax = plt.subplots(figsize=(2.895, 1.125))
    # below is the list of default matplotlib styles, we can add if necessary
    # ['Solarize_Light2', '_classic_test_patch', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight',
    #  'ggplot', 'grayscale', 'seaborn', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-dark', 'seaborn-dark-palette',
    #  'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel',
    #  'seaborn-poster', 'seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'tableau-colorblind10']

    for i, j in enumerate(courses[1:]):
        print(i)
        print(j)
        plt.bar([p + width * i * 1.8 for p in pos], df[j], alpha=0.4, label=j,
                width=width)

    ax.set_ylabel("COMPLIANCE", fontdict={'family':'tahoma', 'size':8, 'color':'#003087'})
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.00))
    ax.set_xticklabels(df['Month'], fontdict={'family':'tahoma', 'size':8, 'color':'#003087'})
    ax.set_xticks([p + 6 * width for p in pos])

    l = ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3), ncol=5, prop={'size':6}, frameon=True, handlelength=0.7)
    for text in l.get_texts():
        text.set_color("#003087")
    ax.yaxis.set_tick_params(labelsize=6, labelcolor='#003087')
    plt.title("STATUTORY AND MANDATORY TRAINING", fontdict={'family':'arial', 'color':'#003087', 'size':12, 'weight':'bold'}, pad=30)
    plt.tight_layout()
    plt.savefig('C:/storyboards/graph1.jpg',edgecolor='#003087', dpi=300)


def absence_graph():
    df = pd.read_excel('C:/storyboards/absence_graphdata.xlsx')
    total_abs = df['Total Absence'].to_list()
    print(total_abs)
    short_term = df['Short Term Absence'].to_list()
    long_term = df['Long Term Absence'].to_list()
    labels = df['Month'].to_list()
    x = np.arange(len(labels))
    print(x)
    width = 0.5
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(5.795, 2.25))

    bar1 = ax.bar(x - 0.05 - width/3, total_abs, width/3, label="Total Absence")
    bar2 = ax.bar(x + 0.05 + width/3, short_term, width/3, label="Short Term Absence")
    bar3 = ax.bar(x, long_term, width/3, label="Long Term Absence")

    ax.set_ylabel('ABSENCE %', fontdict={'family':'tahoma', 'size':8,'color':'#003087'}, )
    ax.set_title('ABSENCE', fontdict={'family':'arial', 'color':'#003087', 'size':12, 'weight':'bold'}, pad=35)
    ax.yaxis.set_tick_params(labelsize=6, labelcolor='#003087')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontdict={'family':'tahoma', 'size':8, 'color':'#003087'})
    l = ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.30), ncol=5, prop={'size': 10}, frameon=True,
                  handlelength=0.7)
    plt.tight_layout()
    plt.savefig('C:/storyboards/graph2.jpg', dpi=300)

absence_graph()
stat_mand_graph()