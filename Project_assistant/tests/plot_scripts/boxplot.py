import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def boxplot():

    pos_emb = pd.read_csv("Project_assistant/tests/results/data/positive_results.csv")
    neg_emb = pd.read_csv("Project_assistant/tests/results/data/negative_results.csv")
    pos_bleu = pd.read_csv("Project_assistant/tests/results/data/bleu_positive.csv")
    neg_bleu = pd.read_csv("Project_assistant/tests/results/data/bleu_negative.csv")

    matrix = np.vstack((pos_emb['avg'],neg_emb['avg'],pos_bleu['avg'],neg_bleu['avg'])).T

    fig, ax = plt.subplots()

    boxplot = ax.boxplot(matrix, vert=True, patch_artist=True) 

    colors = ['lightgreen', 'darkgreen', 'fuchsia', 'darkmagenta']
    for patch, color in zip(boxplot['boxes'], colors):
        patch.set_facecolor(color)

    labels = ['Pos embedding', 'Neg embedding', 'Pos BLEU', 'Neg BLEU']

    ax.set_xticklabels(labels)

    ax.set_xlabel('Testing method')
    ax.set_ylabel('Score')
    ax.set_title('Boxplot for different methods and scores')

    plt.savefig('Project_assistant/tests/results/plots/boxplot_avg.png')