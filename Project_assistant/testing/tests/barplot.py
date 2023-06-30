import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def barplot_vector(data):

    # Set the positions of the bars
    positions = np.arange(len(data))

    # Set the grouping of bars
    grouping = [2, 3, 3, 2]

    # Create the figure and axes
    fig, ax = plt.subplots()

    labels = ['pos gpt', 'neg gpt', 'pos embed min', 'pos embed avg', 'pos embed max', 'neg embed min', 'neg embed avg', 'neg embed max', 'pos bleu', 'neg bleu']
    colors = ['gold', 'lightsalmon', 'darkorchid', 'goldenrod']

    # Plot the bars
    bar_width = 0.5  # Adjust this value to set the width of the bars
    current_position = 0
    for i, group in enumerate(grouping):
        ax.bar(positions[current_position:current_position+group], data[current_position:current_position+group],
            bar_width, color=colors[i % len(colors)])
        current_position += group
        

    # Set the x-axis ticks and labels
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, rotation = 15, ha = 'right')

    # Set the y-axis label
    ax.set_ylabel('Score')

    # Set the title
    ax.set_title('Bar Plot for different methods and their score')

    # Show the plot
    plt.savefig('Project_assistant/testing/tests/plots_n_results/barplot_tot.png')


pos_embed = pd.read_csv("Project_assistant/testing/tests/data/positive_results.csv")
neg_embed = pd.read_csv("Project_assistant/testing/tests/data/negative_results.csv")
pos_bleu = pd.read_csv("Project_assistant/testing/tests/data/bleu_positive.csv")
neg_bleu = pd.read_csv("Project_assistant/testing/tests/data/bleu_negative.csv")

smpe = np.sum(pos_embed['avg'])
smne = np.sum(neg_embed['avg'])
smpb = np.sum(pos_bleu['avg'])
smnb = np.sum(neg_bleu['avg'])

smpe1 = np.sum(pos_embed['min'])
smne1 = np.sum(neg_embed['min'])

smpe2 = np.sum(pos_embed['max'])
smne2 = np.sum(neg_embed['max'])

gpt_ans_pos = 10
gpt_ans_neg = 1

vector = [gpt_ans_pos, gpt_ans_neg, smpe2, smpe, smpe1, smne2, smne, smne1, smpb, smnb]

barplot_vector(vector)